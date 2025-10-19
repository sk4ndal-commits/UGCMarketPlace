from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'campaign-applications', ApplicationViewSet, basename='campaign-application')

urlpatterns = [
    path('', include(router.urls)),
]
