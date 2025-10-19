from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Template, Application

User = get_user_model()


class TemplateModelTest(TestCase):
    """Test cases for Template model."""
    
    def setUp(self):
        """Set up test data."""
        self.template = Template.objects.create(
            template_id='tpl-test-01',
            name='Test Template',
            description='Test template description',
            required_parameters=['param1', 'param2'],
        )
    
    def test_template_creation(self):
        """Test template is created correctly."""
        self.assertEqual(self.template.template_id, 'tpl-test-01')
        self.assertEqual(self.template.name, 'Test Template')
        self.assertTrue(self.template.is_available)
    
    def test_template_str(self):
        """Test template string representation."""
        self.assertEqual(str(self.template), 'Test Template (tpl-test-01)')
    
    def test_validate_parameters_success(self):
        """Test parameter validation succeeds with all required params."""
        parameters = {'param1': 'value1', 'param2': 'value2'}
        self.assertTrue(self.template.validate_parameters(parameters))
    
    def test_validate_parameters_missing(self):
        """Test parameter validation fails with missing params."""
        parameters = {'param1': 'value1'}
        with self.assertRaises(ValidationError):
            self.template.validate_parameters(parameters)


class ApplicationModelTest(TestCase):
    """Test cases for Application model."""
    
    def setUp(self):
        """Set up test data."""
        self.creator = User.objects.create_user(
            email='creator@test.com',
            password='testpass123',
            role='CREATOR'
        )
        self.template = Template.objects.create(
            template_id='tpl-react-spa-01',
            name='React SPA Template',
            description='React single page application template',
        )
    
    def test_application_creation(self):
        """Test application is created correctly."""
        app = Application.objects.create(
            name='Test App',
            description='Test application',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        self.assertEqual(app.name, 'Test App')
        self.assertEqual(app.visibility, 'INTERNAL')
        self.assertTrue(app.application_id.startswith('app_'))
    
    def test_application_unique_name(self):
        """Test application name must be unique."""
        Application.objects.create(
            name='Unique App',
            description='First app',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        
        # Try to create another with same name
        with self.assertRaises(ValidationError):
            app = Application(
                name='Unique App',
                description='Second app',
                owner='team-test',
                visibility='INTERNAL',
                creator=self.creator,
            )
            app.save()
    
    def test_application_with_template(self):
        """Test application with template."""
        app = Application.objects.create(
            name='Templated App',
            description='App with template',
            owner='team-test',
            visibility='INTERNAL',
            template=self.template,
            creator=self.creator,
        )
        self.assertEqual(app.template, self.template)
    
    def test_git_integration_validation(self):
        """Test Git integration validation."""
        app = Application(
            name='Git App',
            description='App with Git',
            owner='team-test',
            visibility='INTERNAL',
            git_integration={'invalid': 'data'},  # Missing repository_url
            creator=self.creator,
        )
        with self.assertRaises(ValidationError):
            app.save()


class ApplicationAPITest(APITestCase):
    """Test cases for Application API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create users
        self.creator = User.objects.create_user(
            email='creator@test.com',
            password='testpass123',
            role='CREATOR',
            is_active=True
        )
        self.brand = User.objects.create_user(
            email='brand@test.com',
            password='testpass123',
            role='BRAND',
            is_active=True
        )
        
        # Create template
        self.template = Template.objects.create(
            template_id='tpl-react-spa-01',
            name='React SPA Template',
            description='React single page application template',
        )
    
    def test_create_application_as_creator(self):
        """Test creating application as creator."""
        self.client.force_authenticate(user=self.creator)
        
        data = {
            'name': 'Customer Portal',
            'description': 'Portal for customers',
            'owner': 'team-customer',
            'visibility': 'INTERNAL',
            'template_id': 'tpl-react-spa-01',
        }
        
        response = self.client.post('/api/v1/applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['name'], 'Customer Portal')
        self.assertTrue(response.data['data']['application_id'].startswith('app_'))
    
    def test_create_application_as_non_creator(self):
        """Test creating application as non-creator fails."""
        self.client.force_authenticate(user=self.brand)
        
        data = {
            'name': 'Customer Portal',
            'description': 'Portal for customers',
            'owner': 'team-customer',
            'visibility': 'INTERNAL',
        }
        
        response = self.client.post('/api/v1/applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_application_unauthenticated(self):
        """Test creating application without authentication fails."""
        data = {
            'name': 'Customer Portal',
            'description': 'Portal for customers',
            'owner': 'team-customer',
            'visibility': 'INTERNAL',
        }
        
        response = self.client.post('/api/v1/applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_applications_as_creator(self):
        """Test listing applications as creator."""
        # Create application
        Application.objects.create(
            name='Test App',
            description='Test',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        
        self.client.force_authenticate(user=self.creator)
        response = self.client.get('/api/v1/applications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 1)
    
    def test_get_templates(self):
        """Test getting available templates."""
        self.client.force_authenticate(user=self.creator)
        response = self.client.get('/api/v1/templates/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 1)
    
    def test_update_application(self):
        """Test updating application."""
        app = Application.objects.create(
            name='Original Name',
            description='Original description',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        
        self.client.force_authenticate(user=self.creator)
        data = {
            'name': 'Updated Name',
            'description': 'Updated description',
        }
        
        response = self.client.patch(f'/api/v1/applications/{app.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Name')
    
    def test_delete_application(self):
        """Test deleting application."""
        app = Application.objects.create(
            name='To Delete',
            description='Will be deleted',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        
        self.client.force_authenticate(user=self.creator)
        response = self.client.delete(f'/api/v1/applications/{app.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Application.objects.filter(id=app.id).exists())
    
    def test_duplicate_name_validation(self):
        """Test duplicate application name is rejected."""
        Application.objects.create(
            name='Unique Name',
            description='First',
            owner='team-test',
            visibility='INTERNAL',
            creator=self.creator,
        )
        
        self.client.force_authenticate(user=self.creator)
        data = {
            'name': 'Unique Name',
            'description': 'Second',
            'owner': 'team-test',
            'visibility': 'INTERNAL',
        }
        
        response = self.client.post('/api/v1/applications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
