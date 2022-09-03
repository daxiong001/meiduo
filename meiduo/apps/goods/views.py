from django.contrib.admin.utils import lookup_field
from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import SKU, GoodsCategory

# Create your views here.
from .serializers import SKUSerializer, CategorySerializer
from ...utils.pagination import StandardResultsSetPagination


class SKUListView(GenericViewSet, ListModelMixin):
    """
    商品数据查询
    """
    serializer_class = SKUSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_time', 'price', 'sales']
    # lookup_field = "sku_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return SKU.objects.filter(is_launched=True, category_id=category_id)


class CategoryView(GenericViewSet, ListModelMixin):
    """面包屑"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return GoodsCategory.objects.filter(id=category_id)
