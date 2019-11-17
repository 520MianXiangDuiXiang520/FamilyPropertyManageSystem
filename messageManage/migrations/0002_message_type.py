# Generated by Django 2.2.2 on 2019-11-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageManage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.SmallIntegerField(choices=[(0, '普通用户消息'), (1, '系统通知消息'), (2, '申请消息')], db_column='消息类型', default=0),
        ),
    ]
