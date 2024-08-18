from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_tester2 = User.objects.create_user(username='tester2',password='somepassword')
        
    def test_landing(self):
        post_001 = Post.objects.create(
            title="First Post",
            content='this is the first content',
            author=self.user_tester2
        )

        post_002 = Post.objects.create(
            title="Second Post",
            content='this is the second content',
            author=self.user_tester2
        )

        post_003 = Post.objects.create(
            title="Third Post",
            content='this is the third content',
            author=self.user_tester2
        )

        post_004 = Post.objects.create(
            title="Forth Post",
            content='this is the forth content',
            author=self.user_tester2
        )

        response = self.client.get('')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn(post_001.title, body.text)
        self.assertIn(post_002.title, body.text)
        self.assertIn(post_003.title, body.text)
        self.assertIn(post_004.title, body.text)
    

# Create your tests here.
