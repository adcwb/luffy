from . import models
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, user=None, request=None):
    # print('>>>>>',user,type(user))

    return {
        'token': token,
        'username': user.username,
        'id': user.id
    }


def get_user_obj(accout):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        user_obj = models.User.objects.get(Q(username=accout) | Q(phone=accout))
    except:
        return None
    return user_obj


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_obj = get_user_obj(username)
        if user_obj:
            if user_obj.check_password(password):
                return user_obj

        else:
            return None
