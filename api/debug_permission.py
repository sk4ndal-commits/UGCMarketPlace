import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from authentication.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from applications.views import ApplicationViewSet

# Create a creator user
creator = User.objects.create_user(
    email='debug@test.com',
    password='testpass123',
    role='CREATOR',
    is_active=True
)

print(f"User: {creator.email}")
print(f"Role: {creator.role}")
print(f"Role type: {type(creator.role)}")
print(f"Is CREATOR: {creator.role == 'CREATOR'}")
print(f"Has role attr: {hasattr(creator, 'role')}")
print(f"Is authenticated: {creator.is_authenticated}")
print(f"Is active: {creator.is_active}")

# Test the permission
factory = APIRequestFactory()
request = factory.post('/api/v1/applications/', {}, format='json')
force_authenticate(request, user=creator)

print(f"\nRequest user: {request.user}")
print(f"Request user authenticated: {request.user.is_authenticated}")
print(f"Request user role: {request.user.role}")

from applications.views import IsCreator
permission = IsCreator()
has_perm = permission.has_permission(request, None)
print(f"\nPermission result: {has_perm}")

# Cleanup
creator.delete()
