from django.db import models


# Create your models here.


class Family(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="家庭ID")
    family_name = models.CharField(max_length=20, db_column="家庭名")
    family_member = models.OneToOneField('FamilyMembers', on_delete=models.CASCADE, db_column='家庭成员')

    class Meta:
        db_table = '家庭表'

    def toString(self):
        return {
         'id': self.id,
         'family_name': self.family_name,
         'family_member': self.family_member.toString()
        }


class FamilyMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent1 = models.ForeignKey('userManage.User', on_delete=models.CASCADE, blank=False, db_column='家长1')
    parent2 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="members2", db_column='家长2')
    members3 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members3", db_column='成员3')
    members4 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members4", db_column='成员4')
    members5 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members5", db_column='成员5')
    members6 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members6", db_column='成员6')
    members7 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members7", db_column='成员7')
    members8 = models.ForeignKey('userManage.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="members8", db_column='成员8')

    class Meta:
        db_table = '家庭成员表'

    def toString(self):
        result = {}
        attr_list = ['parent1', 'parent2', 'members3', 'members4', 'members5', 'members6', 'members7', 'members8']
        for i in attr_list:
            if getattr(self, i):
                result[i] = getattr(self, i).username
        return result


class Application(models.Model):
    # 专门用来实现加入家庭或申请加入时的同意认证
    applicant = models.ForeignKey('userManage.User', on_delete=models.CASCADE,
                                  related_name='applicant', db_column="申请者")
    interviewer = models.ForeignKey('userManage.User', on_delete=models.CASCADE,
                                    related_name='interviewer', db_column="审核者")

    start_time = models.DateTimeField(auto_now_add=True, db_column="申请时间")

