from django.urls import path

from meiduo.apps.oauth import views

urlpatterns = [
    path('authorize/', views.WeiBoOauthURLView.as_view()),
    path('user/', views.WeiBoAuthUserView.as_view()),
]