from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'blog/home.html'

class AboutView(TemplateView):
    template_name = 'blog/about.html'
class NewPostView(TemplateView):
    template_name = "blog/post_form.html"
class UserPostView(TemplateView):
    template_name = "blog/user_posts.html"