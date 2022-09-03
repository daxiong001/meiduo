from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
# router.register("sku", views.SKUListView, basename="goodsList")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:category_id>/sku/", views.SKUListView.as_view(actions={"get": "list"})),
    path("<int:category_id>/list/", views.CategoryView.as_view(actions={"get": "list"})),
]
