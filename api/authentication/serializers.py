from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    gdpr_consent = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'gdpr_consent')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate that passwords match and GDPR consent is given."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": _("Password fields didn't match.")
            })
        
        if not attrs.get('gdpr_consent', False):
            raise serializers.ValidationError({
                "gdpr_consent": _("You must consent to data processing to register.")
            })
        
        return attrs
    
    def validate_email(self, value):
        """Validate email is unique and properly formatted."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        return value.lower()
    
    def create(self, validated_data):
        """Create and return a new user."""
        validated_data.pop('password_confirm')
        gdpr_consent = validated_data.pop('gdpr_consent')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            gdpr_consent=gdpr_consent,
            gdpr_consent_date=timezone.now() if gdpr_consent else None
        )
        return user


class RoleSelectionSerializer(serializers.Serializer):
    """Serializer for role selection on first login."""
    
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=True,
        help_text=_("Select your role: Brand or Influencer")
    )
    
    def validate_role(self, value):
        """Ensure role is one of the valid choices."""
        if value not in [User.Role.BRAND, User.Role.INFLUENCER]:
            raise serializers.ValidationError(_("Invalid role selected."))
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role',
            'is_email_verified', 'gdpr_consent', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_email_verified', 'created_at', 'updated_at')


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset."""
    
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Validate that email exists in the system."""
        if not User.objects.filter(email__iexact=value).exists():
            # Return success even if email doesn't exist (security best practice)
            # Don't reveal whether email exists or not
            pass
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset with token."""
    
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": _("Password fields didn't match.")
            })
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing password when authenticated."""
    
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": _("Password fields didn't match.")
            })
        return attrs
    
    def validate_old_password(self, value):
        """Validate that old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is incorrect."))
        return value
