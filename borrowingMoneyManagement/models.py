from django.db import models
from userManage.models import User
# Create your models here.


class BorrowMoneyTable(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="ID")
    STATUS = [(0, "未处理"), (1, "已发款"), (2, "已还款")]
    borrower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="borrower", db_column="借款人")
    lender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="lender", db_column="发借人")
    money = models.IntegerField(db_column="金额")
    date = models.DateField(auto_now_add=True, null=True, db_column="借款时间")
    repayment_date = models.DateField(null=True, db_column="还款时间")
    status = models.SmallIntegerField(choices=STATUS, default=0, db_column="状态")

    class Meta:
        db_table = '借还钱管理表'
