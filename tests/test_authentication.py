from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bandhan", email="bandhan@example.com", password="StrongPass123!"
        )

    def test_registration_page_loads(self):
        self.assertEqual(self.client.get(reverse("register")).status_code, 200)

    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Test", "last_name": "User", "username": "newuser",
            "email": "new@example.com", "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Other", "last_name": "User", "username": "other",
            "email": "BANDHAN@example.com", "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

    def test_login_and_logout(self):
        self.assertTrue(self.client.login(username="bandhan", password="StrongPass123!"))
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/accounts/login/?next=/dashboard/")

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/accounts/login/?next=/accounts/profile/")

    def test_staff_role_is_recognized(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse("dashboard")), "Staff")
