from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from FamilyPropertyMS.util.Tool import response_detail
from userManage.models import User
from .models import Message


# Create your views here.


class MessageView(APIView):

    @staticmethod
    def _get_message(request):
        messages = Message.objects.filter(receive__id=request.user.id)
        message_list = []
        for i in messages.values():
            i['send_id'] = User.objects.get(id=i['send_id']).id
            i['send_name'] = User.objects.get(id=i['send_id']).username
            i['receive_id'] = User.objects.get(id=i['receive_id']).id
            i['receive_name'] = User.objects.get(id=i['receive_id']).username
            message_list.append(i)
        return message_list

    def get(self, request, *args, **kwargs):
        # 获得消息列表
        return JsonResponse(self._get_message(request), safe=False)

    def delete(self, request, *args, **kwargs):
        # 删除消息
        DELETE = QueryDict(request.body)
        message_id = DELETE.get('id')
        try:
            prepare_delete_mes = Message.objects.get(id=message_id)
        except:
            return JsonResponse(response_detail(400))
        # 只能删自己的信息
        if request.user.id != prepare_delete_mes.receive_id:
            return JsonResponse(response_detail(403, "你想上天啊！！"))
        prepare_delete_mes.delete()
        return JsonResponse(self._get_message(request), safe=False)

    def post(self, request, *args, **kwargs):
        # 发送消息
        receive = request.POST.get('receive')
        title = request.POST.get('title')
        text = request.POST.get('text')
        try:
            receive_id = User.objects.get(username=receive)
        except Exception:
            return JsonResponse(response_detail(400))
        try:
            new_message = Message(send=request.user, receive=receive_id, title=title, text=text)
            new_message.save()
        except Exception:
            return JsonResponse(response_detail(500))
        return JsonResponse(self._get_message(request), safe=False)

    def put(self, request, *args, **kwargs):
        # 修改消息状态为已读或者星标
        PUT = QueryDict(request.body)
        message_id = PUT.get('id')
        message_state = int(PUT.get('state'))
        try:
            message = Message.objects.get(id=message_id)
        except:
            return JsonResponse(response_detail(400))
        if message_state not in (0, 1, 2, 3):
            return JsonResponse(response_detail(400, "别搞了！！！"))
        try:
            message.state = message_state
            message.save()
        except:
            return JsonResponse(response_detail(500))
        return JsonResponse(self._get_message(request), safe=False)

