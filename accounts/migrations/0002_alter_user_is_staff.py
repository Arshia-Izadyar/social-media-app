# Generated by Django 4.2 on 2023-10-09 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False, verbose_name="Staff"),
        ),
    ]
