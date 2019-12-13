# 定义序列化

from rest_framework import serializers
from .models import UserBills, FamilyBills


class BillsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bill_type = serializers.CharField(source='get_type_display')
    time = serializers.SerializerMethodField()

    def get_time(self, row):
        return row.time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserBills
        fields = ['id', 'remarks', 'money', 'time', 'username', 'bill_type']
