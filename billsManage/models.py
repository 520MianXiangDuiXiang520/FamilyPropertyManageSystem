from django.db import models

# Create your models here.
import userManage
from userManage.models import User
from familyManage.models import Family


class UserBills(models.Model):
    # 用户账单
    # 为了方便“银行储蓄管理”和借还钱管理
    # 小于10代表收入的钱（借来的钱也算收入），大于10表示支出的钱（借出去的和存入银行的钱也算支出）
    # “生成资产报告”时可以按type分组查询
    BILL_TYPE = [(0, '收入'), (1, '借来的钱'),  (10, '支出'), (11, '借出去的钱'), (12, '存入银行的钱')]
    id = models.BigAutoField(primary_key=True, db_column="账单ID")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column="用户")
    time = models.DateTimeField(auto_now_add=True, db_column='创建时间')
    money = models.FloatField(db_column="金额")
    type = models.SmallIntegerField(choices=BILL_TYPE, db_column='类型')
    concrete_type = models.CharField(max_length=100, default="其他", db_column='具体类型')
    remarks = models.TextField(max_length=1000, blank=True, null=True, db_column='备注')

    class Meta:
        db_table = '用户账单'


class FamilyBills(models.Model):
    family_id = models.ForeignKey(to=Family, on_delete=models.CASCADE, db_column="家庭ID")
    bills_id = models.ForeignKey(to=UserBills, on_delete=models.CASCADE, db_column='账单号')

    class Meta:
        db_table = '家庭账单'
