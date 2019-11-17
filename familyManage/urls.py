from django.urls import path
from . import views

urlpatterns = [
    path('familyManage/', views.FamilyManageView.as_view()),
    path('familyMember/', views.MemberManageView.as_view())
]