from django.contrib import admin
from .models import Campaign, CampaignFile


class CampaignFileInline(admin.TabularInline):
    """Inline admin for campaign files."""
    model = CampaignFile
    extra = 0
    readonly_fields = ['uploaded_at']


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin interface for Campaign model."""
    
    list_display = ['title', 'brand', 'status', 'content_type', 'budget', 'deadline', 'created_at']
    list_filter = ['status', 'content_type', 'created_at']
    search_fields = ['title', 'description', 'brand__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CampaignFileInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'brand')
        }),
        ('Campaign Details', {
            'fields': ('content_type', 'deliverables', 'budget', 'deadline', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CampaignFile)
class CampaignFileAdmin(admin.ModelAdmin):
    """Admin interface for CampaignFile model."""
    
    list_display = ['campaign', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['campaign__title']
    readonly_fields = ['uploaded_at']
