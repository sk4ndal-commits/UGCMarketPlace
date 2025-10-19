from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
import logging

from .models import Template, Application
from .serializers import (
    TemplateSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationListSerializer,
)

logger = logging.getLogger(__name__)


class IsCreator(permissions.BasePermission):
    """Custom permission to only allow creators to create/edit applications."""
    
    def has_permission(self, request, view):
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # For write operations, check if user has CREATOR role
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role == 'CREATOR'
        )
    
    def has_object_permission(self, request, view, obj):
        # Allow read operations for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations, check if user is the creator
        return obj.creator == request.user


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing templates (read-only for creators)."""
    
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only available templates."""
        return Template.objects.filter(is_available=True)
    
    def list(self, request, *args, **kwargs):
        """List templates with consistent response format."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single template."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    @action(detail=True, methods=['get'])
    def validate_parameters(self, request, pk=None):
        """Validate provided parameters against template requirements."""
        template = self.get_object()
        parameters = request.query_params.dict()
        
        try:
            template.validate_parameters(parameters)
            return Response({
                'status': 'success',
                'data': {'valid': True},
                'errors': []
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'data': {'valid': False},
                'errors': [str(e)]
            }, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing applications."""
    
    queryset = Application.objects.all()
    permission_classes = [IsCreator]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'list':
            return ApplicationListSerializer
        return ApplicationSerializer
    
    def get_queryset(self):
        """Filter applications based on user role and visibility."""
        user = self.request.user
        
        if not user.is_authenticated:
            return Application.objects.none()
        
        # Creators can see their own applications
        if user.role == 'CREATOR':
            return Application.objects.filter(creator=user)
        
        # Other authenticated users can see public and internal applications
        return Application.objects.filter(
            Q(visibility='PUBLIC') | Q(visibility='INTERNAL')
        )
    
    def create(self, request, *args, **kwargs):
        """Create a new application and publish creation event."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Save the application
        application = serializer.save()
        
        # Publish creation event
        self._publish_creation_event(application)
        
        # Return success response
        response_serializer = ApplicationSerializer(application, context={'request': request})
        return Response({
            'status': 'success',
            'data': response_serializer.data,
            'errors': []
        }, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single application."""
        instance = self.get_object()
        serializer = ApplicationSerializer(instance, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def list(self, request, *args, **kwargs):
        """List applications with consistent response format."""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply pagination if configured
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def update(self, request, *args, **kwargs):
        """Update an application."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ApplicationSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
    
    def destroy(self, request, *args, **kwargs):
        """Delete an application."""
        instance = self.get_object()
        instance.delete()
        
        return Response({
            'status': 'success',
            'data': {'message': 'Application deleted successfully'},
            'errors': []
        }, status=status.HTTP_200_OK)
    
    def _publish_creation_event(self, application):
        """Publish creator.application.created event."""
        event_data = {
            'event_type': 'creator.application.created',
            'timestamp': timezone.now().isoformat(),
            'data': {
                'application_id': application.application_id,
                'application_name': application.name,
                'creator_email': application.creator.email,
                'owner': application.owner,
                'visibility': application.visibility,
                'template_id': application.template.template_id if application.template else None,
                'created_at': application.created_at.isoformat(),
            }
        }
        
        # Log the event (in a real system, this would publish to a message queue)
        logger.info(f"Event published: {event_data}")

        return event_data
    
    @action(detail=True, methods=['get'])
    def catalog_view(self, request, pk=None):
        """Get application details for catalog display."""
        application = self.get_object()
        
        # Check visibility permissions
        if application.visibility == 'PRIVATE' and application.creator != request.user:
            return Response({
                'status': 'error',
                'data': None,
                'errors': ['You do not have permission to view this application']
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ApplicationSerializer(application, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data,
            'errors': []
        })
