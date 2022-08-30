from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData


def generate_save_user_token(openid):
    """对openid加密"""
    serializer = TJWSSerializer(settings.SECRET_KEY, 600)

    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()


def check_save_user_token(access_token):
    """传入加密的openid进行解密并返回"""
    serializer = TJWSSerializer(settings.SECRET_KEY, 600)

    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        return data.get('openid')
