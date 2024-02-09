from django.urls import path

from blog.views import HomePageView, AboutView, NewPostView, UserPostView, PostDetailView, home_page, post_detail, \
    user_profile, logout_view, login_view, register_view, post_create, post_update, post_delete

app_name = 'blog'
urlpatterns = [
    path('', home_page, name="home-page"),
    path('login/', login_view, name="login-page"),
    path('register/', register_view, name="register-page"),
    path('logout/', logout_view, name="logout"),
    path('about/', AboutView.as_view(), name="about"),
    path('new-post/', post_create, name="new-post"),
    path('post-detail/<int:pk>', post_detail, name="post-detail"),
    path('post-update/<int:pk>', post_update, name="post-update"),
    path('post-delete/<int:pk>', post_delete, name="post-delete"),
    path('user-post/<str:username>', user_profile, name="user-profile")

]
