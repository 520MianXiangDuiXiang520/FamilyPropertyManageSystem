
from django.urls import path
from . import views


urlpatterns = [
    path('', views.MessageView.as_view())
]