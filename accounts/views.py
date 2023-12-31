from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, UpdateView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from tweet.models import Tweet, Comment, Retweet, BookMark


from .forms import CreateUserForm, LoginForm, UpdateProfileForm


User = get_user_model()


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            password1 = cleaned_data["password"]
            password2 = cleaned_data["password2"]
            if password2 != password1:
                form.add_error("password", "passwords dont match")
                return render(request, "accounts/register.html", {"form": form})
            try:
                validate_password(password1)
            except ValidationError as e:
                form.add_error("password", e)
                return render(request, "accounts/register.html", {"form": form})
            hashed_password = make_password(password1)
            user = User.objects.create(
                username=cleaned_data["username"],
                password=hashed_password,
                phone_number=cleaned_data["phone_number"],
                email=cleaned_data["email"],
            )
            user.first_name = cleaned_data["first_name"]
            user.last_name = cleaned_data["last_name"]
            user.save()
            usr = authenticate(username=user.username, password=password1)
            login(request, usr)
            return HttpResponseRedirect(reverse_lazy("home"))
        return render(request, "accounts/register.html", {"form": form})


class UserLogin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("home"))

    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data["username"], form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy("home"))
            return HttpResponseRedirect(reverse_lazy("sign-user"))
        raise Http404


class UserLogout(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("login-user"))

    def get(self, request):
        usr = self.request.user
        user = User.objects.get(username=usr.username)
        logout(request)
        return HttpResponseRedirect(reverse_lazy("login-user"))


class Follow(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        curr_user = get_object_or_404(User, username=request.user.username)
        target_user = request.POST.get("user")
        following = request.POST.get("following")
        if following is not None:
            curr_user.following.remove(target_user)
        else:
            curr_user.following.add(target_user)

        return HttpResponseRedirect(request.POST.get("next", "/home"))


class ShowUsersFollower(ListView):
    template_name = "accounts/follower_list.html"
    context_object_name = "followers"

    @method_decorator(login_required(redirect_field_name=reverse_lazy("login-user")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        username = self.kwargs["username"]
        return User.objects.get(username=username).followers.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.kwargs["username"]
        ctx["user"] = user
        return ctx


class ShowUsersFollowing(ListView):
    template_name = "accounts/following_list.html"
    context_object_name = "followings"

    @method_decorator(login_required(redirect_field_name=reverse_lazy("login-user")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        username = self.kwargs["username"]
        return User.objects.get(username=username).following.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.kwargs["username"]
        ctx["user"] = user
        return ctx


class ActivateAccount(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        uuid = self.kwargs["uuid"]
        user = User.objects.filter(Q(uuid=uuid) & Q(username=username)).first()
        if user is not None:
            user.is_verified = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy("home"))
        raise Http404


class ProfileDetail(DetailView):
    model = User
    template_name = "accounts/profile.html"
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
        ctx["tweets"] = (
            Tweet.objects.filter(author=user)
            .prefetch_related("likes")
            .annotate(like_count=Count("likes"))
            .order_by("created_at")
        )
        ctx["retweets"] = Retweet.objects.filter(user=user).order_by("created_at")
        ctx["comments"] = (
            Comment.objects.filter(author=user).prefetch_related("tweet").annotate(like_count=Count("tweet__likes"))
        )
        return ctx

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateProfileForm

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            update = form.save(commit=False)
            update.save()

            return HttpResponseRedirect(request.POST.get("next"))
        return Http404

    def get_object(self, queryset=None):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)

    def get_initial(self):
        user = self.get_object()
        initial = super(UpdateProfile, self).get_initial()
        initial["bio"] = user.bio
        return initial


class ListBookMarks(ListView):
    context_object_name = "bookmarks"
    template_name = "accounts/bookmarks.html"

    @method_decorator(login_required(redirect_field_name=reverse_lazy("login-user")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        user = get_object_or_404(User, username=username)
        if user.uuid == request.user.uuid:
            print(type(user))
            print(type(self.request.user))
            return super().get(request, *args, **kwargs)
        raise Http404

    def get_queryset(self):
        return BookMark.objects.filter(user=self.request.user)
