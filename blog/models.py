from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

from blog.utils import avatar_path


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractModel):
    avatar = models.ImageField(upload_to=avatar_path, default='avatar.JPG')

    @property
    def post_count(self):
        return self.posts.count()


class Post(AbstractModel):
    title = models.CharField(max_length=128)
    content = models.TextField()
    published = models.DateField()
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey("blog.User", CASCADE, "posts")
    def __str__(self):
        return self.title
