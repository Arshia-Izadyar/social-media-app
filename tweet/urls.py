from django.urls import path
from .views import (CreateTweet,
                    ListTweet,
                    TweetDetails,
                    AddLike,
                    AddComment,
                    AddCommentLike,
                    AddToBookMark,
                    DeleteTweet,
                    DeleteComment,
                    UpdateTweet,
                    AddRetweet)

urlpatterns = [
    path("tweet/", CreateTweet.as_view(), name="tweet"),
    path("edit/<int:pk>", UpdateTweet.as_view(), name="update"),
    path("home/", ListTweet.as_view(), name="home"),
    path("<slug:username>/status/<int:pk>/", TweetDetails.as_view(), name="detail"),
    path("like/", AddLike.as_view(), name="like"),
    path("comment/", AddComment.as_view(), name="comment"),
    path("comment-like/", AddCommentLike.as_view(), name="comment-like"),
    path("bookmark/", AddToBookMark.as_view(), name="bookmark"),
    path("retweet/<slug:username>/<int:pk>/", AddRetweet.as_view(), name="retweet"),
    path("delete/<int:pk>", DeleteTweet.as_view(), name="delete"),
    path("comment/delete/<int:pk>", DeleteComment.as_view(), name="delete-comment"),

]
