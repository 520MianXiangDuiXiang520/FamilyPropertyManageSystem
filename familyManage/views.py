from FamilyPropertyMS.util.Permission import ParentPermission
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from FamilyPropertyMS.util.Tool import send_message, response_detail
from userManage.models import User
from .models import Family, FamilyMembers, Application

# Create your views here.


class FamilyManageView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        # create new family
        family_name = request.POST.get('family_name')
        # 判断该用户能不能创建家庭（每个人只能加入一个家庭）
        if request.user.family1:
            return JsonResponse(response_detail(460, "每人只能加入一个家庭"))
        try:
            family_from_db = Family.objects.filter(
                family_name=family_name)
        except:
            return JsonResponse(response_detail(500))
        # if family_from_db:
        #     msg = CODE[400]
        #     msg['msg'] = "家庭名重复"
        #     return JsonResponse(msg)
        try:
            parent1 = User.objects.get(id=request.user.id)
            new_family_member = FamilyMembers(parent1=parent1)
            new_family_member.save()
            new_family = Family(family_name=family_name,
                                family_member=new_family_member)
            new_family.save()
            parent1.family1 = new_family
            parent1.save()
            return JsonResponse(response_detail(200))
        except:
            return JsonResponse(response_detail(500))

    # 查看家庭信息
    @staticmethod
    def get(request, *args, **kwargs):
        family_info = {'family': 'null'}
        family = request.user.family1
        if family:
            family_info = family.toString()
        ret = response_detail(200)
        print(family_info)
        ret.update(family_info)
        return JsonResponse(ret, safe=False)


class MemberManageView(APIView):
    # 家长权限
    permission_classes = [ParentPermission]

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
        need_fields = ['parent_id', 'user_id', 'is_agree']
        PUT = QueryDict(request.body)
        put_data = PUT.dict()
        for field in need_fields:
            if not put_data.get(field):
                return JsonResponse(response_detail(400, "您传递的数据不符合接口要求"))
            if field == 'is_agree':
                if put_data.get(field) not in ['0', '1']:
                    return JsonResponse(response_detail(400, "您只能选择同意或不同意"))
        child = User.objects.get(id=int(put_data.get('user_id')))
        # 根据家长ID找到家庭
        try:
            fm = User.objects.filter(id=int(put_data.get('parent_id'))).first().family1.family_member
        except TypeError:
            # 正常从前端界面发请求不会触发
            return JsonResponse(response_detail(400, "没有这个家庭"))
        the_family = User.objects.get(id=int(put_data.get('parent_id'))).family1
        if put_data.get('is_agree') == '1':
            send_message(request.user, child, "申请失败",
                         f"{request.user.username} 不同意你加入家庭{the_family.family_name}.", 1)
            return JsonResponse(response_detail(200))
        get_application = Application.objects.filter(applicant=child,
                                                     interviewer=request.user).first()
        if not get_application:
            return JsonResponse(response_detail(400, "该用户从来没发起过请求"))
        for m in member_list:
            m_value = getattr(fm, m)
            # 将家庭加入到成员家庭项目中
            if child.family1:
                return JsonResponse(response_detail(460, "只能加入一个家庭"))
            # 将新成员加入到家庭成员表中
            # TODO：判断新成员是不是在家庭中了
            if m_value is None:
                setattr(fm, m, child)
                fm.save()
                child.family1 = the_family
                child.save()
                send_message(request.user, child, "加入成功",
                             "{request.user.username} 同意你加入家庭{the_family.family_name}.", 1)
                get_application.delete()
                return JsonResponse(response_detail(200))



