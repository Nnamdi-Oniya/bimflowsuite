from celery import shared_task
import logging
import traceback
from datetime import datetime
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import GeneratedIFC, Site
from .generators.building import BuildingIFCGenerator
from .generators.bridge import BridgeIFCGenerator
from .generators.road import RoadIFCGenerator

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_ifc_for_site(self, site_id):
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

        # Create GeneratedIFC record
        generated_ifc = GeneratedIFC.objects.create(
            project=project,
            name=f"{site.site_name} - IFC Generation",
            asset_type="other",
            ifc_schema_version=site.ifc_schema_version,
            status="generating",
            specifications={
                "site_id": str(site_id),
                "project_type": project.project_type,
                "spatial_element_count": site.spatial_structures.count(),
            },
        )

        logger.info(f"Starting IFC generation for site: {site_id}")
        start_time = datetime.now()

        # Select generator based on project type
        generator_class = _get_generator_class(project.project_type)

        if not generator_class:
            raise ValueError(
                f"No generator implemented for project type: {project.project_type}"
            )

        # Instantiate and generate IFC
        generator = generator_class(site)
        ifc_string = generator.generate()

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


def _get_generator_class(project_type):
    """
    Factory method to select appropriate generator class based on project type.

    Args:
        project_type: str - Project type from Project.PROJECT_TYPE_CHOICES

    Returns:
        Generator class or None if not implemented
    """
    generators = {
        "BUILDING": BuildingIFCGenerator,
        "INFRA_BRIDGE": BridgeIFCGenerator,
        "INFRA_ROAD": RoadIFCGenerator,
        # Additional types can be added as generators are implemented:
        # "INFRA_RAILWAY": RailwayIFCGenerator,
        # "INFRA_TUNNEL": TunnelIFCGenerator,
        # "INDUSTRIAL_FACTORY": FactoryIFCGenerator,
    }
    return generators.get(project_type)
