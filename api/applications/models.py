from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import secrets
import string


def generate_application_id():
    """Generate a unique application ID with format app_XXXXXX."""
    chars = string.ascii_lowercase + string.digits
    random_part = ''.join(secrets.choice(chars) for _ in range(6))
    return f'app_{random_part}'


class Template(models.Model):
    """Template model for application templates."""
    
    template_id = models.CharField(
        _('template ID'),
        max_length=50,
        unique=True,
        help_text=_('Unique template identifier (e.g., tpl-react-spa-01)')
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        help_text=_('Template name')
    )
    description = models.TextField(
        _('description'),
        help_text=_('Template description')
    )
    is_available = models.BooleanField(
        _('is available'),
        default=True,
        help_text=_('Whether this template is available for use')
    )
    default_parameters = models.JSONField(
        _('default parameters'),
        default=dict,
        blank=True,
        help_text=_('Default parameters for this template')
    )
    required_parameters = models.JSONField(
        _('required parameters'),
        default=list,
        blank=True,
        help_text=_('List of required parameter names')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.template_id})"
    
    def validate_parameters(self, parameters):
        """Validate that all required parameters are provided."""
        if not parameters:
            parameters = {}
        
        missing_params = [
            param for param in self.required_parameters
            if param not in parameters
        ]
        
        if missing_params:
            raise ValidationError(
                f"Missing required parameters: {', '.join(missing_params)}"
            )
        return True


class Application(models.Model):
    """Application model for creator applications."""
    
    class Visibility(models.TextChoices):
        PUBLIC = 'PUBLIC', _('Public')
        INTERNAL = 'INTERNAL', _('Internal')
        PRIVATE = 'PRIVATE', _('Private')
    
    # Basic fields
    application_id = models.CharField(
        _('application ID'),
        max_length=50,
        unique=True,
        default=generate_application_id,
        help_text=_('Unique application identifier')
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        unique=True,
        help_text=_('Application name (must be unique)')
    )
    description = models.TextField(
        _('description'),
        help_text=_('Application description')
    )
    owner = models.CharField(
        _('owner'),
        max_length=200,
        help_text=_('Application owner (e.g., team name)')
    )
    visibility = models.CharField(
        _('visibility'),
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.INTERNAL,
        help_text=_('Application visibility level')
    )
    
    # Template and configuration
    template = models.ForeignKey(
        Template,
        on_delete=models.PROTECT,
        related_name='applications',
        null=True,
        blank=True,
        help_text=_('Template used for this application (optional)')
    )
    parameters = models.JSONField(
        _('parameters'),
        default=dict,
        blank=True,
        help_text=_('Application parameters and configuration')
    )
    
    # Integrations (optional)
    git_integration = models.JSONField(
        _('Git integration'),
        default=dict,
        blank=True,
        help_text=_('Git integration configuration (repository URL, branch, etc.)')
    )
    oidc_integration = models.JSONField(
        _('OIDC integration'),
        default=dict,
        blank=True,
        help_text=_('OIDC integration configuration (provider, client ID, etc.)')
    )
    
    # Creator relationship
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_applications',
        limit_choices_to={'role': 'CREATOR'},
        help_text=_('Creator who created this application')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['creator', '-created_at']),
            models.Index(fields=['visibility']),
            models.Index(fields=['template']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.application_id})"
    
    def clean(self):
        """Validate application constraints."""
        super().clean()
        
        # If template is provided, validate that required parameters are complete
        if self.template:
            try:
                self.template.validate_parameters(self.parameters)
            except ValidationError as e:
                raise ValidationError({'parameters': e.message})
        
        # Validate integrations if provided
        if self.git_integration:
            self._validate_git_integration()
        
        if self.oidc_integration:
            self._validate_oidc_integration()
    
    def _validate_git_integration(self):
        """Validate Git integration configuration."""
        required_fields = ['repository_url']
        missing_fields = [
            field for field in required_fields
            if field not in self.git_integration
        ]
        
        if missing_fields:
            raise ValidationError({
                'git_integration': f"Missing required fields: {', '.join(missing_fields)}"
            })
    
    def _validate_oidc_integration(self):
        """Validate OIDC integration configuration."""
        required_fields = ['provider', 'client_id']
        missing_fields = [
            field for field in required_fields
            if field not in self.oidc_integration
        ]
        
        if missing_fields:
            raise ValidationError({
                'oidc_integration': f"Missing required fields: {', '.join(missing_fields)}"
            })
    
    def save(self, *args, **kwargs):
        """Override save to run clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)
