from rest_framework import serializers
from .models import Template, Application


class TemplateSerializer(serializers.ModelSerializer):
    """Serializer for Template model."""
    
    class Meta:
        model = Template
        fields = [
            'id',
            'template_id',
            'name',
            'description',
            'is_available',
            'default_parameters',
            'required_parameters',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model."""
    
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    template_details = TemplateSerializer(source='template', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'application_id',
            'name',
            'description',
            'owner',
            'visibility',
            'template',
            'template_details',
            'parameters',
            'git_integration',
            'oidc_integration',
            'creator',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['application_id', 'creator', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate that the application name is unique."""
        # Check if updating existing application
        if self.instance:
            # Exclude current instance from uniqueness check
            if Application.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
                raise serializers.ValidationError("An application with this name already exists.")
        else:
            # Creating new application
            if Application.objects.filter(name=value).exists():
                raise serializers.ValidationError("An application with this name already exists.")
        return value
    
    def validate_template(self, value):
        """Validate that the template is available."""
        if value and not value.is_available:
            raise serializers.ValidationError("This template is not available.")
        return value
    
    def validate(self, data):
        """Validate the entire application data."""
        # If template is provided, check that required parameters are complete
        template = data.get('template')
        parameters = data.get('parameters', {})
        
        if template:
            try:
                template.validate_parameters(parameters)
            except Exception as e:
                raise serializers.ValidationError({
                    'parameters': str(e)
                })
        
        return data
    
    def create(self, validated_data):
        """Create application and set the creator from the request context."""
        # Get creator from request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['creator'] = request.user
        
        return super().create(validated_data)


class ApplicationCreateSerializer(ApplicationSerializer):
    """Serializer for creating applications with more flexible input."""
    
    template_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields + ['template_id']
    
    def validate_template_id(self, value):
        """Validate and retrieve template by template_id."""
        if value:
            try:
                template = Template.objects.get(template_id=value, is_available=True)
                return template
            except Template.DoesNotExist:
                raise serializers.ValidationError(
                    f"Template '{value}' not found or not available."
                )
        return None
    
    def validate(self, data):
        """Handle template_id conversion and validation."""
        # Convert template_id to template object
        template_id = data.pop('template_id', None)
        if template_id:
            data['template'] = template_id
        
        return super().validate(data)


class ApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing applications."""
    
    template_name = serializers.CharField(source='template.name', read_only=True)
    creator_email = serializers.CharField(source='creator.email', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'application_id',
            'name',
            'description',
            'owner',
            'visibility',
            'template_name',
            'creator_email',
            'created_at',
        ]
