from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Q, Count
from django.db import IntegrityError

from .forms import TweetForm, LikeForm, CommentForm
from .models import Tweet, Like, Comment

class CreateTweet(CreateView):
    form_class = TweetForm
    success_url = "/"

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
        qs = Tweet.objects.prefetch_related("likes").filter(author__in=user.following.all())
        qs = qs.annotate(like_count=Count("likes"))
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["user"] = self.request.user
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
        if len(qs) ==0 :
            return HttpResponseRedirect("/home")
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tweet = ctx["tweet"]
        ctx["comment_form"] = CommentForm()
        ctx["like_count"] = Like.objects.filter(tweet=tweet).count() 
        ctx["tweet_comments"] = tweet.comments.all()
        return ctx

class AddLike(View):
    def post(self, request, *args, **kwargs):
        form = LikeForm(request.POST)
        try:
            if form.is_valid():
                like = form.save(commit=False)
                like.author = request.user
                like.save()
                return HttpResponseRedirect(request.POST.get("next", "/home"))
        except IntegrityError:
            l = Like.objects.filter(Q(author=like.author) & Q(tweet=like.tweet)).first()
            l.delete()
            return HttpResponseRedirect(request.POST.get("next", "/home"))
    
class AddComment(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST,request.FILES)
        tweed_id = request.POST.get("tweet")
        
        if form.is_valid():
            print(form.cleaned_data)
            comment = form.save(commit=False)
            comment.author = request.user
            tweet = Tweet.objects.get(pk=tweed_id)
            comment.tweet = tweet
            a = request.POST.get("parent_comment", None)
            print()
            print()
            print(a)
            b= Comment.objects.filter(Q(pk=a)&Q(tweet=tweet)).first()
            print(b)
            
            comment.parent_comment = b
          
            comment.save()
            return HttpResponseRedirect(request.POST.get("next", "/home"))
        else:
            raise Http404
 