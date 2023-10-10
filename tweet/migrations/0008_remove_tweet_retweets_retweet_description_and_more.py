# Generated by Django 4.2 on 2023-10-10 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tweet", "0007_alter_bookmark_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tweet",
            name="retweets",
        ),
        migrations.AddField(
            model_name="retweet",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="retweet",
            name="original_tweet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="retweets",
                to="tweet.tweet",
            ),
        ),
        migrations.AlterField(
            model_name="retweet",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="retweets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
