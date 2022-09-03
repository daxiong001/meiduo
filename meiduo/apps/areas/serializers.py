from rest_framework.serializers import ModelSerializer

from .models import Area


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = ["id", "name"]


class SubAreaSerializer(ModelSerializer):
    subs = AreaSerializer(many=True)

    class Meta:
        model = Area
        fields = ["id", "name", "subs"]



