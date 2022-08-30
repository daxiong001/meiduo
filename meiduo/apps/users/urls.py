from django.urls import URLPattern, path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from meiduo.apps.users import views

router = SimpleRouter()
router.register("addUser", views.UserView, basename="addUser")
# 用户详情
router.register("userDetail", views.UserDetailView, basename="userDetail")
# 修改邮箱
router.register("updateEmail", views.UserEmailView, basename="updateEmail")

urlpatterns = [
    path("", include(router.urls)),
    # JWT登录
    re_path(r"^authorizations/$", obtain_jwt_token),

    re_path("activation/", views.EmailVerifyView.as_view())

]
