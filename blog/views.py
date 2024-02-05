from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from blog.models import Post


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


@login_required
def user_profile(request, username):
    posts = Post.objects.filter(author__username=username)
    first_name = posts[0].author.first_name
    last_name = posts[0].author.last_name
    return render(request, "blog/user_posts.html", {"posts": posts,
                                                    "first_name":first_name,
                                                    "last_name":last_name})


@login_required
def logout_view(request):
    messages.info(request,f"{request.user.username} user successfulley loged out")
    logout(request)
    return redirect("blog:home-page")
