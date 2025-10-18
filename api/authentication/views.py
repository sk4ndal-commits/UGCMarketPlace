from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    RoleSelectionSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    Accepts: email, password, password_confirm, first_name, last_name, gdpr_consent
    Returns: user data and authentication tokens
    """
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            'errors': []
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    API endpoint for user login.
    
    Inherits from SimpleJWT's TokenObtainPairView.
    Accepts: email (as username), password
    Returns: access and refresh tokens
    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Override to ensure email is used as username
        data = request.data.copy()
        if 'email' in data and 'username' not in data:
            data['username'] = data['email']
        
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            # Get user info
            email = data.get('username') or data.get('email')
            user = User.objects.get(email=email)
            
            return Response({
                'status': 'success',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': serializer.validated_data,
                },
                'errors': []
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': {},
                'errors': [str(e)]
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    API endpoint for user logout.
    
    Blacklists the refresh token to invalidate it.
    Accepts: refresh token
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'status': 'error',
                    'data': {},
                    'errors': [_('Refresh token is required.')]
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'status': 'success',
                'data': {'message': _('Successfully logged out.')},
                'errors': []
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': {},
                'errors': [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)


class RoleSelectionView(APIView):
    """
    API endpoint for role selection on first login.
    
    Accepts: role (BRAND or INFLUENCER)
    Updates the user's role field.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = RoleSelectionSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            user.role = serializer.validated_data['role']
            user.save()
            
            return Response({
                'status': 'success',
                'data': {
                    'user': UserSerializer(user).data,
                    'message': _('Role updated successfully.')
                },
                'errors': []
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get and update current user data.
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': {'user': serializer.data},
            'errors': []
        })


class PasswordResetRequestView(APIView):
    """
    API endpoint to request password reset.
    
    Sends password reset email with token.
    Accepts: email
    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # In a real application, you'd send this via email
                # For now, we'll just return it in the response (development only)
                reset_link = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/reset-password/{uid}/{token}/"
                
                # Send email (currently using console backend for development)
                subject = _('Password Reset Request')
                message = render_to_string('authentication/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
            except User.DoesNotExist:
                # Don't reveal if email exists (security best practice)
                pass
            
            return Response({
                'status': 'success',
                'data': {
                    'message': _('If an account with this email exists, a password reset link has been sent.')
                },
                'errors': []
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    API endpoint to confirm password reset with token.
    
    Accepts: uid, token, password, password_confirm
    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Decode uid to get user
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)
                
                # Verify token
                if not default_token_generator.check_token(user, token):
                    return Response({
                        'status': 'error',
                        'data': {},
                        'errors': [_('Invalid or expired reset link.')]
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Set new password
                user.set_password(serializer.validated_data['password'])
                user.save()
                
                return Response({
                    'status': 'success',
                    'data': {
                        'message': _('Password has been reset successfully.')
                    },
                    'errors': []
                }, status=status.HTTP_200_OK)
                
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({
                    'status': 'error',
                    'data': {},
                    'errors': [_('Invalid reset link.')]
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    API endpoint for authenticated users to change their password.
    
    Accepts: old_password, new_password, new_password_confirm
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'status': 'success',
                'data': {
                    'message': _('Password changed successfully.')
                },
                'errors': []
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserDataView(APIView):
    """
    API endpoint for GDPR-compliant user data deletion.
    
    Allows authenticated users to delete their account and data.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        email = user.email
        
        # Call the GDPR-compliant deletion method
        user.delete_user_data()
        
        return Response({
            'status': 'success',
            'data': {
                'message': _(f'Account {email} and associated data have been deleted.')
            },
            'errors': []
        }, status=status.HTTP_200_OK)
