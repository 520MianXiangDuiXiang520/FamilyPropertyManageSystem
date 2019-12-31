from django.shortcuts import HttpResponse
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
import uuid
from FamilyPropertyMS.util import OAuth
from .models import User, UserToken
# from FamilyPropertyMS.util.Tool import timeout_judgment, send_message, response_detail
from FamilyPropertyMS.util.Tool import response_detail
from familyManage.models import Family, Application
import requests
import re


# Create your views here.
# TODO: 密码需要加密（使用Django原生的加密框架把）
# TODO： 修改密码要作为另一个单独的视图，因为需要确认两遍密码，还要输入原密码

class OAuthByGitHub(APIView):
    """
    GitHub第三方登录
    """
    authentication_classes = []

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse(response_detail(400))
        data = {'client_id': OAuth.OAuthByGitHubSetting['client_id'],
                'client_secret': OAuth.OAuthByGitHubSetting['client_secret'],
                'code': code}
        request = requests.post('https://github.com/login/oauth/access_token', data=data).text
        pattern = re.compile(r'^access_token=+[0-9a-zA-Z]+&.+$')
        if not re.match(pattern, request):
            return JsonResponse(response_detail(400, "登录失败！"))
        try:
            token = (request.split("=")[1]).split("&")[0]
        except IndexError:
            return JsonResponse(response_detail(400, "登录失败！"))
        get_user_info = requests.get(f'https://api.github.com/user?access_token={token}').json()
        try:
            username = get_user_info['login']
        except NameError:
            return JsonResponse(response_detail(400, "登录失败！"))
        user = User.objects.filter(username=username).first()
        if not user:
            newOAuthUser = User(username=username, password='password')
            newOAuthUser.save()
            user = newOAuthUser
        u4 = uuid.uuid4()  # 生成uuid4
        UserToken.objects.update_or_create(user=user, defaults={'token': u4})
        return JsonResponse(response_detail(200, data={'token': u4}))


class LoginView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse('login')

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username, password=password).first()
            if not user:
                return JsonResponse(response_detail(400, "用户名或密码错误"))
            u4 = uuid.uuid4()  # 生成uuid4
            UserToken.objects.update_or_create(user=user, defaults={'token': u4})
            ret = response_detail(200)
            ret['token'] = u4
            return JsonResponse(ret)
        except Exception:
            return JsonResponse(response_detail(400))


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
            return JsonResponse(response_detail(400))
        try:
            user_in_db = User.objects.filter(username=username)
        except:
            return JsonResponse(response_detail(500))
        if user_in_db:
            return JsonResponse(response_detail(400, "用户名重复"))
        if password != pwdagain:
            return JsonResponse(response_detail(400, '两次密码不一致'))
        new_user = User.objects.create(username=username, password=password)
        new_user.save()
        u4 = uuid.uuid4()  # 生成uuid4
        UserToken.objects.update_or_create(user=new_user, defaults={'token': u4})
        ret = response_detail(200)
        ret['token'] = u4
        ret.update(new_user.toString())
        return JsonResponse(ret)


class LogoutView(APIView):

    @staticmethod
    def delete(request, *args, **kwargs):
        DELETE = QueryDict(request.body)
        token = DELETE.get('token')
        try:
            UserToken.objects.get(token=token).delete()
            return JsonResponse(response_detail(200))
        except:
            return JsonResponse(response_detail(400, '登出失败'))


class UserInfoView(APIView):
    user_info_matters = [i.name for i in User._meta.fields if i.name != 'password']

    @staticmethod
    def get_user_info(request, *args, **kwargs):
        """
        返回用户信息
        :param request: Request
        :return: dict
        """
        return request.user.toString()

    def get(self, request, *args, **kwargs):
        """
        返回用户信息
        :param request: Request
        :return:
        """
        try:
            info = self.get_user_info(request, *args, **kwargs)
        except AttributeError:
            return JsonResponse(response_detail(500))
        ret = response_detail(200)
        ret.update(info)
        return JsonResponse(ret, safe=False)

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
                if len(data[field]) != 0:
                    try:
                        setattr(request.user, field, data[field])
                        request.user.save()
                    except:
                        return JsonResponse(response_detail(500))
        ret = self.get_user_info(request)
        ret.update(response_detail(200))
        return JsonResponse(ret, safe=False)


class AboutFamilyView(APIView):

    def _notify_all_parents(self, request, family_mumber):
        """
        有请求加入家庭的消息时通知家长，并储存请求信息
        :param request: Request，主要用来获取认证用户身份
        :param family_mumber: QuerySet，主要用来获得家长信息
        """
        # TODO ： 请求信息目前没有时间限制，需要解决，请求最多保持一天

        for parent in [family_mumber.parent1, family_mumber.parent2]:
            if parent is not None:
                send_message(request.user, family_mumber.parent1, "加入家庭请求",
                             f"{request.user.username} (id = {request.user.id}) 请求加入您的家庭， 是否同意？", 2)
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
            return JsonResponse(response_detail(600, "这里人满了"))

    def post(self, request, *args, **kwargs):
        """
        普通用户请求加入某个家庭
        :param request: Request
        :return: 200
        """
        family_id = request.POST.get('family_id')
        family = Family.objects.filter(id=family_id).first()
        if not family:
            return JsonResponse(response_detail(400))
        self_applicant = Application.objects.filter(applicant=request.user).first()
        if self_applicant:
            # 如果用户发起过请求
            if not timeout_judgment(self_applicant, 'start_time', '1/d'):
                return JsonResponse(response_detail(460, "你已经申请过了，明天再来!!!!"), safe=False)
        # 限制一个用户只能加入一个家庭
        if request.user.family1:
            return JsonResponse(response_detail(460, "只能加入一个家庭!!!"))
        family_mumber = family.family_member
        self._people_reached_upper_limit_judge(family_mumber)
        self._notify_all_parents(request, family_mumber)
        return JsonResponse(response_detail(200), safe=False)

    @staticmethod
    def put(request, *args, **kwargs):
        # 成员同意家长的邀请
        # TODO： 解密出 1 的数据（明文传输一个校验字段）
        # 1. 检查put过来的数据中有没有（家长id，家庭id，成员id，时间，是否同意）
        # 2. 如果同意，发消息给家长
        # 3. 加入家庭表
        # 4. 不同意法消息给家长
        return JsonResponse("pass", safe=False)
