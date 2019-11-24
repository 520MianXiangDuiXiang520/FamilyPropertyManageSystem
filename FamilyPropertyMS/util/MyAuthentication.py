import pytz
from rest_framework.exceptions import APIException
from rest_framework.authentication import BaseAuthentication
from userManage import models
import datetime


class MyAuthentication(BaseAuthentication):
    @staticmethod
    def _timeout_judgment(token_field):
        delta = (datetime.datetime.now(tz=pytz.timezone('UTC')).replace(tzinfo=pytz.timezone('UTC'))
                 - token_field.create_time.replace(tzinfo=pytz.timezone('UTC')))
        return delta.seconds < 60 * 15

    @staticmethod
    def _delete_token(token_field):
        token_field.delete()

    def authenticate(self, request):
        token = request.GET.get('token')
        token_field = models.UserToken.objects.filter(token=token).first()
        if not token_field:
            raise APIException("认证失败(no token)")
        else:
            if not self._timeout_judgment(token_field):
                self._delete_token(token_field)
                raise APIException("认证失败(token timeout)")
            user = models.User.objects.filter(id=token_field.user_id).first()
            print(datetime.datetime.now(tz=pytz.timezone('UTC')))
            token_field.create_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
            token_field.save()
        return user, token_field
