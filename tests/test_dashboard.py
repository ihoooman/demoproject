"""
Tests for the dashboard app.

This module contains tests for the dashboard app functionality.
"""

from django.test import TestCase
from dashboard.models import Group, Category, Subcategory, Response, SubcategoryResponse
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupModelTest(TestCase):
    """Test cases for the Group model."""
    
    def setUp(self):
        """Set up test data."""
        self.parent_group = Group.objects.create(title='Parent Group')
        self.child_group = Group.objects.create(
            title='Child Group',
            parent=self.parent_group
        )
    
    def test_group_creation(self):
        """Test that groups can be created with proper relationships."""
        self.assertEqual(self.parent_group.title, 'Parent Group')
        self.assertEqual(self.child_group.title, 'Child Group')
        self.assertEqual(self.child_group.parent, self.parent_group)
        self.assertIn(self.child_group, self.parent_group.children.all())

class CategoryModelTest(TestCase):
    """Test cases for the Category and Subcategory models."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(title='Test Category')
        self.subcategory = Subcategory.objects.create(
            title='Test Subcategory',
            category=self.category
        )
    
    def test_category_subcategory_relationship(self):
        """Test the relationship between categories and subcategories."""
        self.assertEqual(self.subcategory.category, self.category)
        self.assertIn(self.subcategory, self.category.subcategories.all())

class ResponseModelTest(TestCase):
    """Test cases for the Response models."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password='testpassword'
        )
        self.category = Category.objects.create(title='Test Category')
        self.subcategory = Subcategory.objects.create(
            title='Test Subcategory',
            category=self.category
        )
        self.group = Group.objects.create(title='Test Group')
        
        # Create a response linked to a subcategory
        self.subcategory_response = Response.objects.create(
            subcategory=self.subcategory,
            user=self.user,
            question='Test Question for Subcategory',
            answer='Test Answer for Subcategory'
        )
        
        # Create a response linked to a group
        self.group_response = Response.objects.create(
            group=self.group,
            user=self.user,
            question='Test Question for Group',
            answer='Test Answer for Group'
        )
    
    def test_response_creation(self):
        """Test that responses can be created and linked properly."""
        self.assertEqual(self.subcategory_response.subcategory, self.subcategory)
        self.assertEqual(self.subcategory_response.user, self.user)
        self.assertEqual(self.subcategory_response.question, 'Test Question for Subcategory')
        
        self.assertEqual(self.group_response.group, self.group)
        self.assertEqual(self.group_response.user, self.user)
        self.assertEqual(self.group_response.question, 'Test Question for Group')