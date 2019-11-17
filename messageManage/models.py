from django.db import models
from userManage.models import User


class Message(models.Model):
    STATE = [(0, '未读'), (1, '星标'), (2, '已读')]
    MESSAGE_TYPE = [(0, '普通用户消息'), (1, "系统通知消息"), (2, "申请消息")]
    send = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='send', db_column='发送者')
    receive = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receive', db_column='接收者')
    title = models.CharField(max_length=24, db_column="标题")
    text = models.TextField(max_length=1000, db_column='内容')
    send_time = models.DateTimeField(auto_now_add=True, db_column='发送时间')
    state = models.SmallIntegerField(default=0, choices=STATE, db_column='状态')
    type = models.SmallIntegerField(default=0, choices=MESSAGE_TYPE, db_column='消息类型')

    class Meta:
        db_table = 'MessageDT'