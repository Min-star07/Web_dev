from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("testresult", views.LastedAllresult.as_view(), name="testresult"),
    path("chartq1", views.ChartQ1.as_view(), name="chartq1"),
    path("chartgain", views.ChartAbsGain.as_view(), name="chartgain"),
]
