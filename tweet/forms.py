from django import forms
from .models import Tweet, Like, Comment


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
        fields = ("content","image","video")