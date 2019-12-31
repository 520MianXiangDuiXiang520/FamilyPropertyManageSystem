from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('user_info/', views.UserInfoView.as_view()),
    # path('about_family/', views.AboutFamilyView.as_view()),
    path('oauth_by_github/', views.OAuthByGitHub.as_view())
]
