from django.contrib import admin
from .models import Application, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Admin interface for Application Templates."""
    list_display = ('name', 'template_id', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'template_id', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template_id', 'description', 'is_available')
        }),
        ('Configuration', {
            'fields': ('default_parameters', 'required_parameters')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Applications."""
    list_display = ('name', 'application_id', 'owner', 'visibility', 'template', 'created_at')
    list_filter = ('visibility', 'created_at', 'template')
    search_fields = ('name', 'application_id', 'description', 'owner')
    readonly_fields = ('application_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'application_id', 'description', 'owner')
        }),
        ('Configuration', {
            'fields': ('template', 'visibility', 'parameters')
        }),
        ('Integrations', {
            'fields': ('git_integration', 'oidc_integration')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
