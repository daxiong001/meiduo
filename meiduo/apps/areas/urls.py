from django.urls import path, include
from rest_framework.routers import SimpleRouter

from meiduo.apps.areas import views

router = SimpleRouter()
router.register("area", views.AreaListView, basename="area")
urlpatterns = [
    path("", include(router.urls))
]