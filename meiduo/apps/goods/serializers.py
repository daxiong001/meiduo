from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import SKU, GoodsCategory


class SKUSerializer(ModelSerializer):
    class Meta:
        model = SKU
        fields = ["id", "name", "price", "default_image_url", "comments", "category"]


class CategorySerializer(ModelSerializer):
    cat3 = serializers.CharField(source='name')

    class Meta:
        model = GoodsCategory
        fields = ("cat3",)
