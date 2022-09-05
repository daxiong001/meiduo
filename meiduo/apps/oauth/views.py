import logging

from rest_framework import status

from rest_framework.views import APIView
from weibo_oauth import Weibo
from rest_framework.response import Response
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from .models import OAuthWeiBoUser
from .serializers import WeiBoAuthUserSerializer
from .utils import generate_save_user_token
from ...utils.myresponse import APIResponse

logger = logging.getLogger("django")


class WeiBoOauthURLView(APIView):
    """拼接微博的请求url"""

    def get(self, request):
        # 提取前端传入的next参数记录用户从哪里去到login页面

        # 利用微博登陆工具对象
        oauth = Weibo(app_id=settings.APP_KEY, app_key=settings.APP_SECRET,
                      redirect_uri=settings.REDIRECT_URI)
        login_url = oauth.get_authorize_url()

        return APIResponse({'login_url': login_url})


class WeiBoAuthUserView(APIView):
    """微博登陆成功后的回调处理"""

    def get(self, request):
        # 获取前端传递code
        code = request.query_params.get("code")

        if not code:
            return Response({"message": "获取code失败"}, status=status.HTTP_400_BAD_REQUEST)
        # 创建微博登陆工具对象
        oauth = Weibo(app_id=settings.APP_KEY, app_key=settings.APP_SECRET,
                      redirect_uri=settings.REDIRECT_URI)

        # 调用方法获取access_token
        try:
            data = oauth.get_access_token(code)
            access_token = data.get('access_token')
            weibo_uid = oauth.get_token_uid(access_token)  # 获取到的微博token
        except Exception as e:
            return Response({"message": "调用微博接口异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        existed = OAuthWeiBoUser.objects.filter(openid=weibo_uid).exists()

        if existed:
            userModel = OAuthWeiBoUser.objects.filter(openid=weibo_uid)
            user = userModel[0].user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return APIResponse(
                {
                    'token': token,
                    'username': user.username,
                    'user_id': user.id
                }
            )
        else:
            acc_token_openid = generate_save_user_token(weibo_uid)
            return APIResponse({'access_token': acc_token_openid})

    def post(self, request):
        """openid绑定用户接口"""
        serializer = WeiBoAuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return APIResponse({
            "token": token,
            "username": user.username,
            "user_id": user.id
        })
