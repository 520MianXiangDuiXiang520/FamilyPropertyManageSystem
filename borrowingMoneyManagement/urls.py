from django.urls import path
from .views import BorrowingMoneyManagementView

urlpatterns = [
    path('borrow/', BorrowingMoneyManagementView.as_view())
    ]