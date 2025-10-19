from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal
from .models import Campaign, CampaignFile

User = get_user_model()


class CampaignModelTest(TestCase):
    """Test Campaign model."""
    
    def setUp(self):
        """Set up test data."""
        self.brand_user = User.objects.create_user(
            email='brand@test.com',
            password='testpass123',
            role='BRAND'
        )
    
    def test_campaign_creation(self):
        """Test creating a campaign."""
        campaign = Campaign.objects.create(
            title='Test Campaign',
            description='Test description',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='1 reel video',
            budget=Decimal('250.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=self.brand_user
        )
        self.assertEqual(campaign.title, 'Test Campaign')
        self.assertEqual(campaign.brand, self.brand_user)
        self.assertEqual(campaign.status, Campaign.Status.DRAFT)
    
    def test_campaign_str(self):
        """Test campaign string representation."""
        campaign = Campaign.objects.create(
            title='Test Campaign',
            description='Test description',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='1 reel video',
            budget=Decimal('250.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.LIVE,
            brand=self.brand_user
        )
        self.assertEqual(str(campaign), 'Test Campaign - Live')


class CampaignAPITest(APITestCase):
    """Test Campaign API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.brand_user = User.objects.create_user(
            email='brand@test.com',
            password='testpass123',
            role='BRAND'
        )
        self.influencer_user = User.objects.create_user(
            email='influencer@test.com',
            password='testpass123',
            role='INFLUENCER'
        )
        
        self.campaign_data = {
            'title': 'UGC Reel for Vegan Skincare Product',
            'description': 'Create an engaging reel showcasing our vegan skincare line',
            'content_type': 'INSTAGRAM_REEL',
            'deliverables': '1 Instagram Reel (30-60 seconds)',
            'budget': '250.00',
            'deadline': (date.today() + timedelta(days=30)).isoformat(),
            'status': 'DRAFT'
        }
    
    def test_brand_can_create_campaign(self):
        """Test that a brand user can create a campaign."""
        self.client.force_authenticate(user=self.brand_user)
        response = self.client.post('/api/v1/campaigns/', self.campaign_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['title'], self.campaign_data['title'])
        self.assertEqual(Campaign.objects.count(), 1)
    
    def test_influencer_cannot_create_campaign(self):
        """Test that an influencer cannot create a campaign."""
        self.client.force_authenticate(user=self.influencer_user)
        response = self.client.post('/api/v1/campaigns/', self.campaign_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Campaign.objects.count(), 0)
    
    def test_budget_validation_positive(self):
        """Test that budget must be greater than 0."""
        self.client.force_authenticate(user=self.brand_user)
        invalid_data = self.campaign_data.copy()
        invalid_data['budget'] = '0.00'
        
        response = self.client.post('/api/v1/campaigns/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('budget', response.data['errors'])
    
    def test_deadline_validation_future(self):
        """Test that deadline must be a future date."""
        self.client.force_authenticate(user=self.brand_user)
        invalid_data = self.campaign_data.copy()
        invalid_data['deadline'] = (date.today() - timedelta(days=1)).isoformat()
        
        response = self.client.post('/api/v1/campaigns/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('deadline', response.data['errors'])
    
    def test_brand_sees_own_campaigns(self):
        """Test that brand sees their own campaigns regardless of status."""
        self.client.force_authenticate(user=self.brand_user)
        
        # Create campaigns with different statuses
        Campaign.objects.create(
            title='Draft Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=self.brand_user
        )
        Campaign.objects.create(
            title='Live Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.LIVE,
            brand=self.brand_user
        )
        
        response = self.client.get('/api/v1/campaigns/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 2)
    
    def test_influencer_sees_only_live_campaigns(self):
        """Test that influencers see only live campaigns."""
        # Create campaigns with different statuses
        Campaign.objects.create(
            title='Draft Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=self.brand_user
        )
        Campaign.objects.create(
            title='Live Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.LIVE,
            brand=self.brand_user
        )
        Campaign.objects.create(
            title='Closed Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.CLOSED,
            brand=self.brand_user
        )
        
        self.client.force_authenticate(user=self.influencer_user)
        response = self.client.get('/api/v1/campaigns/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], 'Live Campaign')
    
    def test_brand_can_update_own_campaign(self):
        """Test that brand can update their own campaign."""
        campaign = Campaign.objects.create(
            title='Original Title',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=self.brand_user
        )
        
        self.client.force_authenticate(user=self.brand_user)
        response = self.client.patch(
            f'/api/v1/campaigns/{campaign.id}/',
            {'title': 'Updated Title'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['title'], 'Updated Title')
    
    def test_brand_cannot_update_others_campaign(self):
        """Test that brand cannot update another brand's campaign."""
        other_brand = User.objects.create_user(
            email='other@test.com',
            password='testpass123',
            role='BRAND'
        )
        campaign = Campaign.objects.create(
            title='Other Campaign',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=other_brand
        )
        
        self.client.force_authenticate(user=self.brand_user)
        response = self.client.patch(
            f'/api/v1/campaigns/{campaign.id}/',
            {'title': 'Hacked Title'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_brand_can_delete_own_campaign(self):
        """Test that brand can delete their own campaign."""
        campaign = Campaign.objects.create(
            title='To Delete',
            description='Test',
            content_type=Campaign.ContentType.INSTAGRAM_REEL,
            deliverables='Test',
            budget=Decimal('100.00'),
            deadline=date.today() + timedelta(days=30),
            status=Campaign.Status.DRAFT,
            brand=self.brand_user
        )
        
        self.client.force_authenticate(user=self.brand_user)
        response = self.client.delete(f'/api/v1/campaigns/{campaign.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(Campaign.objects.count(), 0)
    
    def test_authentication_required(self):
        """Test that authentication is required for all endpoints."""
        response = self.client.get('/api/v1/campaigns/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.post('/api/v1/campaigns/', self.campaign_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
