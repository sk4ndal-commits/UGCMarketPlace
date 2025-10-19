from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Campaign, CampaignFile
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignCreateSerializer,
    CampaignFileSerializer
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
        Return campaigns based on user role.
        - Brands see all their own campaigns
        - Influencers see only live campaigns
        """
        user = self.request.user
        
        if user.role == 'BRAND':
            # Brands see their own campaigns regardless of status
            return Campaign.objects.filter(brand=user).select_related('brand').prefetch_related('reference_files')
        elif user.role == 'INFLUENCER':
            # Influencers see only live campaigns
            return Campaign.objects.filter(status=Campaign.Status.LIVE).select_related('brand').prefetch_related('reference_files')
        else:
            # No role assigned - return empty queryset
            return Campaign.objects.none()
    
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
