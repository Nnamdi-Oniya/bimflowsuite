from celery import shared_task
from ifcopenshell import file as ifc_file
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from .models import GeneratedIFC
from .generators import (
    building,
    bridge,
    road,
    highrise,
    tunnel,
    generic,
)
from bimflow.consumers import broadcast_progress
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def generate_ifc_task(self, model_id, asset_type_code, spec_json, scenario_id=None):
    try:
        model = GeneratedIFC.objects.get(id=model_id)
        model.status = "generating"
        model.save()

        # Broadcast progress
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"task_{self.request.id}",
            {"type": "task_update", "status": "generating", "progress": 30},
        )

        # Get generator function for asset type
        generators = {
            "building": building.generate_building_ifc,
            "bridge": bridge.generate_bridge_ifc,
            "road": road.generate_road_ifc,
            "highrise": highrise.generate_highrise_ifc,
            "tunnel": tunnel.generate_tunnel_ifc,  # New example
            # Add more: 'railway': railway.generate_railway_ifc,
        }
        gen_func = generators.get(asset_type_code)

        # Fallback to generic if not implemented
        if not gen_func:
            logger.warning(
                f"Using generic fallback for {asset_type_code}; implement custom generator."
            )
            ifc_string = generic.generate_generic_ifc(spec_json, asset_type_code)
            spec_json["_fallback_used"] = True  # Flag in results
        else:
            ifc_string = gen_func(spec_json)

        # Federated merge if scenario
        if scenario_id:
            # Placeholder: Merge with baseline IFC
            pass

        # Use new method to save
        base64_data = base64.b64encode(ifc_string.encode()).decode()
        model.save_ifc_from_base64(base64_data, f"{model.id}.ifc")

        async_to_sync(channel_layer.group_send)(
            f"task_{self.request.id}",
            {"type": "task_update", "status": "completed", "progress": 100},
        )

        task_instance = model.tasks.filter(task_id=self.request.id).first()
        if task_instance:
            task_instance.mark_completed(
                {
                    "status": "success",
                    "model_id": model_id,
                    "fallback_used": spec_json.get("_fallback_used", False),
                }
            )

        return {"status": "success", "model_id": model_id}

    except Exception as e:
        logger.error(f"IFC generation failed: {e}")
        model = GeneratedIFC.objects.get(id=model_id)
        model.status = "failed"
        model.error_message = str(e)
        model.save()
        task_instance = model.tasks.filter(task_id=self.request.id).first()
        if task_instance:
            task_instance.mark_failed(str(e))
        raise self.retry(exc=e, countdown=60)
