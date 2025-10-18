from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    RoleSelectionView,
    CurrentUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordChangeView,
    DeleteUserDataView,
)

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('role/', RoleSelectionView.as_view(), name='role_selection'),
    
    # Password management
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    
    # GDPR compliance
    path('delete/', DeleteUserDataView.as_view(), name='delete_user_data'),
]
