# Generated by Django 4.2 on 2023-10-10 05:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tweet", "0008_remove_tweet_retweets_retweet_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tweet",
            name="retweetss",
            field=models.ManyToManyField(through="tweet.Retweet", to=settings.AUTH_USER_MODEL),
        ),
    ]
