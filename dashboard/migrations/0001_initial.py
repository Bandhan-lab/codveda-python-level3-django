from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Workspace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="Codveda Workspace",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="workspace",
            options={
                "permissions": [
                    (
                        "access_member_dashboard",
                        "Can access the member dashboard",
                    )
                ]
            },
        ),
    ]
