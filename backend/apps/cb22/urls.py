from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "cb22"
router = DefaultRouter(trailing_slash=False)
router.register("cb22", views.CB22View, basename="cb22")

urlpatterns = [
    path("download", views.ListDownloadView.as_view(), name="download"),
] + router.urls
