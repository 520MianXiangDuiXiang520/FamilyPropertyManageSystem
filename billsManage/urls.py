from django.urls import path
from . import views

urlpatterns = [
    # 收入
    path('Income/', views.IncomeView.as_view()),
    # path('familyMember/', views.MemberManageView.as_view())
]