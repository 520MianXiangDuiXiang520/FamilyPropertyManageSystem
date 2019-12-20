from datetime import datetime
from django.http import JsonResponse, QueryDict
from rest_framework.views import APIView
from FamilyPropertyMS.util.Tool import response_detail, send_message
from .models import BorrowMoneyTable
from userManage.models import User
from billsManage.models import UserBills


class BorrowingMoneyManagementView(APIView):

    def post(self, request, *args, **kwargs):
        """
        发起借钱请求, 需要三个字段（向谁借who, 借多少money，什么时候还pay_back_date）
        """
        need_fields = ('who', 'money', 'pay_back_date')
        for field in need_fields:
            if not request.POST.get(field):
                return JsonResponse(response_detail(400, f"{field}缺失"))
        who = int(request.POST.get('who'))
        money = int(request.POST.get('money'))
        pay_back_date = str(request.POST.get('pay_back_date'))
        try:
            who = User.objects.get(id=who)
        except:
            return JsonResponse(response_detail(400, "请求失败！用户不存在！"))
        if money < 0:
            return JsonResponse(response_detail(400, "请求失败！金额应该大于0"))
        try:
            field_time = datetime.strptime(pay_back_date, '%Y-%m-%d')
            print(field_time)
        except ValueError:
            return JsonResponse(response_detail(400, '时间格式有误，应为 %Y-%m-%d'))

        borrow_field = BorrowMoneyTable(borrower=request.user,
                                        lender=who,
                                        money=money,
                                        repayment_date=field_time,
                                        status=0)
        borrow_field.save()
        send_message(request.user, who, "借钱信息", f"{request.user.username} 想向你借 {money}"
                                                f"块钱，还款时间是: {field_time}, 是否同意？\n记录号：【{borrow_field.id}】", 3)
        return JsonResponse(response_detail(200))

    def put(self, request):
        """
        处理借钱请求，需要两个字段（是否同意【is_agree】 1代表不同意， 0代表同意, 借钱记录号【borrow_id】）
        """
        need_fields = ('is_agree', 'borrow_id')
        PUT = QueryDict(request.body)
        put_data = PUT.dict()
        for field in need_fields:
            if not put_data.get(field):
                return JsonResponse(response_detail(400, f"{field}缺失！"))
        is_agree = int(put_data['is_agree'])
        borrow_id = int(put_data['borrow_id'])
        if is_agree not in (0, 1):
            return JsonResponse(response_detail(400, "参数错误！"))
        try:
            borrow_field = BorrowMoneyTable.objects.filter(id=borrow_id).first()
        except:
            return JsonResponse(response_detail(400, "记录不存在或过期！"))
        if not borrow_field:
            return JsonResponse(response_detail(400, '请求不存在'))
        if borrow_field.status != 0:
            return JsonResponse(response_detail(400, "已处理"))
        if is_agree == 1:
            send_message(request.user, borrow_field.borrower, "借款申请结果",
                         f"{request.user.username} 不同意您的借款申请", 1)
            borrow_field.delete()
            return JsonResponse(response_detail(200))
        send_message(request.user, borrow_field.borrower, "借款申请结果",
                     f"{request.user.username} 同意了您的借款申请", 1)
        bill_lender = UserBills(user=request.user, money=borrow_field.money,
                                type=10, concrete_type="外借",
                                remarks=f"{borrow_field.date} 借给 {borrow_field.borrower.username},"
                                        f" 还款日期： {borrow_field.repayment_date}")
        bill_lender.save()
        bill_borrower = UserBills(user=borrow_field.borrower, money=borrow_field.money,
                                  type=0, concrete_type="借款",
                                  remarks=f"{borrow_field.date} 向 {borrow_field.lender.username} 借的。"
                                          f"还款日期： {borrow_field.repayment_date}")
        bill_borrower.save()
        borrow_field.status = 1
        borrow_field.save()
        return JsonResponse(response_detail(200))
