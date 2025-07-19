from django.urls import path
from django.contrib.auth.views import LoginView, TemplateView
from .views import (UserRegisterView, custom_logout, PasswordResetView,
                    ConfirmRegistrationView, PasswordResetRequestView,
                    UsersListView, UsersDetailView, BlockingUsersView,  )

from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', custom_logout, name='logout'),
    path('confirm/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/done/', TemplateView.as_view(template_name='users/password_reset_request.html'), name='password_reset_done'),
    path('reset/<str:token>/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/complete/', TemplateView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('user/', UsersListView.as_view(), name='users_list'),
    path('user/<int:pk>/blocking/', BlockingUsersView.as_view(), name='blocking_user')

]