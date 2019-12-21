from django.urls import path
from .views import BorrowingView
from .views import PayBackView

urlpatterns = [
    path('borrow/', BorrowingView.as_view()),
    path('payBack/', PayBackView.as_view())
    ]