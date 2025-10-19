from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, ApplicationViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
