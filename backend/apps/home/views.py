import logging
from django.http.response import JsonResponse
from apps.cb22.models import CB22_calibration
from apps.cb22.serializers import CB22Serializer
from rest_framework.views import APIView
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np

# Set up logger
logger = logging.getLogger(__name__)


class LastedAllresult(APIView):
    serializer_class = CB22Serializer

    def get_queryset(self):
        queryset = CB22_calibration.objects.all()

        # Filtering logic based on query parameters
        wall = self.request.query_params.get("WALL")
        cb = self.request.query_params.get("CB")
        rob = self.request.query_params.get("ROB")
        channel = self.request.query_params.get("Channel")

        if wall:
            queryset = queryset.filter(WALL=wall)
        if cb:
            queryset = queryset.filter(CB=cb)
        if rob:
            queryset = queryset.filter(ROB=rob)
        if channel:
            queryset = queryset.filter(Channel=channel)

        logger.debug(
            f"Filtered QuerySet: {queryset.query}"
        )  # Log the actual SQL query for debugging
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CB22Serializer(queryset, many=True)
        logger.debug(f"Serialized Data: {serializer.data}")
        return JsonResponse(serializer.data, safe=False)


class ChartBase(APIView):
    """Base class for generating charts to avoid code duplication."""

    def get_filtered_queryset(self):
        """Filter the queryset based on the request parameters."""
        queryset = CB22_calibration.objects.all()

        wall = self.request.query_params.get("WALL")
        cb = self.request.query_params.get("CB")
        rob = self.request.query_params.get("ROB")
        channel = self.request.query_params.get("Channel")

        if wall:
            queryset = queryset.filter(WALL=wall)
        if cb:
            queryset = queryset.filter(CB=cb)
        if rob:
            queryset = queryset.filter(ROB=rob)
        if channel:
            queryset = queryset.filter(Channel=channel)

        logger.debug(
            f"Filtered QuerySet for chart: {queryset.query}"
        )  # Log the actual SQL query for debugging
        return queryset

    def generate_histogram(self, data, xlabel, title, label):
        """Generates and returns a histogram plot."""
        fig, ax = plt.subplots()
        y_min, y_max = np.min(data), np.max(data)
        y_mean, y_std = np.mean(data), np.std(data)

        # Determine histogram range
        lower = y_min - (y_max - y_min)
        upper = y_max + (y_max - y_min)

        bins = 30
        ax.hist(
            data,
            range=[lower, upper],
            bins=bins,
            label=f"{label}: mean = {y_mean:.2f}, std = {y_std:.2f}",
        )
        ax.set_title(title, fontsize=14)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Count")
        plt.legend()

        # Save to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)  # Rewind the buffer to the beginning
        plt.close(fig)  # Close the figure to free up memory
        return buffer


class ChartQ1(ChartBase):
    """Chart for Q1 distribution."""

    def get(self, request):
        try:
            queryset = self.get_filtered_queryset()
            serializer = CB22Serializer(queryset, many=True)
            calibration_data = serializer.data

            # Extract Q1 values and filter None
            q_values = [
                float(item.get("Q1"))
                for item in calibration_data
                if item.get("Q1") is not None
            ]

            if not q_values:  # Check if q_values is empty
                logger.warning("No Q1 values found.")
                return JsonResponse({"error": "No Q1 values available."}, status=404)

            buffer = self.generate_histogram(q_values, "Q1", "Q1 Distribution", "Q1")
            return HttpResponse(buffer.getvalue(), content_type="image/png")

        except Exception as e:
            logger.error("Error generating Q1 chart: %s", str(e))
            return JsonResponse({"error": "Error generating Q1 chart."}, status=500)


class ChartAbsGain(ChartBase):
    """Chart for absolute gain distribution."""

    def get(self, request):
        try:
            queryset = self.get_filtered_queryset()
            serializer = CB22Serializer(queryset, many=True)
            calibration_data = serializer.data

            # Extract gain values and filter None
            gain_values = [
                float(item.get("gain"))
                for item in calibration_data
                if item.get("gain") is not None
            ]

            if not gain_values:  # Check if gain_values is empty
                logger.warning("No gain values found.")
                return JsonResponse({"error": "No gain values available."}, status=404)

            buffer = self.generate_histogram(
                gain_values, "Gain", "Absolute Gain Distribution", "abs.Gain"
            )
            return HttpResponse(buffer.getvalue(), content_type="image/png")

        except Exception as e:
            logger.error("Error generating absolute gain chart: %s", str(e))
            return JsonResponse(
                {"error": "Error generating absolute gain chart."}, status=500
            )
