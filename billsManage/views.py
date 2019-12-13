
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers
from FamilyPropertyMS.util.Tool import response_detail
from .models import UserBills
from .MySerializers import BillsSerializer

from datetime import datetime

# Create your views here.


class ExpendView(APIView):
    # 支出视图
    pass


class IncomeView(APIView):
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

    def post(self, request, *args, **kwargs):
        """
        添加一条收入记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 期望接受到的字段
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
                              type=0, time=field_time, remarks=request.POST['remarks'])
        new_field.save()
        income_bill = UserBills.objects.filter(user=request.user, type=0)
        bills = BillsSerializer(instance=income_bill, many=True)
        result = response_detail(200, data=bills.data)
        return JsonResponse(result)

