# Generated by Django 4.2 on 2023-10-10 05:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tweet", "0009_tweet_retweetss"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tweet",
            name="retweetss",
        ),
    ]