import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


User = get_user_model()


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resetuser",
            email="reset@example.com",
            password="OldStrongPass123!",
        )

    def test_reset_request_sends_email(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "reset@example.com"},
        )
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset@example.com", mail.outbox[0].to)

    def test_unknown_email_does_not_reveal_account(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "unknown@example.com"},
        )
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_link_changes_password_and_new_password_logs_in(self):
        self.client.post(
            reverse("password_reset"),
            {"email": "reset@example.com"},
        )
        body = mail.outbox[0].body
        match = re.search(r"/accounts/reset/(\S+)/(\S+)/", body)
        self.assertIsNotNone(match)

        uidb64, token = match.groups()
        response = self.client.get(
            reverse(
                "password_reset_confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
        )
        self.assertEqual(response.status_code, 302)
        confirm_url = response.url
        response = self.client.post(
            confirm_url,
            {
                "new_password1": "NewStrongPass123!",
                "new_password2": "NewStrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPass123!"))
        self.assertTrue(
            self.client.login(
                username="resetuser",
                password="NewStrongPass123!",
            )
        )

    def test_registration_assigns_member_role(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Role",
                "last_name": "User",
                "username": "roleuser",
                "email": "role@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="roleuser")
        self.assertTrue(user.groups.filter(name="Member").exists())
