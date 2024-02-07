import datetime

from django.test import TestCase
from django.urls import reverse

from blog.models import User, Post


class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(first_name="Jahongir",
                                   last_name="Pulatov",
                                   username="jahongir",
                                   email="jahongir2@gmail.com")
        user.set_password("testpass")
        user.save()
        self.user = user
        user2 = User.objects.create(first_name="Ahrorjon",
                                    last_name="Hoshimjonov",
                                    username="ahrorjon",
                                    email="ahrorjon@gmail.com")
        user2.set_password("testpass")
        user2.save()
        self.user2 = user2
        post = Post.objects.create(title="Post1",
                                   content="Content1",
                                   author=self.user,
                                   published=datetime.datetime.now().date().strftime("%Y-%d-%m"),
                                   is_active=True
                                   )
        self.post = post

    def test_post_detail(self):
        response = self.client.get(reverse('blog:post-detail', kwargs={"pk": self.post.id}))
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.author.first_name)
        self.assertContains(response, self.post.author.last_name)

    def test_post_inactive_detail(self):
        pass
        # self.assertNotContains()

    def test_user_profile_post_title(self):
        pass

    def test_no_post_profile(self):
        self.client.login(username=self.user2.username, password="testpass")
        response = self.client.get(reverse("blog:user-profile", kwargs={"username": self.user2.username}))
        self.assertContains(response, "No Post")
