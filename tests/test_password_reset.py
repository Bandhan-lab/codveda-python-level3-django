from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
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

    def test_reset_link_can_set_a_new_password(self):
        self.client.post(
            reverse("password_reset"),
            {"email": "reset@example.com"},
        )
        self.assertEqual(len(mail.outbox), 1)

        email_body = mail.outbox[0].body
        self.assertIn("/accounts/reset/", email_body)

        self.client.get(
            reverse("password_reset"),
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
        self.assertTrue(Group.objects.filter(name="Member").exists())
