from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile

class AccountsTests(TestCase):
    def test_signup_creates_profile(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'SafePass123_!',
            'password2': 'SafePass123_!'
        })
        # If password validation fails, print errors to diagnose
        if response.status_code == 200:
            print("Form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')

    def test_login_logout(self):
        user = User.objects.create_user(username='testuser', password='SafePass123_!')
        # Login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'SafePass123_!'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue('_auth_user_id' in self.client.session)

        # Logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_update(self):
        user = User.objects.create_user(username='testuser', password='SafePass123_!')
        user.first_name = 'Original'
        user.save()
        
        self.client.login(username='testuser', password='SafePass123_!')
        
        response = self.client.post(reverse('profile'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'age': 25,
            'gender': 'M',
            'height_cm': 175.5,
            'weight_kg': 70.0,
            'bio': 'Some bio'
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'UpdatedFirst')
        self.assertEqual(user.profile.age, 25)
        self.assertEqual(user.profile.gender, 'M')
        self.assertEqual(user.profile.height_cm, 175.5)
        self.assertEqual(user.profile.weight_kg, 70.0)
        self.assertEqual(user.profile.bio, 'Some bio')
