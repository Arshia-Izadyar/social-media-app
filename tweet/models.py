from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Tweet(models.Model):
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, null=False,
                               related_name="tweets")
    content = models.CharField(max_length=280, verbose_name=_("Content"))
    created_at = models.DateField(auto_now_add=True, verbose_name=_("created_at"))
    modified_at = models.DateField(auto_now=True, verbose_name=_("modified_at"))
    image = models.ImageField(upload_to="./media/uploads", null=True, blank=True, verbose_name=_("Image"))
    video = models.FileField(upload_to="./files", null=True, blank=True, verbose_name=_("video"))

    # retweetss = models.ManyToManyField(User, through='Retweet')

    def __str__(self):
        return f"{self.author} - {self.created_at}"


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retweets")
    original_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="retweets")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.original_tweet}"

    class Meta:
        unique_together = ('user', 'original_tweet')


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_("Author"), null=False, related_name="comments",
                               on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', verbose_name=_("Tweet"), on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey('self', verbose_name=_("Parent Comment"), null=True, blank=True,
                                       on_delete=models.CASCADE, related_name='replies')
    content = models.CharField(max_length=200)
    image = models.ImageField(upload_to="./media/uploads", null=True, blank=True, verbose_name=_("Image"))
    video = models.FileField(upload_to="./files", null=True, blank=True, verbose_name=_("Video"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"{self.author} - {self.created_at} comment"


class Like(models.Model):
    tweet = models.ForeignKey('Tweet', verbose_name=_("Tweet"), on_delete=models.CASCADE, related_name="likes")
    author = models.ForeignKey(User, verbose_name=_("Author"), null=False, related_name="likes",
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tweet', 'author')

    def __str__(self):
        return f"{self.author} liked {self.tweet}"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, verbose_name=_("comment"), on_delete=models.CASCADE,
                                related_name="comment_likes")
    author = models.ForeignKey(User, verbose_name=_("Author"), null=False, related_name="comment_likes",
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'author')

    def __str__(self):
        return f"{self.author} liked {self.comment}"


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        unique_together = ('user', 'tweet')
