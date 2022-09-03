from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet


# Create your views here.

class Cart(GenericViewSet, ModelViewSet):
    """购物车增删改查"""
