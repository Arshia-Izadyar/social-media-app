from django.urls import path
from .views import CreateTweet, ListTweet, TweetDetails, AddLike, AddComment, AddCommentLike, AddToBookMark, DeleteTweet

urlpatterns = [
    path("create/", CreateTweet.as_view(), name="tweet"),
    path("home/", ListTweet.as_view(), name="home"),
    path("<slug:username>/status/<int:pk>/", TweetDetails.as_view(), name="detail"),
    path("like/", AddLike.as_view(), name="like"),
    path("comment/", AddComment.as_view(), name="comment"),
    path("comment-like/", AddCommentLike.as_view(), name="comment-like"),
    path("bookmark/", AddToBookMark.as_view(), name="bookmark"),
    path("delete/<int:pk>", DeleteTweet.as_view(), name="delete"),
]
