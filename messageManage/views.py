import datetime

import pytz
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from FamilyPropertyMS.util.ResponseCode import CODE
from userManage.models import User
from .models import Message


# Create your views here.


class MessageView(APIView):

    @staticmethod
    def _delete_overtime_message(message):
        delta = datetime.datetime.now(tz=pytz.timezone('UTC')).replace(tzinfo=pytz.timezone('UTC')) -\
                message['send_time'].replace(tzinfo=pytz.timezone('UTC'))
        print(delta.seconds)
        return delta.seconds > 60 * 60 * 24

    def get(self, request, *args, **kwargs):
        # 获得消息列表
        messages = Message.objects.filter(receive__id=request.user.id)
        message_list = []
        for i in messages.values():
            if self._delete_overtime_message(i) and i['state'] == 2:
                field = Message.objects.get(i['id'])
                field.delete()
            i['send_id'] = User.objects.get(id=i['send_id']).username
            i['receive_id'] = User.objects.get(id=i['receive_id']).username
            message_list.append(i)
        return JsonResponse(message_list, safe=False)

    @staticmethod
    def delete(request, *args, **kwargs):
        # 删除消息
        DELETE = QueryDict(request.body)
        message_id = DELETE.get('id')
        print(message_id)
        try:
            prepare_delete_mes = Message.objects.get(id=message_id)
        except:
            return JsonResponse(CODE[400])
        # 只能删自己的信息
        if request.user.id != prepare_delete_mes.receive_id:
            return JsonResponse(CODE[403])
        prepare_delete_mes.delete()
        return JsonResponse(CODE[200], safe=False)

    @staticmethod
    def post(request, *args, **kwargs):
        # 发送消息
        receive = request.POST.get('receive')
        title = request.POST.get('title')
        text = request.POST.get('text')
        try:
            receive_id = User.objects.get(username=receive)
        except Exception:
            return JsonResponse(CODE[400])
        try:
            new_message = Message(send=request.user, receive=receive_id, title=title, text=text)
            new_message.save()
        except Exception:
            return JsonResponse(CODE[500])
        return JsonResponse(CODE[200], safe=False)

    @staticmethod
    def put(request, *args, **kwargs):
        # 修改消息状态为已读或者星标
        PUT = QueryDict(request.body)
        message_id = PUT.get('id')
        message_state = int(PUT.get('state'))
        try:
            message = Message.objects.get(id=message_id)
        except:
            return JsonResponse(CODE[400])
        if message_state not in (1, 2):
            return JsonResponse(CODE[403])
        try:
            message.state = message_state
            message.save()
        except:
            return JsonResponse(CODE[500])
        return JsonResponse(CODE[200])

