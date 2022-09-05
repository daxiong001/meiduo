from django.urls import path, include
from rest_framework.routers import SimpleRouter

from meiduo.apps.carts import views

router = SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("cart/", views.CartView.as_view())
]
