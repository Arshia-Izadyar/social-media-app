from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView,View
from django.db.models import Q, Count
from django.db import IntegrityError, models
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TweetForm, LikeForm, CommentForm, CommentLikeForm, BookmarkForm, RetweetForm, UpdateProfileForm
from .models import Tweet, Like, Comment, CommentLike, BookMark, Retweet


class CreateTweet(CreateView):
    form_class = TweetForm
    success_url = reverse_lazy("home")

    template_name = "tweet/create_tweet.html"

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.author = self.request.user
        tweet.save()
        return HttpResponseRedirect(self.success_url)


class ListTweet(ListView):
    context_object_name = "tweets"
    template_name = "tweet/list_tweet.html"

    def get_queryset(self):
        user = self.request.user
        user_following_list = user.following.all()

        qs = Tweet.objects.filter(
            Q(author__in=user_following_list)
        ).prefetch_related("likes").order_by("created_at")

        qs = qs.annotate(like_count=Count("likes"))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["user"] = self.request.user

        retweets = Retweet.objects.filter(user__in=self.request.user.following.all()).order_by("created_at")

        ctx["retweets"] = retweets

        return ctx


class TweetDetails(DetailView):
    context_object_name = "tweet"
    template_name = "tweet/detail_tweet.html"

    def get_queryset(self):
        username = self.kwargs["username"]
        pk = self.kwargs["pk"]
        qs = Tweet.objects.filter(Q(author__username=username) & Q(pk=pk))
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if len(qs) == 0:
            return HttpResponseRedirect(reverse_lazy("home"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tweet = ctx["tweet"]
        ctx["comment_form"] = CommentForm()
        ctx["like_count"] = Like.objects.filter(tweet=tweet).count()
        tweet_comments = tweet.comments.prefetch_related("comment_likes").all()
        usr_bookmarks = self.request.user.bookmarks.filter(tweet=tweet)
        ctx["bookmark"] = usr_bookmarks.exists()

        ctx["tweet_comments"] = tweet_comments
        return ctx


class DeleteTweet(DeleteView):
    model = Tweet
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        qs = Tweet.objects.filter(pk=pk)
        if qs.exists() and qs.first().author == request.user:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404


class DeleteComment(DeleteView):
    model = Comment

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        qs = Comment.objects.filter(pk=pk)
        self.success_url = request.POST.get("next", reverse_lazy("home"))
        if qs.exists() and qs.first().author == request.user:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404


class AddLike(View):
    def post(self, request, *args, **kwargs):
        form = LikeForm(request.POST)
        try:
            if form.is_valid():
                like = form.save(commit=False)
                like.author = request.user
                like.save()
                return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
        except IntegrityError:
            l = Like.objects.filter(Q(author=like.author) & Q(tweet=like.tweet)).first()
            l.delete()
            return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))


class AddComment(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        tweed_id = request.POST.get("tweet")

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            tweet = Tweet.objects.get(pk=tweed_id)
            comment.tweet = tweet
            comment_id = request.POST.get("parent_comment", None)
            parent_comment = Comment.objects.filter(Q(pk=comment_id) & Q(tweet=tweet)).first()

            comment.parent_comment = parent_comment
            comment.save()
            return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
        else:
            raise Http404


class AddCommentLike(View):
    def post(self, request, *args, **kwargs):
        form = CommentLikeForm(request.POST)
        try:
            if form.is_valid():
                like = form.save(commit=False)
                like.author = request.user
                like.save()
                return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
            raise Http404
        except IntegrityError:
            l = CommentLike.objects.filter(Q(author=like.author) & Q(comment=like.comment)).first()
            l.delete()
            return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))


class AddToBookMark(View):
    def post(self, request, *args, **kwargs):
        form = BookmarkForm(request.POST)
        try:
            if form.is_valid():
                bookmark = form.save(commit=False)
                bookmark.user = request.user
                bookmark.save()
                return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
            raise Http404
        except IntegrityError:
            b = BookMark.objects.filter(Q(user=request.user) & Q(tweet=bookmark.tweet))
            b.delete()
            return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))


"""    
class UpdateTweet2(UpdateView):
    form_class = TweetForm
    template_name = "tweet/update_tweet.html"
    success_url = "/home"
    model = Tweet
    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Tweet.objects.filter(pk=pk)
    
    
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user and request.user.user_type > 0: # user_type > 0 -> not a free user
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/home")    
"""


class UpdateTweet(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        obj = Tweet.objects.filter(pk=pk).first()
        form_class = TweetForm(instance=obj)
        template_name = "tweet/update_tweet.html"
        if request.user.user_type > 0 and obj.author == request.user:  # user_type > 0 -> not a free user
            return render(request, template_name, {"form": form_class})
        else:
            return HttpResponseRedirect(reverse_lazy("home"))

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        obj = Tweet.objects.filter(pk=pk).first()
        form = TweetForm(request.POST, request.FILES, instance=obj)
        if obj.author != request.user:
            raise Http404
        if form.is_valid():
        
            form.save()
            return HttpResponseRedirect(reverse_lazy("home"))
        raise Http404


class AddRetweet(View):
    def post(self, request, *args, **kwargs):
        form = RetweetForm(request.POST)
        try:
            if form.is_valid():
                retweet = form.save(commit=False)
                retweet.user = request.user
                retweet.save()
                return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
            raise Http404
        except IntegrityError:
            r = Retweet.objects.filter(user=request.user, original_tweet=retweet.original_tweet).first()
            if r is not None:
                r.delete()
                return HttpResponseRedirect(request.POST.get("next", reverse_lazy("home")))
            raise Http404

User = get_user_model()
class ProfileDetail(DetailView):
    model = User
    template_name='accounts/profile.html'
    context_object_name = "user"
    
    
    @method_decorator(login_required(redirect_field_name=reverse_lazy("login-user")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        username = self.kwargs["username"]
        return User.objects.filter(username=username)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        ctx = super().get_context_data(**kwargs)
        ctx["tweets"] = Tweet.objects.filter(author=user).prefetch_related("likes").annotate(like_count=Count("likes")).order_by("created_at")
        ctx["retweets"] = Retweet.objects.filter(user=user).order_by("created_at")
        ctx["comments"] = Comment.objects.filter(author=user).prefetch_related("tweet").annotate(like_count=Count("tweet__likes"))
        return ctx
    
    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)
    

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateProfileForm
    success_url ="/"
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return super().post(request, *args, **kwargs)
        return Http404
    
    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)
    