from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
# Create your views here.

class AreaListView(GenericViewSet, ListModelMixin):
    queryset =
    serializer_class =