from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test user registration endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('authentication:register')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'gdpr_consent': True
        }
    
    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('user', response.data['data'])
        self.assertIn('tokens', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], 'test@example.com')
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
    
    def test_register_without_gdpr_consent(self):
        """Test registration fails without GDPR consent."""
        payload = self.valid_payload.copy()
        payload['gdpr_consent'] = False
        
        response = self.client.post(self.register_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_with_mismatched_passwords(self):
        """Test registration fails with mismatched passwords."""
        payload = self.valid_payload.copy()
        payload['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(self.register_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email."""
        # Create first user
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Try to create second user with same email
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_invalid_email(self):
        """Test registration fails with invalid email."""
        payload = self.valid_payload.copy()
        payload['email'] = 'invalid-email'
        
        response = self.client.post(self.register_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    """Test user login endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:login')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            gdpr_consent=True,
            gdpr_consent_date=timezone.now()
        )
    
    def test_login_success(self):
        """Test successful login."""
        payload = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('user', response.data['data'])
        self.assertIn('tokens', response.data['data'])
        self.assertIn('access', response.data['data']['tokens'])
        self.assertIn('refresh', response.data['data']['tokens'])
    
    def test_login_wrong_password(self):
        """Test login fails with wrong password."""
        payload = {
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post(self.login_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login fails with nonexistent user."""
        payload = {
            'email': 'nonexistent@example.com',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutTests(TestCase):
    """Test user logout endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('authentication:logout')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            gdpr_consent=True,
            gdpr_consent_date=timezone.now()
        )
        
        # Login to get tokens
        login_url = reverse('authentication:login')
        response = self.client.post(login_url, {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }, format='json')
        
        self.access_token = response.data['data']['tokens']['access']
        self.refresh_token = response.data['data']['tokens']['refresh']
    
    def test_logout_success(self):
        """Test successful logout."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.post(self.logout_url, {
            'refresh': self.refresh_token
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')


class RoleSelectionTests(TestCase):
    """Test role selection endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.role_url = reverse('authentication:role_selection')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            gdpr_consent=True,
            gdpr_consent_date=timezone.now()
        )
        
        # Login to get access token
        login_url = reverse('authentication:login')
        response = self.client.post(login_url, {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }, format='json')
        
        self.access_token = response.data['data']['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_select_brand_role(self):
        """Test selecting Brand role."""
        response = self.client.post(self.role_url, {
            'role': 'BRAND'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['user']['role'], 'BRAND')
        
        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'BRAND')
    
    def test_select_influencer_role(self):
        """Test selecting Influencer role."""
        response = self.client.post(self.role_url, {
            'role': 'INFLUENCER'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['user']['role'], 'INFLUENCER')
        
        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'INFLUENCER')
    
    def test_invalid_role(self):
        """Test selecting invalid role."""
        response = self.client.post(self.role_url, {
            'role': 'INVALID'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetTests(TestCase):
    """Test password reset endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.reset_request_url = reverse('authentication:password_reset_request')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='OldPass123!',
            gdpr_consent=True,
            gdpr_consent_date=timezone.now()
        )
    
    def test_password_reset_request(self):
        """Test password reset request."""
        response = self.client.post(self.reset_request_url, {
            'email': 'test@example.com'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
    
    def test_password_reset_nonexistent_email(self):
        """Test password reset with nonexistent email still returns success (security)."""
        response = self.client.post(self.reset_request_url, {
            'email': 'nonexistent@example.com'
        }, format='json')
        
        # Should still return success to not reveal user existence
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CurrentUserTests(TestCase):
    """Test current user endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.me_url = reverse('authentication:current_user')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            role='BRAND',
            gdpr_consent=True,
            gdpr_consent_date=timezone.now()
        )
        
        # Login to get access token
        login_url = reverse('authentication:login')
        response = self.client.post(login_url, {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }, format='json')
        
        self.access_token = response.data['data']['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_get_current_user(self):
        """Test retrieving current user data."""
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['user']['email'], 'test@example.com')
        self.assertEqual(response.data['data']['user']['role'], 'BRAND')
