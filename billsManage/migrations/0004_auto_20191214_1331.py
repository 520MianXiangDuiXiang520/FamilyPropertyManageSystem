# Generated by Django 2.2.2 on 2019-12-14 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billsManage', '0003_auto_20191214_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbills',
            name='remarks',
            field=models.TextField(blank=True, db_column='备注', max_length=1000, null=True),
        ),
    ]
