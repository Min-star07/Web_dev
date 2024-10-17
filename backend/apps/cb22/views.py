from rest_framework import generics
from .models import CB22_calibration
from .serializers import CB22Serializer
from .paginations import ListPagination
import json
import pandas as pd
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http.response import HttpResponse
from rest_framework import mixins
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework.response import Response


class CB22View(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = CB22_calibration.objects.all()
    serializer_class = CB22Serializer
    pagination_class = ListPagination

    def get_queryset(self):
        wall = self.request.query_params.get("WALL")
        cb = self.request.query_params.get("CB")
        rob = self.request.query_params.get("ROB")
        channel = self.request.query_params.get("Channel")
        queryset = self.queryset

        if wall:
            queryset = queryset.filter(WALL=wall)
        if cb:
            queryset = queryset.filter(CB=cb)
        if rob:
            queryset = queryset.filter(ROB=rob)
        if channel:
            queryset = queryset.filter(Channel=channel)
        # print(queryset)
        return queryset


# class ListDownloadView(APIView):
#     def get(self, request):
#         pks = request.query_params.get("pks")
#         print(pks)
#         try:
#             pks = json.loads(pks)
#         except Exception:
#             return Response(
#                 {"detail": "parameters result wrong"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             queryset = CB22_calibration.objects.filter(pk__in=pks)
#             result = queryset.values("WALL", "CB", "ROB", "Channel", "HV")
#             result_df = pd.DataFrame(list(result))

#             response = HttpResponse(
#                 content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#             )
#             response["Content-Disposition"] = "attachment; filename=test.xlsx"

#             with pd.ExcelWriter(response) as writer:
#                 result_df.to_excel(writer, sheet_name="test")
#             return response
#         except Exception as e:
#             print(e)
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListDownloadView(APIView):
    def get(self, request):
        pks = request.query_params.get("pks")
        # print(pks)

        # Parse and validate the "pks" parameter
        try:
            pks = json.loads(pks)
        except Exception:
            return Response(
                {"detail": "parameters result wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter the queryset based on the primary keys (pks)
        try:
            queryset = CB22_calibration.objects.filter(pk__in=pks)
            result = queryset.values("WALL", "CB", "ROB", "Channel", "HV")
            result_df = pd.DataFrame(list(result))

            # Prepare the response for CSV download
            response = HttpResponse(
                content_type="text/csv",
            )
            response["Content-Disposition"] = (
                "attachment; filename=calibration_data.csv"
            )

            # Write the DataFrame to CSV
            result_df.to_csv(path_or_buf=response, index=False)

            return response
        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
