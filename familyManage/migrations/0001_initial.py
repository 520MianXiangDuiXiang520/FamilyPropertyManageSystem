# Generated by Django 2.2.2 on 2019-12-13 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userManage', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMembers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('members3', models.ForeignKey(blank=True, db_column='成员3', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members3', to='userManage.User')),
                ('members4', models.ForeignKey(blank=True, db_column='成员4', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members4', to='userManage.User')),
                ('members5', models.ForeignKey(blank=True, db_column='成员5', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members5', to='userManage.User')),
                ('members6', models.ForeignKey(blank=True, db_column='成员6', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members6', to='userManage.User')),
                ('members7', models.ForeignKey(blank=True, db_column='成员7', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members7', to='userManage.User')),
                ('members8', models.ForeignKey(blank=True, db_column='成员8', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members8', to='userManage.User')),
                ('parent1', models.ForeignKey(db_column='家长1', on_delete=django.db.models.deletion.CASCADE, to='userManage.User')),
                ('parent2', models.ForeignKey(blank=True, db_column='家长2', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members2', to='userManage.User')),
            ],
            options={
                'db_table': '家庭成员表',
            },
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(db_column='家庭ID', primary_key=True, serialize=False)),
                ('family_name', models.CharField(db_column='家庭名', max_length=20)),
                ('family_member', models.OneToOneField(db_column='家庭成员', on_delete=django.db.models.deletion.CASCADE, to='familyManage.FamilyMembers')),
            ],
            options={
                'db_table': '家庭表',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, db_column='申请时间')),
                ('applicant', models.ForeignKey(db_column='申请者', on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to='userManage.User')),
                ('interviewer', models.ForeignKey(db_column='审核者', on_delete=django.db.models.deletion.CASCADE, related_name='interviewer', to='userManage.User')),
            ],
        ),
    ]
