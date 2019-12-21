from rest_framework import serializers
from .models import BorrowMoneyTable


class BorrowSerializer(serializers.ModelSerializer):
    borrower = serializers.CharField(source='borrower.username')
    lender = serializers.CharField(source='lender.username')
    lender_id = serializers.CharField(source='lender.id')
    status = serializers.CharField(source='get_status_display')
    deadline = serializers.SerializerMethodField()

    def get_deadline(self, row):
        return row.date.strftime('%Y-%m-%d')

    class Meta:
        model = BorrowMoneyTable
        fields = ['id', 'money', 'deadline', 'borrower', 'status', 'lender', 'lender_id']
