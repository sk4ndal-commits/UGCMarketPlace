from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Campaign, CampaignFile, Application
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignCreateSerializer,
    CampaignFileSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer
)


class IsBrand(IsAuthenticated):
    """Permission class to check if user is a brand."""
    
    def has_permission(self, request, view):
        """Check if user is authenticated and has BRAND role."""
        if not super().has_permission(request, view):
            return False
        return request.user.role == 'BRAND'


class IsInfluencer(IsAuthenticated):
    """Permission class to check if user is an influencer."""
    
    def has_permission(self, request, view):
        """Check if user is authenticated and has INFLUENCER role."""
        if not super().has_permission(request, view):
            return False
        return request.user.role == 'INFLUENCER'


class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Campaign model.
    
    - Brands can create, update, delete their own campaigns
    - Influencers can only view live campaigns
    - List view shows different campaigns based on user role
    """
    
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CampaignCreateSerializer
        elif self.action == 'list':
            return CampaignListSerializer
        return CampaignSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action.
        - Create, update, partial_update, destroy: Brand only
        - List, retrieve: Both brands and influencers
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsBrand]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Return campaigns based on user role with optional filtering.
        - Brands see all their own campaigns
        - Influencers see only live campaigns
        
        Query parameters for filtering (for influencers):
        - budget_min: minimum budget
        - budget_max: maximum budget
        - category: campaign category
        - content_type: platform/content type
        - deadline_before: deadline before this date (YYYY-MM-DD)
        """
        user = self.request.user
        
        if user.role == 'BRAND':
            # Brands see their own campaigns regardless of status
            queryset = Campaign.objects.filter(brand=user).select_related('brand').prefetch_related('reference_files')
        elif user.role == 'INFLUENCER':
            # Influencers see only live campaigns
            queryset = Campaign.objects.filter(status=Campaign.Status.LIVE).select_related('brand').prefetch_related('reference_files')
            
            # Apply filters from query parameters
            budget_min = self.request.query_params.get('budget_min')
            budget_max = self.request.query_params.get('budget_max')
            category = self.request.query_params.get('category')
            content_type = self.request.query_params.get('content_type')
            deadline_before = self.request.query_params.get('deadline_before')
            
            if budget_min:
                try:
                    queryset = queryset.filter(budget__gte=float(budget_min))
                except ValueError:
                    pass
            
            if budget_max:
                try:
                    queryset = queryset.filter(budget__lte=float(budget_max))
                except ValueError:
                    pass
            
            if category:
                queryset = queryset.filter(category=category)
            
            if content_type:
                queryset = queryset.filter(content_type=content_type)
            
            if deadline_before:
                try:
                    queryset = queryset.filter(deadline__lte=deadline_before)
                except ValueError:
                    pass
            
            return queryset
        else:
            # No role assigned - return empty queryset
            return Campaign.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the brand to current user when creating campaign."""
        serializer.save()
    
    def perform_update(self, serializer):
        """Ensure only campaign owner can update."""
        campaign = self.get_object()
        if campaign.brand != self.request.user:
            return Response(
                {
                    'status': 'error',
                    'errors': ['You do not have permission to edit this campaign.']
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure only campaign owner can delete."""
        if instance.brand != self.request.user:
            return Response(
                {
                    'status': 'error',
                    'errors': ['You do not have permission to delete this campaign.']
                },
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
    
    def list(self, request, *args, **kwargs):
        """
        List campaigns with consistent JSON response format.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single campaign with consistent JSON response format.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def create(self, request, *args, **kwargs):
        """
        Create a campaign with consistent JSON response format.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            self.perform_create(serializer)
            # Return full campaign data after creation
            campaign = serializer.instance
            response_serializer = CampaignSerializer(campaign, context={'request': request})
            
            return Response({
                'status': 'success',
                'data': response_serializer.data,
                'errors': []
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update a campaign with consistent JSON response format.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check ownership
        if instance.brand != request.user:
            return Response({
                'status': 'error',
                'data': {},
                'errors': ['You do not have permission to edit this campaign.']
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'errors': []
            })
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a campaign with consistent JSON response format.
        """
        instance = self.get_object()
        
        # Check ownership
        if instance.brand != request.user:
            return Response({
                'status': 'error',
                'data': {},
                'errors': ['You do not have permission to delete this campaign.']
            }, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'data': {'message': 'Campaign deleted successfully.'},
            'errors': []
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsBrand])
    def upload_file(self, request, pk=None):
        """
        Upload additional reference files to an existing campaign.
        Only the campaign owner (brand) can upload files.
        """
        campaign = self.get_object()
        
        # Check ownership
        if campaign.brand != request.user:
            return Response({
                'status': 'error',
                'data': {},
                'errors': ['You do not have permission to upload files to this campaign.']
            }, status=status.HTTP_403_FORBIDDEN)
        
        file = request.FILES.get('file')
        if not file:
            return Response({
                'status': 'error',
                'data': {},
                'errors': ['No file provided.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create campaign file
        campaign_file = CampaignFile(campaign=campaign, file=file)
        try:
            campaign_file.full_clean()
            campaign_file.save()
            serializer = CampaignFileSerializer(campaign_file)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'errors': []
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': {},
                'errors': [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application model.
    
    - Influencers can create applications and view their own applications
    - Brands can view applications for their campaigns
    """
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action.
        - Create: Influencer only
        - List, retrieve: Both brands and influencers
        """
        if self.action == 'create':
            permission_classes = [IsInfluencer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Return applications based on user role.
        - Brands see applications for their campaigns
        - Influencers see their own applications
        """
        user = self.request.user
        
        if user.role == 'BRAND':
            # Brands see applications for their campaigns
            return Application.objects.filter(
                campaign__brand=user
            ).select_related('campaign', 'influencer').order_by('-created_at')
        elif user.role == 'INFLUENCER':
            # Influencers see their own applications
            return Application.objects.filter(
                influencer=user
            ).select_related('campaign', 'influencer').order_by('-created_at')
        else:
            return Application.objects.none()
    
    def list(self, request, *args, **kwargs):
        """List applications with consistent JSON response format."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single application with consistent JSON response format."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def create(self, request, *args, **kwargs):
        """
        Create an application with consistent JSON response format.
        Sends confirmation email to influencer after successful submission.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            application = serializer.save()
            
            # Send confirmation email to influencer
            try:
                send_mail(
                    subject=f'Application Submitted: {application.campaign.title}',
                    message=f'Dear {request.user.email},\n\n'
                            f'Your application to the campaign "{application.campaign.title}" has been successfully submitted.\n\n'
                            f'Campaign Details:\n'
                            f'- Title: {application.campaign.title}\n'
                            f'- Budget: €{application.campaign.budget}\n'
                            f'- Deadline: {application.campaign.deadline}\n\n'
                            f'Your Pitch: {application.pitch}\n'
                            f'Proposed Price: €{application.proposed_price if application.proposed_price else "Not specified"}\n\n'
                            f'The brand will review your application and get back to you.\n\n'
                            f'Best regards,\n'
                            f'CollabMarket Team',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log email error but don't fail the request
                print(f"Failed to send confirmation email: {e}")
            
            # Return full application data
            response_serializer = ApplicationSerializer(application, context={'request': request})
            
            return Response({
                'status': 'success',
                'data': response_serializer.data,
                'errors': []
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'data': {},
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
