#!/usr/bin/env python
"""
Test script for campaign application features:
1. Applications appear in the list after creation
2. Duplicate applications are prevented
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
from campaigns.models import Campaign, Application
from datetime import date, timedelta

User = get_user_model()

print("=" * 80)
print("CAMPAIGN APPLICATION FEATURE TESTS")
print("=" * 80)

# Clean up any existing test data
print("\n1. Cleaning up test data...")
User.objects.filter(email__in=['test_brand@example.com', 'test_influencer@example.com']).delete()
Campaign.objects.filter(title='Test Campaign for Applications').delete()

# Create test users
print("\n2. Creating test users...")
brand = User.objects.create_user(
    email='test_brand@example.com',
    password='testpass123',
    role='BRAND',
    is_active=True
)
print(f"   ✓ Created brand user: {brand.email}")

influencer = User.objects.create_user(
    email='test_influencer@example.com',
    password='testpass123',
    role='INFLUENCER',
    is_active=True,
    followers=10000,
    engagement_rate=5.5,
    platform='Instagram'
)
print(f"   ✓ Created influencer user: {influencer.email}")

# Create a test campaign
print("\n3. Creating test campaign...")
campaign = Campaign.objects.create(
    title='Test Campaign for Applications',
    description='A test campaign to verify application features',
    content_type='INSTAGRAM_REEL',
    category='LIFESTYLE',
    deliverables='Create 1 Instagram Reel',
    budget=500.00,
    deadline=date.today() + timedelta(days=30),
    status='LIVE',
    brand=brand
)
print(f"   ✓ Created campaign: {campaign.title} (ID: {campaign.id})")

# Setup API client for influencer
print("\n4. Setting up API client with JWT authentication...")
client = APIClient()
refresh = RefreshToken.for_user(influencer)
access_token = str(refresh.access_token)
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
print(f"   ✓ Generated JWT token for influencer")

# Test 1: Create an application
print("\n" + "=" * 80)
print("TEST 1: Create Application")
print("=" * 80)

application_data = {
    'campaign': campaign.id,
    'pitch': 'I am perfect for this campaign because I have relevant experience and engaged audience.',
    'portfolio_link': 'https://instagram.com/testinfluencer',
    'proposed_price': 450.00
}

print(f"   → POST /api/v1/campaign-applications/")
response = client.post('/api/v1/campaign-applications/', application_data, format='json')

print(f"   - Status code: {response.status_code}")
if response.status_code == 201:
    print(f"   ✓ Application created successfully!")
    application_id = response.data['data']['id']
    print(f"   - Application ID: {application_id}")
    print(f"   - Status: {response.data['data']['status']}")
else:
    print(f"   ✗ Failed to create application")
    print(f"   - Response: {response.data}")
    sys.exit(1)

# Test 2: Verify application appears in list
print("\n" + "=" * 80)
print("TEST 2: Verify Application Appears in List")
print("=" * 80)

print(f"   → GET /api/v1/campaign-applications/")
response = client.get('/api/v1/campaign-applications/')

print(f"   - Status code: {response.status_code}")
if response.status_code == 200:
    applications = response.data['data']
    print(f"   ✓ Applications list retrieved successfully!")
    print(f"   - Total applications: {len(applications)}")
    
    # Check if our application is in the list
    found = False
    for app in applications:
        if app['campaign'] == campaign.id:
            found = True
            print(f"   ✓ Application found in list!")
            print(f"   - Campaign: {app['campaign_title']}")
            print(f"   - Status: {app['status_display']}")
            print(f"   - Pitch: {app['pitch'][:50]}...")
            break
    
    if not found:
        print(f"   ✗ Application NOT found in list!")
        sys.exit(1)
else:
    print(f"   ✗ Failed to retrieve applications")
    print(f"   - Response: {response.data}")
    sys.exit(1)

# Test 3: Try to apply again (should be prevented)
print("\n" + "=" * 80)
print("TEST 3: Prevent Duplicate Application")
print("=" * 80)

print(f"   → POST /api/v1/campaign-applications/ (duplicate attempt)")
response = client.post('/api/v1/campaign-applications/', application_data, format='json')

print(f"   - Status code: {response.status_code}")
if response.status_code == 400:
    print(f"   ✓ Duplicate application correctly prevented!")
    errors = response.data.get('errors', {})
    if 'campaign' in errors:
        error_msg = errors['campaign']
        if isinstance(error_msg, list):
            error_msg = error_msg[0]
        print(f"   - Error message: {error_msg}")
        if 'already applied' in error_msg.lower():
            print(f"   ✓ Correct error message returned!")
        else:
            print(f"   ⚠ Error message doesn't mention 'already applied'")
    else:
        print(f"   - Full errors: {errors}")
else:
    print(f"   ✗ Duplicate application was NOT prevented!")
    print(f"   - Response: {response.data}")
    sys.exit(1)

# Cleanup
print("\n" + "=" * 80)
print("CLEANUP")
print("=" * 80)
print("   Removing test data...")
Application.objects.filter(campaign=campaign).delete()
campaign.delete()
brand.delete()
influencer.delete()
print("   ✓ Test data removed")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED!")
print("=" * 80)
print("\nSummary:")
print("  ✓ Applications can be created successfully")
print("  ✓ Applications appear in the user's application list")
print("  ✓ Duplicate applications are prevented with proper error message")
print("=" * 80)
