from django.urls import path

from blog.views import HomePageView, AboutView, NewPostView, UserPostView, PostDetailView, home_page, post_detail, \
    user_profile, logout_view, login_view, register_view, post_create

app_name = 'blog'
urlpatterns = [
    # path('', HomePageView.as_view(), name="home-page"),
    path('', home_page, name="home-page"),
    path('login/', login_view, name="login-page"),
    path('register/', register_view, name="register-page"),
    path('logout/', logout_view, name="logout"),
    path('about/', AboutView.as_view(), name="about"),
    path('new-post/', post_create, name="new-post"),
    path('user-post/', UserPostView.as_view(), name="user-post"),
    path('post-detail/<int:pk>', post_detail, name="post-detail"),
    path('user-post/<str:username>', user_profile, name="user-profile")

]
