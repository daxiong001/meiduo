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
# 新增个人地址
router.register("address", views.AddressView, basename="address")
# 保存查看个人浏览商品记录
router.register("history/add", views.UserBrowserHistoryView, basename="history")

urlpatterns = [
    path("", include(router.urls)),
    # JWT登录
    re_path(r"^authorizations/$", obtain_jwt_token),

    # 邮箱激活
    re_path("activation/", views.EmailVerifyView.as_view()),
    # 保存查看个人浏览商品记录
    # path("history/add", views.UserBrowserHistoryView, basename="history")

]
