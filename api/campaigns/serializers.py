from rest_framework import serializers
from django.utils import timezone
from .models import Campaign, CampaignFile, Application


class CampaignFileSerializer(serializers.ModelSerializer):
    """Serializer for campaign reference files."""
    
    class Meta:
        model = CampaignFile
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model."""
    
    reference_files = CampaignFileSerializer(many=True, read_only=True)
    brand_email = serializers.EmailField(source='brand.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Campaign
        fields = [
            'id',
            'title',
            'description',
            'content_type',
            'content_type_display',
            'category',
            'category_display',
            'deliverables',
            'budget',
            'deadline',
            'status',
            'status_display',
            'brand',
            'brand_email',
            'reference_files',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'brand', 'created_at', 'updated_at']
    
    def validate_budget(self, value):
        """Validate that budget is greater than 0."""
        if value <= 0:
            raise serializers.ValidationError("Budget must be greater than 0.")
        return value
    
    def validate_deadline(self, value):
        """Validate that deadline is in the future."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline must be a future date.")
        return value
    
    def validate(self, attrs):
        """Additional validation for the campaign."""
        # Ensure brand users can only create campaigns
        request = self.context.get('request')
        if request and request.user:
            if request.user.role != 'BRAND':
                raise serializers.ValidationError(
                    "Only users with Brand role can create campaigns."
                )
        return attrs


class CampaignListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for campaign listing."""
    
    brand_email = serializers.EmailField(source='brand.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Campaign
        fields = [
            'id',
            'title',
            'content_type',
            'content_type_display',
            'category',
            'category_display',
            'budget',
            'deadline',
            'status',
            'status_display',
            'brand_email',
            'created_at',
        ]
        read_only_fields = fields


class CampaignCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating campaigns with file uploads."""
    
    reference_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False,
        allow_empty=True,
        help_text="Optional reference material files (max 10 MB each)"
    )
    
    class Meta:
        model = Campaign
        fields = [
            'title',
            'description',
            'content_type',
            'category',
            'deliverables',
            'budget',
            'deadline',
            'status',
            'reference_files',
        ]
    
    def validate_budget(self, value):
        """Validate that budget is greater than 0."""
        if value <= 0:
            raise serializers.ValidationError("Budget must be greater than 0.")
        return value
    
    def validate_deadline(self, value):
        """Validate that deadline is in the future."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline must be a future date.")
        return value
    
    def validate_reference_files(self, files):
        """Validate each uploaded file."""
        max_size = 10 * 1024 * 1024  # 10 MB
        for file in files:
            if file.size > max_size:
                raise serializers.ValidationError(
                    f"File {file.name} exceeds maximum size of 10 MB."
                )
        return files
    
    def create(self, validated_data):
        """Create campaign and associated files."""
        reference_files = validated_data.pop('reference_files', [])
        
        # Set brand from request user
        request = self.context.get('request')
        if request and request.user:
            validated_data['brand'] = request.user
        
        # Create campaign
        campaign = Campaign.objects.create(**validated_data)
        
        # Create associated files
        for file in reference_files:
            CampaignFile.objects.create(campaign=campaign, file=file)
        
        return campaign


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model with influencer profile details."""
    
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    influencer_email = serializers.EmailField(source='influencer.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Influencer profile fields
    influencer_followers = serializers.IntegerField(source='influencer.followers', read_only=True)
    influencer_engagement_rate = serializers.DecimalField(
        source='influencer.engagement_rate',
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    influencer_platform = serializers.CharField(source='influencer.platform', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'campaign',
            'campaign_title',
            'influencer',
            'influencer_email',
            'influencer_followers',
            'influencer_engagement_rate',
            'influencer_platform',
            'pitch',
            'portfolio_link',
            'proposed_price',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'influencer', 'status', 'created_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications."""
    
    class Meta:
        model = Application
        fields = [
            'campaign',
            'pitch',
            'portfolio_link',
            'proposed_price',
        ]
    
    def validate_pitch(self, value):
        """Validate that pitch is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Pitch cannot be empty.")
        return value
    
    def validate_proposed_price(self, value):
        """Validate that proposed price is positive if provided."""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Proposed price must be greater than 0.")
        return value
    
    def validate(self, attrs):
        """Additional validation for the application."""
        request = self.context.get('request')
        
        # Ensure only influencers can create applications
        if request and request.user:
            if request.user.role != 'INFLUENCER':
                raise serializers.ValidationError(
                    "Only users with Influencer role can create applications."
                )
        
        campaign = attrs.get('campaign')
        
        # Check if campaign is live
        if campaign.status != Campaign.Status.LIVE:
            raise serializers.ValidationError(
                {'campaign': 'Can only apply to live campaigns.'}
            )
        
        # Check if campaign is expired
        if campaign.deadline < timezone.now().date():
            raise serializers.ValidationError(
                {'campaign': 'Cannot apply to expired campaigns.'}
            )
        
        # Check if user already applied
        if request and request.user:
            existing_application = Application.objects.filter(
                campaign=campaign,
                influencer=request.user
            ).first()
            if existing_application:
                raise serializers.ValidationError(
                    {'campaign': 'You have already applied to this campaign.'}
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create application with the current user as influencer."""
        request = self.context.get('request')
        if request and request.user:
            validated_data['influencer'] = request.user
        
        return Application.objects.create(**validated_data)
