#!/usr/bin/env python
"""
Test script to debug the applications endpoint authentication issue.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Create or get a creator user
creator, created = User.objects.get_or_create(
    email='test_creator@example.com',
    defaults={
        'role': 'CREATOR',
        'is_active': True
    }
)
if created:
    creator.set_password('testpass123')
    creator.save()
    print(f"✓ Created test creator user: {creator.email}")
else:
    print(f"✓ Using existing creator user: {creator.email}")

print(f"  - Role: {creator.role}")
print(f"  - Is authenticated: {creator.is_authenticated}")
print(f"  - Is active: {creator.is_active}")

# Generate JWT token
refresh = RefreshToken.for_user(creator)
access_token = str(refresh.access_token)

print(f"\n✓ Generated JWT token")
print(f"  - Access token (first 50 chars): {access_token[:50]}...")

# Test the endpoint
client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

print(f"\n→ Testing GET /api/v1/applications/")
response = client.get('/api/v1/applications/')

print(f"  - Status code: {response.status_code}")
print(f"  - Response data: {response.data}")

if response.status_code == 200:
    print("\n✅ SUCCESS: Authentication is working correctly!")
elif response.status_code == 401:
    print("\n❌ FAILED: Got 401 Unauthorized")
    print("   This suggests an authentication issue in the actual frontend-backend connection.")
else:
    print(f"\n⚠️  Unexpected status code: {response.status_code}")

# Cleanup option
print("\n(Test user will remain in database for further testing)")
