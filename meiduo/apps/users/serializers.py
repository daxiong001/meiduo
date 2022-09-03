import logging
import re
from rest_framework_jwt.settings import api_settings

from django_redis import get_redis_connection
from rest_framework import serializers

from .models import User, Address
from celery_tasks.email.tasks import send_verify_email
from .utils import generate_email_verify_url
from ..goods.models import SKU

logger = logging.getLogger("django")


class UserAddSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, help_text="确认密码")
    sms_code = serializers.CharField(write_only=True, help_text="验证码")
    allow = serializers.CharField(write_only=True, help_text="同意协议")
    token = serializers.CharField(read_only=True, help_text="token")

    class Meta:
        model = User
        fields = ["id", "mobile", "username", "password", "password2", "sms_code", "allow", "token"]
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                "error_messages": {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名'
                },
                "help_text": "用户名"
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                "error_messages": {
                    'min_length': '仅允许8-20个字符的用户名',
                    'max_length': '仅允许8-20个字符的用户名'
                }
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式错误")
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError("请同意用户协议")
        return value

    def validate(self, attrs):

        existed = User.objects.filter(username=attrs["username"]).exists()
        if existed:
            raise serializers.ValidationError("用户名已存在")

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("两次密码不一致")

        # 校验验证码
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs["mobile"]
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        # 向redis中存储数据都是以字符串存储，取出来后都是byte类型
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError("验证码不正确或已过期")
        return attrs

    def create(self, validated_data):
        logger.info(validated_data)
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "mobile", "email", "email_active"]


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        extra_kwargs = {
            "email": {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        """触发发送激活邮箱"""
        instance.email = validated_data['email']
        instance.save()
        verify_url = generate_email_verify_url(instance)
        send_verify_email.delay(instance.email, verify_url=verify_url)

        return instance


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address
        exclude = ["is_deleted", "create_time", "update_time"]
        extra_kwargs = {
            'province': {
                'required': True,
                "error_messages": {
                    'required': '省不能为空',
                },
                "help_text": "地址"
            },
            'city': {
                'required': True,
                "error_messages": {
                    'required': '市不能为空',
                },
                "help_text": "市"
            },
            'district': {
                'required': True,
                "error_messages": {
                    'required': '区不能为空',
                },
                "help_text": "区"
            },
        }


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["title"]


class UserBrowserHistorySerializer(serializers.Serializer):
    sku_id = serializers.IntegerField(help_text="商品sku_id", label="商品sku_id", min_value=1)

    def validate_sku_id(self, value):
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError("sku_id不存在")
        return value

    def create(self, validated_data):
        sku_id = validated_data.get("sku_id")
        user = self.context['request'].user
        redis_conn = get_redis_connection("browser_history")
        pl = redis_conn.pipeline()
        # 去重
        pl.lrem('history_%d' % user.id, 0, sku_id)
        # 添加
        pl.lpush('history_%d' % user.id, sku_id)
        # 截取
        pl.ltrim('history_%d' % user.id, 0, 4)
        pl.execute()
        return validated_data


# class UserHistoryGoodsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SKU
#         fields = ["id", "name", "price", "default_image_url", "comments", "category"]

