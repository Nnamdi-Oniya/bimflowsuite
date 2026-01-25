from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AnalyticsRun
from .serializers import AnalyticsRunSerializer
from apps.parametric_generator.models import GeneratedIFC
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


class AnalyticsRunViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsRun.objects.all()
    serializer_class = AnalyticsRunSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        return self.queryset.filter(model__program_spec__intent__user=self.request.user)

    @action(detail=False, methods=["post"])
    def run(self, request):
        model_id = request.data.get("model_id")
        atype = request.data.get("type", "qto")

        try:
            model = GeneratedIFC.objects.get(
                id=model_id, program_spec__intent__user=request.user
            )
        except GeneratedIFC.DoesNotExist:
            return Response({"error": "Model not found"}, status=404)

        results = {}
        if atype == "qto":
            # Real QTO from IFC (stub data)
            df = pd.DataFrame(
                [
                    {"type": "Wall", "volume": 120.5, "area": 450},
                    {"type": "Slab", "volume": 80.0, "area": 300},
                ]
            )
            results = {
                "quantities": df.groupby("type").sum().to_dict(),
                "total_volume": df["volume"].sum(),
            }

        elif atype == "anomaly_detection":
            volumes = np.random.normal(100, 20, 50).reshape(-1, 1)
            iso = IsolationForest(contamination=0.1)
            preds = iso.fit_predict(volumes)
            anomalies = np.where(preds == -1)[0].tolist()
            results = {"anomalies_count": len(anomalies), "indices": anomalies}

        run = AnalyticsRun.objects.create(
            model=model,
            analytics_type=atype,
            results=results,
            has_anomalies=len(results.get("anomalies_count", [0])) > 0,
        )
        run.generate_report()
        return Response(AnalyticsRunSerializer(run).data)
