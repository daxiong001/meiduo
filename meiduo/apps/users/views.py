from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.decorators import permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from . import serializers
from .models import User, Address
# Create your views here.
from .serializers import UserAddSerializer, AddressSerializer, UserEmailSerializer, TitleSerializer, \
    UserBrowserHistorySerializer
from .utils import check_verify_email
from ..goods.models import SKU
from ..goods.serializers import SKUSerializer


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


@permission_classes((IsAuthenticated,))
class AddressView(ModelViewSet):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(is_deleted=False, user=self.request.user)

    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        count = Address.objects.filter(user=self.request.user, is_deleted=False).count()
        if count > 20:
            return Response({"msg": "地址数量不能超过20条"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        address = self.get_object()
        serializer = TitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["put"], detail=True)
    def status(self, request, pk=None):
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserBrowserHistoryView(GenericViewSet, CreateModelMixin, ListModelMixin):
    """
    用户商品浏览记录
    """

    def get_queryset(self):
        redis_conn = get_redis_connection("browser_history")
        sku_id_set = redis_conn.lrange('history_%s' % self.request.user.id, 0, 4)
        print(sku_id_set)
        queryset = SKU.objects.filter(id__in=sku_id_set)
        # for i in sku_id_set:
        #     queryset = SKU.objects.filter(id= i in sku_id_set)
        #     sku_id.append(queryset)
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return UserBrowserHistorySerializer
        return SKUSerializer
