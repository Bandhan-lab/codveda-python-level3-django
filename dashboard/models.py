from django.db import models

class Workspace(models.Model):
    """Permission anchor for the protected member dashboard."""

    name = models.CharField(max_length=100, default="Codveda Workspace")

    class Meta:
        permissions = [
            ("access_member_dashboard", "Can access the member dashboard"),
        ]

    def __str__(self):
        return self.name
