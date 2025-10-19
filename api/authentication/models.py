from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email authentication and role selection."""
    
    class Role(models.TextChoices):
        BRAND = 'BRAND', _('Brand')
        INFLUENCER = 'INFLUENCER', _('Influencer')
        CREATOR = 'CREATOR', _('Creator')
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        null=True,
        blank=True,
        help_text=_('User role: Brand or Influencer')
    )
    
    # GDPR compliance fields
    gdpr_consent = models.BooleanField(
        _('GDPR consent'),
        default=False,
        help_text=_('User has consented to data processing')
    )
    gdpr_consent_date = models.DateTimeField(
        _('GDPR consent date'),
        null=True,
        blank=True,
        help_text=_('Date when user gave GDPR consent')
    )
    
    # Influencer profile fields
    followers = models.IntegerField(
        _('followers'),
        null=True,
        blank=True,
        help_text=_('Number of followers/subscribers (for influencers)')
    )
    engagement_rate = models.DecimalField(
        _('engagement rate'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Engagement rate percentage (for influencers)')
    )
    platform = models.CharField(
        _('platform'),
        max_length=50,
        null=True,
        blank=True,
        help_text=_('Primary social media platform (for influencers)')
    )
    
    # Additional fields
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def delete_user_data(self):
        """GDPR-compliant data deletion method."""
        # This method can be extended to handle cascading deletions
        # or anonymization of related data
        self.delete()
