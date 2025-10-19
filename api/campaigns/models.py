from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_file_size(file):
    """Validate that uploaded file is not larger than 10 MB."""
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')


def campaign_file_upload_path(instance, filename):
    """Generate upload path for campaign reference materials."""
    return f'campaigns/{instance.campaign.id}/reference/{filename}'


class Campaign(models.Model):
    """Campaign model for UGC briefs posted by brands."""
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        LIVE = 'LIVE', _('Live')
        CLOSED = 'CLOSED', _('Closed')
    
    class ContentType(models.TextChoices):
        INSTAGRAM_REEL = 'INSTAGRAM_REEL', _('Instagram Reel')
        INSTAGRAM_POST = 'INSTAGRAM_POST', _('Instagram Post')
        INSTAGRAM_STORY = 'INSTAGRAM_STORY', _('Instagram Story')
        TIKTOK_VIDEO = 'TIKTOK_VIDEO', _('TikTok Video')
        YOUTUBE_VIDEO = 'YOUTUBE_VIDEO', _('YouTube Video')
        YOUTUBE_SHORT = 'YOUTUBE_SHORT', _('YouTube Short')
    
    # Basic fields
    title = models.CharField(
        _('title'),
        max_length=200,
        help_text=_('Campaign title')
    )
    description = models.TextField(
        _('description'),
        help_text=_('Detailed campaign description')
    )
    content_type = models.CharField(
        _('content type'),
        max_length=50,
        choices=ContentType.choices,
        help_text=_('Type of content to be created')
    )
    deliverables = models.TextField(
        _('deliverables'),
        help_text=_('Expected deliverables for this campaign')
    )
    budget = models.DecimalField(
        _('budget'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text=_('Campaign budget in EUR')
    )
    deadline = models.DateField(
        _('deadline'),
        help_text=_('Application deadline')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text=_('Campaign status')
    )
    
    # Relationships
    brand = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaigns',
        limit_choices_to={'role': 'BRAND'},
        help_text=_('Brand that created this campaign')
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['brand', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def clean(self):
        """Validate that deadline is in the future."""
        super().clean()
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError({'deadline': _('Deadline must be a future date.')})
    
    def save(self, *args, **kwargs):
        """Override save to run clean validation."""
        self.full_clean()
        super().save(*args, **kwargs)


class CampaignFile(models.Model):
    """Model for campaign reference material files."""
    
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='reference_files',
        help_text=_('Campaign this file belongs to')
    )
    file = models.FileField(
        _('file'),
        upload_to=campaign_file_upload_path,
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'mp4', 'mov']
            )
        ],
        help_text=_('Reference material file (max 10 MB)')
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('campaign file')
        verbose_name_plural = _('campaign files')
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"File for {self.campaign.title}"
