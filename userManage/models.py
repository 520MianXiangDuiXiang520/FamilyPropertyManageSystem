from django.db import models
from familyManage.models import Family 

# Create your models here.


class User(models.Model):
    SEX = [(1, '男'), (2, '女')]
    id = models.BigAutoField(primary_key=True, db_column="用户ID")
    username = models.CharField(max_length=10, blank=False, db_column="用户名")
    password = models.CharField(max_length=64, blank=False, db_column="密码")
    telephone = models.CharField(max_length=11, blank=True, db_column="电话")
    email = models.EmailField(max_length=40, blank=True, db_column="邮箱")
    sex = models.SmallIntegerField(choices=SEX, default=1, db_column="性别")
    family1 = models.ForeignKey(to=Family, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="family1", db_column="家庭1")
    # family2 = models.ForeignKey(to=Family, on_delete=models.SET_NULL,
    #                             null=True, blank=True, related_name="family2", db_column="家庭2")
    
    def toString(self):
        result = {'id': self.id,
                  'username': self.username,
                  'telephone': self.telephone,
                  'email': self.email,
                  'sex': self.email,
                  }
        if self.family1:
            result['family1'] = self.family1.toString()
        return result

    class Meta:
        db_table = '用户表'
    

class UserToken(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    



