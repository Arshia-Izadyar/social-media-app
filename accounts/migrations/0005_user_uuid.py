# Generated by Django 4.2 on 2023-10-11 07:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_user_is_verified_alter_user_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, verbose_name="UUID"),
        ),
    ]
