"""
Tests for the accounts app.

This module contains tests for the accounts app functionality.
"""

from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    """Test cases for the User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password='testpassword'
        )
    
    def test_user_creation(self):
        """Test that a user can be created."""
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertTrue(self.user.check_password('testpassword'))