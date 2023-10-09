# Generated by Django 4.2 on 2023-10-09 08:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tweet", "0003_retweet_like_comment_tweet_retweets"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="like",
            unique_together={("tweet", "author")},
        ),
    ]
