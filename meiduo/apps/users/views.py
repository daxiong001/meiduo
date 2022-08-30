from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from . import serializers
from .models import User
# Create your views here.
from .serializers import UserAddSerializer, UserDetailSerializer, UserEmailSerializer
from .utils import check_verify_email


class UserView(GenericViewSet, CreateModelMixin):
    """"用户注册"""
    serializer_class = UserAddSerializer
    queryset = User.objects.all()


@permission_classes((IsAuthenticated,))
class UserDetailView(GenericViewSet, RetrieveModelMixin):
    """用户详细信息"""
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        return self.request.user


@permission_classes((IsAuthenticated,))
class UserEmailView(GenericViewSet, UpdateModelMixin):
    serializer_class = UserEmailSerializer

    def get_object(self):
        return self.request.user


class EmailVerifyView(APIView):
    """激活用户邮箱"""

    def get(self, request):
        token = request.query_params.get("token")
        user = check_verify_email(token)
        if user is None:
            return Response({"message": "激活失败"}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = 1
        user.save()
        return Response({"message": "ok"})
