from rest_framework import serializers
from .models import CB22_calibration


class CB22Serializer(serializers.ModelSerializer):
    class Meta:
        model = CB22_calibration
        fields = "__all__"
