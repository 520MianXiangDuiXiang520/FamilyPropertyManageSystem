from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from messageManage.models import Message
from FamilyPropertyMS.util.ResponseCode import CODE
from userManage.models import User
from .models import Family, FamilyMembers, Application

# Create your views here.


class FamilyManageView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        # create new family
        family_name = request.POST.get('family_name')
        # 判断该用户能不能创建家庭（每个人只能加入两个家庭）
        if request.user.family1 and request.user.family2:
            return JsonResponse(CODE[460])
        try:
            family_from_db = Family.objects.filter(
                family_name=family_name)
        except:
            return JsonResponse(CODE[500])
        if family_from_db:
            msg = CODE[400]
            msg['msg'] = "家庭名重复"
            return JsonResponse(msg)
        try:
            parent1 = User.objects.get(id=request.user.id)
            new_family_member = FamilyMembers(parent1=parent1)
            new_family_member.save()
            new_family = Family(family_name=family_name,
                                family_member=new_family_member)
            new_family.save()
            parent1.family1 = new_family
            parent1.save()
            return JsonResponse(CODE[200])
        except:
            return JsonResponse(CODE[500])

    # 查看家庭信息
    @staticmethod
    def get(request, *args, **kwargs):
        # delete family
        return JsonResponse("pass", safe=False)


class MemberManageView(APIView):
    # TODO ：需要家长权限
    @staticmethod
    def post(request, *args, **kwargs):
        # 家长邀请新成员
        # 1. post过来一个家庭id，家长id， 要邀请的成员id
        # 2. 检查家庭是否满员
        # 3. 检查成员是否存在
        # 4. 给成员发消息
        # 5. 存入数据库（成员id， 家庭id， 家长id， 时间）
        return JsonResponse("pass", safe=False)

    @staticmethod
    def put(request, *args, **kwargs):
        """
        家长审核请求加入的成员
        1. 检查put过来的数据中有没有（家庭id，成员id，时间，是否同意）
        2. 如果同意，发消息给成员(0同意，1不同意)
        3. 加入家庭表
        4. 不同意法消息给成员
        TODO: 校验请求时间也先不写了，命没了
        TODO： 目前是明文传输，前端需要加密（添加校验字段），后端解密
        """
        member_list = ['members3', 'members4',
                       'members5', 'members6', 'members7', 'members8']
        need_fields = ['family_id', 'child_id', 'is_agree']
        PUT = QueryDict(request.body)
        put_data = PUT.dict()
        for field in need_fields:
            if not put_data.get(field):
                return JsonResponse(CODE[400])
            if field == 'is_agree':
                if put_data.get(field) not in ['0', '1']:
                    return JsonResponse(CODE[400])
        child = User.objects.get(id=int(put_data.get('child_id')))
        fm = FamilyMembers.objects.filter(id=int(put_data.get('family_id'))).first()
        the_family = Family.objects.get(id=int(put_data.get('family_id')))
        if not fm:
            return JsonResponse(CODE[500])
        if put_data.get('is_agree') == '1':
            new_message = Message(send=request.user,
                                  receive=child,
                                  title="申请失败！",
                                  text=f"{request.user.username} 不同意你加入家庭 "
                                       f"{the_family.family_name}.")
            new_message.save()
            return JsonResponse(CODE[200])
        get_application = Application.objects.filter(applicant=child,
                                                     interviewer=request.user).first()
        if not get_application:
            return JsonResponse(CODE[418])
        for m in member_list:
            m_value = getattr(fm, m)
            if m_value is None:
                setattr(fm, m, child)
                fm.save()
                new_message = Message(send=request.user,
                                      receive=child,
                                      title="加入成功！",
                                      text=f"{request.user.username} 同意你加入家庭 "
                                           f"{the_family.family_name}.")
                new_message.save()
                return JsonResponse(CODE[200])



