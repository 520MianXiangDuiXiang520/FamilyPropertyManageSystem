from django.http import JsonResponse
from rest_framework.views import APIView
from FamilyPropertyMS.util.Tool import response_detail
from .models import UserBills, FamilyBills
from .MySerializers import BillsSerializer
from abc import abstractmethod
from django.db.models import Sum
from datetime import datetime


class BIllBaseClass:
    @staticmethod
    def statistical_billing_data(request):
        """
        统计账单数据
        1. 统计收入支出总数
        2. 按具体类型统计
        """
        statistical_data = {}
        income_data = []
        expend_data = []
        income_projects = []
        income_money = []
        expend_projects = []
        expend_money = []
        income_bills = UserBills.objects.filter(user=request.user, type=0)
        expend_bills = UserBills.objects.filter(user=request.user, type=10)
        all_income = income_bills.aggregate(Sum("money"))
        all_expend = expend_bills.aggregate(Sum('money'))
        staticmethod_income = income_bills.values('concrete_type').\
            annotate(Sum('money')).values('concrete_type', 'money__sum')
        staticmethod_expend = expend_bills.values('concrete_type').\
            annotate(Sum('money')).values('concrete_type', 'money__sum')

        for i in staticmethod_income:
            income_projects.append(i['concrete_type'])
            income_money.append(i['money__sum'])
        for i in staticmethod_expend:
            expend_projects.append(i['concrete_type'])
            expend_money.append(i['money__sum'])
        overage = all_income['money__sum'] - all_expend['money__sum']
        statistical_data.update({'all_income': all_income['money__sum']})
        statistical_data.update({'all_expend': all_expend['money__sum']})
        statistical_data.update({'overage': overage})
        statistical_data.update({'income_projects': income_projects})
        statistical_data.update({'income_money': income_money})
        statistical_data.update({'expend_projects': expend_projects})
        statistical_data.update({'expend_money': expend_money})
        print(statistical_data)
        return statistical_data

    @abstractmethod
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request):
        bills_type = int(request.POST.get('type'))
        if not bills_type:
            return JsonResponse(response_detail(400, detail="类型缺失"))
        print(bills_type)
        if int(bills_type) not in (0, 1, 10, 11, 12):
            return JsonResponse(response_detail(400, detail="类型错误"))
        need_fields = ['money', 'remarks', 'time']
        for field in need_fields:
            if not request.POST.get(field):
                return JsonResponse(response_detail(400))
        # 判断用户描述是否超出数据库长度限制
        if len(request.POST.get('remarks')) > 1000:
            return JsonResponse(response_detail(400, "长度超出数据库限制"))
        # 判断金额是否超出限制
        if int(request.POST.get('money')) > 9999999:
            return JsonResponse(response_detail(400, "金额超出限制"))
        # 加入到数据库
        try:
            field_time = datetime.strptime(request.POST['time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return JsonResponse(response_detail(400, '时间格式有误，应为 %Y-%m-%d %H:%M:%S'))
        new_field = UserBills(user=request.user, money=request.POST['money'],
                              type=bills_type, time=field_time, remarks=request.POST['remarks'])
        new_field.save()
        # 如果用户有家庭，并且 is_add_to_family = 1， 就把该账单加入到家庭账单
        print(request.user.family1)
        if request.user.family1:
            if int(request.POST.get('is_add_to_family')) == 1:
                new_family_bill = FamilyBills(family_id=request.user.family1, bills_id=new_field)
                new_family_bill.save()
        income_bill = UserBills.objects.filter(user=request.user, type=bills_type)
        bills = BillsSerializer(instance=income_bill, many=True)
        result = response_detail(200, data=bills.data)
        return JsonResponse(result)


class ExpendView(APIView, BIllBaseClass):
    # 支出视图
    def get(self, request, *args, **kwargs):
        income_bill = UserBills.objects.filter(user=request.user, type=10)
        bills = BillsSerializer(instance=income_bill, many=True)
        return JsonResponse(response_detail(200, data=bills.data), safe=False)


class IncomeView(APIView, BIllBaseClass):
    # 收入视图
    def get(self, request, *args, **kwargs):
        """
        查看收入账单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        income_bill = UserBills.objects.filter(user=request.user, type=0)
        bills = BillsSerializer(instance=income_bill, many=True)
        return JsonResponse(bills.data, safe=False)


class StatisticsView(APIView, BIllBaseClass):
    def get(self, request, *args, **kwargs):
        return JsonResponse(response_detail(200, data=self.statistical_billing_data(request)))
