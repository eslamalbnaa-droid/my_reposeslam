from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile

User = get_user_model()


class GuestOnlyPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass12345')

    def test_authenticated_user_is_redirected_from_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('home'))

    def test_authenticated_user_is_redirected_from_register(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('home'))

    def test_anonymous_user_can_open_login_and_register(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('register')).status_code, 200)

    def test_profile_signal_creates_profile(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())


class ProfilePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass12345', email='old@example.com')

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_edit_updates_extended_profile(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Ali', 'last_name': 'Test', 'email': 'ali@example.com',
            'phone': '12345', 'address': 'Aden', 'city': 'Aden', 'gender': 'male', 'birth_date': '',
            'bio': 'Motorcycle fan', 'favorite_brand': 'Honda', 'notifications_enabled': 'on',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ali')
        self.assertEqual(self.user.profile.bio, 'Motorcycle fan')
        self.assertEqual(self.user.profile.favorite_brand, 'Honda')
