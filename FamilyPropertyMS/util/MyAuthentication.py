import pytz
from rest_framework.exceptions import APIException
from rest_framework.authentication import BaseAuthentication
from .Tool import timeout_judgment
from userManage import models
import datetime


class MyAuthentication(BaseAuthentication):
    @staticmethod
    def _delete_token(token_field):
        token_field.delete()

    def authenticate(self, request):
        token = request.GET.get('token')
        token_field = models.UserToken.objects.filter(token=token).first()
        if not token_field:
            raise APIException("认证失败(no token)")
        else:
            if timeout_judgment(token_field, 'create_time', '15/m'):
                self._delete_token(token_field)
                raise APIException("认证失败(token timeout)")
            user = models.User.objects.filter(id=token_field.user_id).first()
            print(datetime.datetime.now(tz=pytz.timezone('UTC')))
            token_field.create_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
            token_field.save()
        return user, token_field
