from django.db.models import Count
from django.shortcuts import HttpResponse
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
import uuid
from .models import User, UserToken
from FamilyPropertyMS.util.ResponseCode import CODE
from familyManage.models import Family, Application
from messageManage.models import Message


# Create your views here.
# TODO: 密码需要加密（使用Django原生的加密框架把）
# TODO： 修改密码要作为另一个单独的视图，因为需要确认两遍密码，还要输入原密码

class LoginView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse('login')

    @staticmethod
    def post(request, *args, **kwargs):
        ret = CODE[200]
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username, password=password).first()
            if not user:
                return JsonResponse(CODE[400])
            u4 = uuid.uuid4()  # 生成uuid4
            UserToken.objects.update_or_create(user=user, defaults={'token': u4})
            ret['token'] = u4
            return JsonResponse(ret)
        except Exception:
            return JsonResponse(CODE[400])


class RegisterView(APIView):
    # TODO : 没有密码长度限制
    # TODO ： 密码明文存储
    authentication_classes = []

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            pwdagain = request.POST.get('pwdagain')
        except:
            ret = CODE[400]
            return JsonResponse(ret)
        try:
            user_in_db = User.objects.filter(username=username)
        except:
            ret = CODE[500]
            return JsonResponse(ret)
        if user_in_db:
            ret = CODE[400]
            ret['msg'] = "用户名重复"
            return JsonResponse(ret)
        if password != pwdagain:
            ret = CODE[400]
            ret['msg'] = "两次密码不一致"
            return JsonResponse(ret)
        new_user = User.objects.create(username=username, password=password)
        new_user.save()
        u4 = uuid.uuid4()  # 生成uuid4
        UserToken.objects.update_or_create(user=new_user, defaults={'token': u4})
        ret = CODE[200]
        ret['token'] = u4
        return JsonResponse(ret)


class LogoutView(APIView):

    @staticmethod
    def delete(request, *args, **kwargs):
        DELETE = QueryDict(request.body)
        token = DELETE.get('token')
        try:
            UserToken.objects.get(token=token).delete()
            return JsonResponse(CODE[200])
        except:
            ret = CODE[400]
            ret['msg'] = "登出失败"
            return JsonResponse(ret)


class UserInfoView(APIView):
    scope = 'THROTTLE'
    user_info_matters = [i.name for i in User._meta.fields if i.name != 'password']

    @staticmethod
    def get_user_info(request, *args, **kwargs):
        """
        返回用户信息
        :param request: Request
        :return: dict
        """
        info = {}
        for matter in UserInfoView.user_info_matters:
            info[matter] = getattr(request.user, matter)
        return info

    def get(self, request, *args, **kwargs):
        """
        返回用户信息
        :param request: Request
        :return:
        """
        try:
            info = self.get_user_info(request, *args, **kwargs)
        except AttributeError:
            return JsonResponse(CODE[500])
        return JsonResponse(info, safe=False)

    def put(self, request, *args, **kwargs):
        """
        修改用户个人信息
        :param request: Request
        :return: 新的信息
        """
        PUT = QueryDict(request.body)
        data = PUT.dict()
        for field in data:
            if field in UserInfoView.user_info_matters:
                try:
                    setattr(request.user, field, data[field])
                    request.user.save()
                except:
                    return JsonResponse(CODE[500])
        return JsonResponse(self.get_user_info(request), safe=False)


class AboutFamilyView(APIView):
    @staticmethod
    def _send_message(send: User, receive: User, title: str, text: str, m_type: int):
        """
        发送一条消息
        :param send: 发送者
        :param receive: 接收者
        :param title: 消息标题
        :param text: 消息正文
        :param m_type: 消息类型（0为普通用户消息， 1为系统通知消息， 2为请求确认类消息）
        2类消息在前端渲染时需要渲染一个form
        """
        try:
            new_message = Message(send=send, receive=receive, title=title, text=text, type=m_type)
            new_message.save()
        except:
            return JsonResponse(CODE[500])

    def _notify_all_parents(self, request, family_mumber):
        """
        有请求加入家庭的消息时通知家长，并储存请求信息
        :param request: Request，主要用来获取认证用户身份
        :param family_mumber: QuerySet，主要用来获得家长信息
        """
        # TODO ： 请求信息目前没有时间限制，需要解决，请求最多保持一天

        for parent in [family_mumber.parent1, family_mumber.parent2]:
            if parent is not None:
                self._send_message(request.user, family_mumber.parent1, "加入家庭请求",
                                   f"{request.user.username} 请求加入您的家庭， 是否同意？", 2)
                new_application = Application(applicant=request.user,
                                              interviewer=family_mumber.parent1)
                new_application.save()

    @staticmethod
    def _people_reached_upper_limit_judge(family_mumber):
        """
        一个家庭最多允许加入8个人（算家长）这个方法用来判断家庭人数是否已满
        :param family_mumber: QuerySet, 主要用来获取家庭成员信息，看还有没有空位
        """
        fm_fields = [getattr(family_mumber, f.name)
                     for f in family_mumber._meta.fields if f.name != 'id']
        if None not in fm_fields:
            return JsonResponse(CODE[600])

    def post(self, request, *args, **kwargs):
        """
        普通用户请求加入某个家庭
        :param request: Request
        :return: 200
        """
        family_id = request.POST.get('family_id')
        family = Family.objects.filter(id=family_id).first()
        if not family:
            return JsonResponse(CODE[400])
        self_applicant_num = Application.objects.aggregate(count=Count('applicant'))['count']
        if self_applicant_num >= 2:
            ret = CODE[429]
            ret['msg'] = "只能搞两次"
            return JsonResponse(ret)
        family_mumber = family.family_member
        self._people_reached_upper_limit_judge(family_mumber)
        self._notify_all_parents(request, family_mumber)
        return JsonResponse(CODE[200], safe=False)

    @staticmethod
    def put(request, *args, **kwargs):
        # 成员同意家长的邀请
        # TODO： 解密出 1 的数据（明文传输一个校验字段）
        # 1. 检查put过来的数据中有没有（家长id，家庭id，成员id，时间，是否同意）
        # 2. 如果同意，发消息给家长
        # 3. 加入家庭表
        # 4. 不同意法消息给家长
        return JsonResponse("pass", safe=False)


