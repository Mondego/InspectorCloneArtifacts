from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from . import models


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="testUser", password="test")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instance
        user.save()
        self.assertIsInstance(user.profile, models.Profile)