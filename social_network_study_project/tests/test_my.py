from django.test import Client, TestCase
from django import forms
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class My_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'sarah', email = 'connor.s@skynet.com',
            password = '12345')
        self.post = Post.objects.create(
            text = "You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user)
        
        
        
    def test_profile(self):
        response = self.client.get("/sarah/")
        self.assertEqual(response.status_code, 200)
        #print(response.context)
        self.assertEqual(response.context["post_num"],1)
        self.assertIsInstance(response.context["Author"], User)
        self.assertEqual(response.context["Author"].username, self.user.username)

    def test_new_post_create(self):
        self.client.login(username = 'sarah', password = '12345')
        response = self.client.post("/new/", {"text": "sss"},follow=True)
        self.assertRedirects(response=response,expected_url='/')
        response = self.client.get("/sarah/")
        self.assertEqual(response.context["post_num"],2)
        posts = response.context['page']
        check = False
        for p in posts:
            if p.text == 'sss':
                check = True
        self.assertTrue(check)

    def test_new_post_guest(self):
        self.client.logout()
        response = self.client.post("/new/", {"text": "ssssss"},follow=True)
        self.assertRedirects(response=response,expected_url='/auth/login/?next=/new/')
    def test_view_new_post(self):
        test_urls = ['/', '/sarah/']
        for ur in test_urls:
            response = self.client.get(ur)
            posts = response.context['page']
            self.assertIn(self.post,posts)
        response = self.client.get(f'/sarah/{self.post.id}/')
        post = response.context['post']
        self.assertEqual(post, self.post)
    
    def test_edit(self):
             
        self.client.login(username = 'sarah', password = '12345')
        response = self.client.get('/sarah/')
        posts = response.context['page']
        new_p = posts[0]
        
        response = self.client.post(f"/sarah/{new_p.id}/edit/", {"text": "ddd"},follow=True)
        test_urls = ['/', '/sarah/']
        for ur in test_urls:
            response = self.client.get(ur)
            posts = response.context['page']
            
            self.assertEqual(posts[0].text,'ddd')
        response = self.client.get(f'/sarah/{new_p.id}/')
        self.assertEqual(response.context['post'].text, 'ddd')

class Test_404(TestCase):
    def setUp(self):
        self.client = Client()
    def test_page_not_found(self):
        response = self.client.get('/1/1/')
        self.assertEqual(response.status_code, 404)

    
        
