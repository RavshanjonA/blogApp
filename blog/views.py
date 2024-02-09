import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from blog.forms import LoginForm, UserRegistrationForm, PostCreateForm, PostUpdateForm
from blog.models import Post, User


class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class NewPostView(TemplateView):
    template_name = "blog/post_form.html"


class UserPostView(TemplateView):
    template_name = "blog/user_posts.html"


class PostDetailView(TemplateView):
    template_name = "blog/post_detail.html"


def home_page(request):
    if request.user.is_authenticated:
        posts = Post.objects.exclude(author=request.user).filter(is_active=True).order_by("published")
    else:
        posts = Post.objects.all().filter(is_active=True).order_by("published")

    return render(request, "blog/home.html", context={"posts": posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required()
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = Post(title=form.cleaned_data["title"], content=form.cleaned_data["content"],
                        is_active=form.cleaned_data["is_active"])
            post.author = request.user
            post.published = datetime.datetime.now().strftime("%Y-%m-%d")
            post.save()
            messages.success(request, "post successfully created")
            return redirect(reverse('blog:user-profile', kwargs={"username": request.user.username}))
        else:
            return render(request, "blog/post_form.html", {"form": form})
    else:
        form = PostCreateForm()
        return render(request, "blog/post_form.html", {"form": form})


@login_required()
def post_update(request, pk: int):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostUpdateForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "post successfully updated")
            return redirect(reverse('blog:post-detail', kwargs={"pk": post.id}))
        else:
            return render(request, "blog/post_update.html", {"form": form})
    else:
        form = PostUpdateForm(instance=post)
        return render(request, "blog/post_update.html", {"form": form})


@login_required()
def post_delete(requet, pk):
    post = get_object_or_404(Post, pk=pk)
    if requet.method == "POST":
        messages.success(requet, "post successfully deleted")
        post.delete()
        return redirect(reverse('blog:user-profile', kwargs={"username": requet.user.username}))
    else:
        return render(requet, "blog/post_confirm_delete.html", {"post": post})


# @login_required
def user_profile(request, username):
    posts = Post.objects.filter(author__username=username)
    user = get_object_or_404(User, username=username)
    first_name = user.first_name
    last_name = user.last_name
    return render(request, "blog/user_posts.html", {"posts": posts,
                                                    "first_name": first_name,
                                                    "last_name": last_name})


@login_required
def logout_view(request):
    messages.info(request, f"{request.user.username} user successfulley loged out")
    logout(request)
    return redirect("blog:home-page")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                messages.success(request, "user succesfully loged in")
                return redirect("blog:home-page")
            else:
                messages.warning(request, "User not found")
                return redirect("blog:login-page")
        else:
            return render(request, "blog/login.html", {"form": form})

    else:
        form = LoginForm()
    return render(request, "blog/login.html", {"form": form})


def register_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully registered")
            return redirect('blog:login-page')
        else:
            return render(request, "blog/register.html", {"form": form})
    else:
        return render(request, "blog/register.html", {"form": form})
