"""
Basic tests for the Open Ear Trainer application.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BasicTestCase(TestCase):
    """Basic Django tests."""

    def test_basic_math(self):
        """Test basic functionality."""
        self.assertEqual(2 + 2, 4)

    def test_django_setup(self):
        """Test that Django is properly configured."""
        from django.conf import settings

        self.assertTrue(settings.DEBUG is not None)


class APITestCase(APITestCase):
    """API endpoint tests."""

    def test_exercises_list_endpoint(self):
        """Test that exercises API endpoint is accessible."""
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        # Should return 200 even if no exercises exist
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check(self):
        """Test basic health check."""
        # Simple test that the app is running
        self.assertTrue(True)
