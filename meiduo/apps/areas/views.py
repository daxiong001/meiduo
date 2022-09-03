from rest_framework_extensions.cache.mixins import ListCacheResponseMixin, RetrieveCacheResponseMixin, \
    CacheResponseMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from .models import Area

from .serializers import AreaSerializer, SubAreaSerializer


# Create your views here.

class AreaListView(CacheResponseMixin, ReadOnlyModelViewSet):

    def get_queryset(self):
        if self.action == "list":
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AreaSerializer
        else:
            return SubAreaSerializer
