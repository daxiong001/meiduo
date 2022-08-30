from django_redis import get_redis_connection
from rest_framework import serializers

from .models import OAuthWeiBoUser, User
from .utils import check_save_user_token


class WeiBoAuthUserSerializer(serializers.Serializer):
    """openid绑定用户的序列化器"""
    mobile = serializers.RegexField(help_text="手机号", regex=r'^1[3-9]\d{9}$')
    access_token = serializers.CharField(help_text="操作凭证")
    password = serializers.CharField(max_length=20, min_length=8, help_text="密码")
    sms_code = serializers.CharField(help_text="短信验证码")

    def validate(self, attrs):
        # 取出加密的openid解密
        access_token = attrs.pop("access_token")
        openid = check_save_user_token(access_token)
        if openid is None:
            raise serializers.ValidationError('openid无效')
        attrs["openid"] = openid

        # 校验验证码
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs["mobile"]
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError("验证码错误")

        # 拿手机好吗查询user表， 如果能查到说明手机号已注册，如果已注册再绑定密码是否和用户匹配
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(attrs["password"]) is False:
                raise serializers.ValidationError("密码错误")
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # 获取user并判断用户是否存在
        user = validated_data.get("user")
        if user is None:
            user = User(
                    username=validated_data.get("mobile"),
                    mobile=validated_data.get("mobile")
                    )
            user.set_password(validated_data.get("password"))
            user.save()
        # 如果存在则绑定openid
        OAuthWeiBoUser.objects.create(
            user=user,
            openid=validated_data.get("openid")
        )
        return user

