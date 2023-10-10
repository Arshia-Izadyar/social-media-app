from django.contrib import admin

# Register your models here.
from .models import Tweet, Like, Comment, CommentLike, Retweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    search_fields = ("author__username",)
    list_display = ("id", "author", "created_at")
    order_by = ("-created_time")


@admin.register(Like)
class TweetAdmin(admin.ModelAdmin):
    search_fields = ("author__username",)
    list_display = ("id", "author")


@admin.register(Comment)
class TweetAdmin(admin.ModelAdmin):
    search_fields = ("author__username",)
    list_display = ("id", "author", "created_at", "tweet")


@admin.register(CommentLike)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "comment")


@admin.register(Retweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ("id", "original_tweet", "created_at")
