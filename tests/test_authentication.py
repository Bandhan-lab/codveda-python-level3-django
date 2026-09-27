from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bandhan",
            email="bandhan@example.com",
            password="StrongPass123!",
        )

    def test_registration_page_loads(self):
        self.assertEqual(self.client.get(reverse("register")).status_code, 200)

    def test_registration_creates_user_logs_in_and_assigns_member_role(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Test", "last_name": "User", "username": "newuser",
            "email": "new@example.com", "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="newuser")
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.groups.filter(name="Member").exists())

    def test_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Other", "last_name": "User", "username": "other",
            "email": "BANDHAN@example.com", "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Mismatch", "last_name": "User", "username": "mismatch",
            "email": "mismatch@example.com", "password1": "StrongPass123!",
            "password2": "DifferentPass123!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "password")

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

    def test_authenticated_user_without_role_is_denied(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_member_role_can_access_dashboard(self):
        group = Group.objects.create(name="Member")
        self.user.groups.add(group)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_staff_role_is_recognized_and_allowed(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse("dashboard")), "Staff")
