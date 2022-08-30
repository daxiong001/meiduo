from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData

from . import constants
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    重写jwt登陆试图的构造响应函数，追加user_id和username
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        "token": token,
        "user_id": user.id,
        "username": user.username
    }


def get_user_by_account(account):
    """
    通过传入的账号动态获取user模型对象
    :param account: 可能是手机号也可能是用户名
    :return: user或none
    """
    query = User.objects.filter(Q(username=account) | Q(mobile=account))
    if len(query) > 0:
        return query[0]
    else:
        return None


class UserNameMobileAuthBackend(ModelBackend):
    """重写django认证类中的认证方法，兼容多种登陆方式"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user


def generate_email_verify_url(user):
    """生成邮箱激活链接"""
    serializer = TJWSSerializer(settings.SECRET_KEY, constants.DEFAULT_EXPIRES_IN)

    data = {"user_id": user.id, "email": user.email}
    token = serializer.dumps(data).decode()

    return 'http://127.0.0.1:8080/success_verify_email.html?token=' + token


def check_verify_email(token):
    """解析token并查询对应的user"""
    serializer = TJWSSerializer(settings.SECRET_KEY, constants.DEFAULT_EXPIRES_IN)

    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get("user_id")
        email = data.get("email")
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user
