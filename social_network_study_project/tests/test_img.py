from django.test import Client, TestCase
#from django import forms
from posts.models import Post
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache

User = get_user_model()

class Image_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'sarah', email = 'connor.s@skynet.com',
            password = '12345')
        self.post = Post.objects.create(
            text = "You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author = self.user
            )
        self.client.force_login(self.user)
        with open('media/posts/1.jpg','rb') as img:
            self.client.post(
                reverse('post_edit', kwargs = {"username": self.user.username, "post_id": self.post.id}),
                data = {"text": "post with image", "image": img, "author": self.user},
                follow=True
            )
    def test_tags_img(self):
        
        #cache.clear()
       # post = Post.objects.get(text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!")
        test_urls = [
            reverse(
                "post", 
                kwargs = {"username": self.user.username, "post_id": self.post.id}
            ),
            reverse('index'),
            reverse('profile',kwargs = {"username": self.user.username, })
        ]
        for ur in test_urls:
            response = self.client.get(ur)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<img", msg_prefix=ur)

    def test_upl_nonimg(self):
        with open('media/posts/2.txt', 'rb') as img:
            self.client.post(reverse('new'),
                data = {"text": "post with non-image", "image": img, "author": self.user},
                follow=True)
        
        try:
            post = Post.objects.get(text = "post with non-image")
            flag = False
        except Exception:
            flag = True
        self.assertTrue(flag)

            
        #self.assert