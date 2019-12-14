from django.urls import path
from . import views

urlpatterns = [
    # 收入
    path('Income/', views.IncomeView.as_view()),
    path('expend/', views.ExpendView.as_view()),
    path('data/', views.StatisticsView.as_view())
]