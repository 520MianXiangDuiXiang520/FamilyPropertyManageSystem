"""FamilyPropertyMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.generic import TemplateView

from userManage import urls as user_manage_urls
from messageManage import urls as message_url
from familyManage import urls as family_manage_url
from billsManage import urls as bill_manage_url
from borrowingMoneyManagement import urls as borrow_url

urlpatterns = [
    path('api/v1/user_manage/', include(user_manage_urls)),
    path('api/v1/message/', include(message_url)),
    path('api/v1/family/', include(family_manage_url)),
    path('api/v1/bill/', include(bill_manage_url)),
    path('api/v1/borrow_money/', include(borrow_url))
]
