#!/usr/bin/env python
"""
Test script to verify logout endpoint handles invalid tokens gracefully.
"""
import os
import sys
import django

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone

User = get_user_model()

def test_logout_with_invalid_token():
    """Test that logout returns success even with invalid token."""
    client = APIClient()
    
    # Create and authenticate user
    user = User.objects.create_user(
        email='test_logout@example.com',
        password='TestPass123!',
        gdpr_consent=True,
        gdpr_consent_date=timezone.now()
    )
    
    # Login to get tokens
    response = client.post('/api/v1/auth/login/', {
        'email': 'test_logout@example.com',
        'password': 'TestPass123!'
    }, format='json')
    
    access_token = response.data['data']['tokens']['access']
    
    # Authenticate with access token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    print("Test 1: Logout with valid refresh token")
    refresh_token = response.data['data']['tokens']['refresh']
    response = client.post('/api/v1/auth/logout/', {
        'refresh': refresh_token
    }, format='json')
    
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.data}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("  ✓ PASSED\n")
    
    # Login again for second test
    response = client.post('/api/v1/auth/login/', {
        'email': 'test_logout@example.com',
        'password': 'TestPass123!'
    }, format='json')
    
    access_token = response.data['data']['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    print("Test 2: Logout with invalid refresh token")
    response = client.post('/api/v1/auth/logout/', {
        'refresh': 'invalid_token_string'
    }, format='json')
    
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.data}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("  ✓ PASSED\n")
    
    print("Test 3: Logout with already blacklisted token (using same token twice)")
    # Login once more
    response = client.post('/api/v1/auth/login/', {
        'email': 'test_logout@example.com',
        'password': 'TestPass123!'
    }, format='json')
    
    access_token = response.data['data']['tokens']['access']
    refresh_token = response.data['data']['tokens']['refresh']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # First logout - should work
    response = client.post('/api/v1/auth/logout/', {
        'refresh': refresh_token
    }, format='json')
    assert response.status_code == 200
    
    # Login again to get new access token (but try to use old refresh token)
    response = client.post('/api/v1/auth/login/', {
        'email': 'test_logout@example.com',
        'password': 'TestPass123!'
    }, format='json')
    
    new_access_token = response.data['data']['tokens']['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
    
    # Try to logout with already blacklisted token
    response = client.post('/api/v1/auth/logout/', {
        'refresh': refresh_token  # This token was already blacklisted
    }, format='json')
    
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.data}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("  ✓ PASSED\n")
    
    # Cleanup
    user.delete()
    
    print("=" * 50)
    print("All tests PASSED! ✓")
    print("=" * 50)

if __name__ == '__main__':
    test_logout_with_invalid_token()
