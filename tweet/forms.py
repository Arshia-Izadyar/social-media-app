from django import forms
from .models import Tweet, Like, Comment, CommentLike, BookMark, Retweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content", "image", "video")


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ["tweet"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", "image", "video")


class CommentLikeForm(forms.ModelForm):
    class Meta:
        model = CommentLike
        fields = ("comment",)


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = BookMark
        fields = ("tweet",)


class RetweetForm(forms.ModelForm):
    class Meta:
        model = Retweet
        fields = ("original_tweet", "description")
