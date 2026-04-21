from config.celery import app
import logging
import os
import traceback
from datetime import datetime
from django.utils import timezone
from django.core.files.base import ContentFile
import tempfile
import ifcopenshell
from .models import GeneratedIFC, Site, Facility
from .generators.building import BuildingIFCGenerator
from .generators.bridge import BridgeIFCGenerator
from .generators.road import RoadIFCGenerator
from .generators.railway import RailwayIFCGenerator

logger = logging.getLogger(__name__)


@app.task(bind=True)
def generate_ifc_for_site(self, site_id, facility_id=None):
    """
    Generate IFC4X3 file for a site with its spatial structure and assets.

    Uses Factory Pattern to select appropriate generator based on project_type:
    - BUILDING → BuildingIFCGenerator (structural analysis properties)
    - INFRA_BRIDGE → BridgeIFCGenerator (bridge-specific properties)
    - INFRA_ROAD → RoadIFCGenerator (pavement and road properties)

    Args:
        site_id: UUID of the Site to generate IFC for

    Returns:
        dict: {"status": "success", "site_id": site_id, "generated_ifc_id": generated_ifc_id}

    Raises:
        Propagates exception for retry handling
    """
    try:
        site = Site.objects.get(id=site_id)
        project = site.project
        facility = None
        if facility_id:
            facility = Facility.objects.filter(id=facility_id, site=site).first()
        if not facility:
            facility = Facility.objects.filter(site=site).first()

        # Reuse or create a single GeneratedIFC per site
        generated_ifc = (
            GeneratedIFC.objects.filter(
                project=project, specifications__site_id=str(site_id)
            )
            .order_by("-created_at")
            .first()
        )
        # Derive asset_type from facility or site/project type
        project_type_map = {
            "IFC_BUILDING": "building",
            "IFC_ROAD": "road",
            "IFC_BRIDGE": "bridge",
            "IFC_TUNNEL": "tunnel",
            "IFC_RAILWAY": "railway",
            "IFC_SITE": "site",
        }
        active_type_raw = facility.facility_type if facility else "IFC_SITE"
        active_type = _normalize_facility_type(active_type_raw) or "IFC_SITE"
        derived_asset_type = project_type_map.get(active_type, "site")

        if generated_ifc:
            # Replace previous file/content
            if generated_ifc.ifc_file:
                generated_ifc.ifc_file.delete(save=False)
            generated_ifc.status = "generating"
            generated_ifc.asset_type = derived_asset_type
            generated_ifc.error_message = None
            generated_ifc.error_details = {}
            generated_ifc.completed_at = None
            generated_ifc.generation_warnings = []
        else:
            generated_ifc = GeneratedIFC(
                project=project,
                name=f"{site.site_name} - IFC Generation",
                asset_type=derived_asset_type,
                ifc_schema_version=site.ifc_schema_version,
                status="generating",
                specifications={"site_id": str(site_id), "facility_id": str(facility.id) if facility else None},
            )

        # Update shared specs every run
        generated_ifc.specifications.update(
            {
                "facility_type": active_type,
                "spatial_element_count": site.spatial_structures.count(),
            }
        )
        generated_ifc.save()

        logger.info(f"Starting IFC generation for site: {site_id}")
        start_time = datetime.now()

        # Select generator based on project type
        generator_class = _get_generator_class(active_type)

        if not generator_class:
            raise ValueError(
                f"Unsupported generator for facility type: {active_type}"
            )

        # Instantiate and generate IFC
        generator = generator_class(site, facility=facility)
        ifc_string = generator.generate()

        # Validate generated IFC by reopening with ifcopenshell
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".ifc", delete=False) as tmp:
                tmp.write(ifc_string.encode())
                tmp.flush()
                tmp_path = tmp.name
                ifcopenshell.open(tmp.name)
        except Exception as validate_exc:
            generated_ifc.status = "failed"
            generated_ifc.error_message = f"IFC validation failed: {validate_exc}"
            generated_ifc.error_details = {
                "exception_type": type(validate_exc).__name__,
                "exception_message": str(validate_exc),
            }
            generated_ifc.save()
            return {
                "status": "failed",
                "site_id": str(site_id),
                "generated_ifc_id": str(generated_ifc.id),
                "error": generated_ifc.error_message,
            }
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        # Save generated IFC file
        filename = f"{site_id}_{site.ifc_schema_version}.ifc"
        generated_ifc.ifc_file.save(filename, ContentFile(ifc_string.encode()))

        # Calculate generation time
        generation_time = (datetime.now() - start_time).total_seconds()

        # Update GeneratedIFC with metadata
        generated_ifc.status = "completed"
        generated_ifc.file_size = len(ifc_string.encode())
        generated_ifc.file_format = "ifc"
        generated_ifc.completed_at = timezone.now()

        # Capture generation metadata
        generated_ifc.generation_metadata = {
            "total_elements": generator.element_map.__len__()
            if hasattr(generator, "element_map")
            else 0,
            "spatial_elements": site.spatial_structures.count(),
            "assets": site.spatial_structures.filter(assets__isnull=False).count(),
            "property_sets": generator.property_sets_count
            if hasattr(generator, "property_sets_count")
            else 0,
            "schema_version": generator.metadata.get(
                "schema_version", site.ifc_schema_version
            ),
            "generator_class": generator_class.__name__,
            "generator_version": "1.0.0",
            "generation_time_seconds": generation_time,
        }

        # Capture any warnings
        if hasattr(generator, "warnings"):
            generated_ifc.generation_warnings = generator.warnings

        generated_ifc.save()

        logger.info(
            f"IFC generation successful: {generated_ifc.id} "
            f"({generation_time:.2f}s, {generated_ifc.file_size} bytes)"
        )

        return {
            "status": "success",
            "site_id": str(site_id),
            "generated_ifc_id": str(generated_ifc.id),
            "generation_time": generation_time,
        }

    except Site.DoesNotExist:
        logger.error(f"Site not found: {site_id}")
        raise ValueError(f"Site with ID {site_id} does not exist")

    except Exception as e:
        logger.error(f"IFC generation failed for site {site_id}: {str(e)}")

        # Try to update the GeneratedIFC record with error details
        try:
            if "generated_ifc" in locals():
                generated_ifc.status = "failed"
                generated_ifc.error_message = str(e)
                generated_ifc.error_details = {
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                    "timestamp": timezone.now().isoformat(),
                }
                generated_ifc.save()
        except Exception as save_error:
            logger.error(f"Failed to save error details: {str(save_error)}")

        # Re-raise for Celery retry mechanism
        raise self.retry(exc=e, countdown=60, max_retries=3)


def _normalize_facility_type(ftype):
    return ftype.upper() if ftype else None


def _get_generator_class(project_type):
    """
    Factory method to select appropriate generator class based on project type.

    Args:
        project_type: str - Project type from Project.PROJECT_TYPE_CHOICES

    Returns:
        Generator class or None if not implemented
    """
    generators = {
        "IFC_BUILDING": BuildingIFCGenerator,
        "IFC_BRIDGE": BridgeIFCGenerator,
        "IFC_ROAD": RoadIFCGenerator,
        "IFC_TUNNEL": RoadIFCGenerator,  # placeholder until tunnel generator is wired
        "IFC_RAILWAY": RailwayIFCGenerator,
    }
    return generators.get(project_type)
