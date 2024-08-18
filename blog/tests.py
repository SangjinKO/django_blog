from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment

# Create your tests here.

class TestView(TestCase):

    def setUp(self):
        print("TEST start: setUp")
        self.client = Client()
        self.user_tester1 = User.objects.create_user(username='tester1', password='somepassword')
        self.user_tester2 = User.objects.create_user(username='tester2', password='somepassword')
        self.user_tester2.is_staff = True
        self.user_tester2.save()

        self.category_catA = Category.objects.create(name='catA',slug='catA')
        self.category_catB = Category.objects.create(name='catB',slug='catB')
        self.tag_tagA = Tag.objects.create(name='에이',slug='에이')
        self.tag_tagB = Tag.objects.create(name='tagB',slug='tagB')
        self.tag_tagC = Tag.objects.create(name='tagC',slug='tagC')

        self.post_001 = Post.objects.create(
            title="First Post",
            content='this is the first content',
            category=self.category_catA,
            author=self.user_tester1
        )
        self.post_001.tags.add(self.tag_tagC)

        self.post_002 = Post.objects.create(
            title="Second Post",
            content='this is the second content',
            category=self.category_catB,
            author=self.user_tester2
        )

        self.post_003 = Post.objects.create(
            title="Third Post",
            content='this is NO category content',
            author=self.user_tester2
        )
        self.post_003.tags.add(self.tag_tagA)
        self.post_003.tags.add(self.tag_tagB)

        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_tester1,
            content="this is the first comment."
        )

        print("TEST finish: setUp")
    
    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_catA.name} ({self.category_catA.post_set.count()})',categories_card.text)
        self.assertIn(f'{self.category_catB.name} ({self.category_catB.post_set.count()})',categories_card.text)
        self.assertIn(f'Unclassified (1)',categories_card.text)

    def navbar_test(self, soup):
        print("TEST start: navi")
        navbar = soup.nav 
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # logo_btn = navbar.find('a',text="Sangjin's Home")
        # self.assertEqual(logo_btn.attrs['href'],'/')

        home_btn = navbar.find("a",text="Home")
        self.assertEqual(home_btn.attrs['href'],'/')

        blog_btn = navbar.find("a",text="Blog")
        self.assertEqual(blog_btn.attrs['href'],'/blog/')

        about_me_btn = navbar.find("a",text="About Me")
        self.assertEqual(about_me_btn.attrs['href'],'/about_me/')

        print("TEST finish: navi")
       

    def test_post_list(self):
        print("TEST start: post_list")
        # with 3 posts
        self.assertEqual(Post.objects.count(),3)

        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area=soup.find('div', id='main-area')
        self.assertNotIn("There is no post yet",main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_tagC.name, post_001_card.text)
        self.assertNotIn(self.tag_tagA.name, post_001_card.text)
        self.assertNotIn(self.tag_tagB.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_tagC.name, post_002_card.text)
        self.assertNotIn(self.tag_tagA.name, post_002_card.text)
        self.assertNotIn(self.tag_tagB.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('Unclassified', post_003_card.text)
        self.assertNotIn(self.tag_tagC.name, post_003_card.text)
        self.assertIn(self.tag_tagA.name, post_003_card.text)
        self.assertIn(self.tag_tagB.name, post_003_card.text)

        self.assertIn(self.user_tester1.username.upper(), main_area.text)
        self.assertIn(self.user_tester2.username.upper(), main_area.text)

        # with 0 posts
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(),0)
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        main_area=soup.find('div', id='main-area')
        self.assertIn("There is no post yet",main_area.text)

        print("TEST finish: post_list")

    def test_post_detail(self):
        print("TEST start: post_detail")
        # post_000 = Post.objects.create(
        #     title="First Post",
        #     content='this is the first content',
        #     author=self.user_tester1,
        # )
        # self.assertEqual(Post.objects.count(),1)
        self.assertEqual(self.post_001.get_absolute_url(),'/blog/1/')

        print("TEST start: elements")
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title,soup.title.text)

        main_area=soup.find('div', id='main-area')
        post_area=soup.find('div', id='post-area')        
        self.assertIn(self.post_001.title,post_area.text)
        self.assertIn(self.category_catA.name, post_area.text)
        
        self.assertIn(self.user_tester1.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_tagC.name, post_area.text)
        self.assertNotIn(self.tag_tagA.name, post_area.text)
        self.assertNotIn(self.tag_tagB.name, post_area.text)
        
        #comment
        comments_area = soup.find('div', id="comment-area")
        comment_001_area = comments_area.find('div', id="comment-1")
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

        print("TEST finish: post_detail")

    def test_category_page(self):
        print("TEST start: category_page")
        response = self.client.get(self.category_catA.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_catA.name, soup.h1.text)

        main_area = soup.find('div',id='main-area')
        self.assertIn(self.category_catA.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        print("TEST finish: category_page")

    def test_tag_page(self):
        print("TEST start: tag_page")
        response = self.client.get(self.tag_tagC.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_tagC.name, soup.h1.text)

        main_area = soup.find('div',id='main-area')
        self.assertIn(self.tag_tagC.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        print("TEST finish: tag_page")

    def test_create_post(self):
        print("TEST start: create_post")
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='tester1', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        
        self.client.login(username='tester2', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')        

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div',id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'new post creation',
                'content': "let's create a new post!",
                'tags_str': 'new tag; 한글 태그, tagB' #existing tags: 에이, tagB, tagC
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title,'new post creation')
        self.assertEqual(last_post.author.username,'tester2')

        self.assertEqual(last_post.tags.count(),3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(),5)
        print("TEST finish: create_post")
        

    def test_update_post(self):
        print("TEST start: update_post")
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        response = self.client.get(update_post_url)
        # case1: not logged in
        self.assertNotEqual(response.status_code, 200) 

        # case2: diff author(tester1) *p003 author: tester2
        self.assertNotEqual(self.post_003.author, self.user_tester1)
        self.client.login(
            username=self.user_tester1.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # case3: author(tester2)
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        
        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('에이; tagB',tag_str_input.attrs['value']) #post_003 tags: 에이, tagB

        response = self.client.post(
            update_post_url,
            {
                'title': 'The third post update',
                'content': 'updated the third post',
                'category': self.category_catB.pk,
                'tags_str': '에이; 한글태그, some tag'
            },
            follow=True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('The third post update',main_area.text)
        self.assertIn('updated the third post',main_area.text)
        self.assertIn(self.category_catB.name,main_area.text)
        self.assertIn('에이', main_area.text)
        self.assertIn('한글태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('tagB', main_area.text)
        print("TEST finish: update_post")

    def test_comment_form(self):
        print("TEST start: comment_form")
        self.assertEqual(Comment.objects.count(),1)
        self.assertEqual(self.post_001.comment_set.count(),1)

        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content,'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment',comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        #after log in
        self.client.login(username='tester1', password='somepassword')
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content,'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment',comment_area.text)
        
        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea',id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': "comments from tester1.",
            },
            follow=True
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(self.post_001.comment_set.count(),2)

        new_comment = Comment.objects.last()
        soup=BeautifulSoup(response.content,'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div',id=f'comment-{new_comment.pk}')
        self.assertIn('tester1', new_comment_div.text)
        self.assertIn('comments from tester1.', new_comment_div.text)
        print("TEST finish: comment_form")

    def test_comment_update(self):
        print("TEST start: comment_update")
        comment_by_tester2 = Comment.objects.create(
            post=self.post_001,
            author=self.user_tester2,
            content='comment written by tester2.'
        )
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        self.client.login(username='tester1', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content, 'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        response=self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': "change the comment from tester1.",
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('change the comment from tester1.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)
        print("TEST finish: comment_update")
    
    def test_comment_delete(self):
        print("TEST start: comment_delete")
        comment_by_tester2 = Comment.objects.create(
            post=self.post_001,
            author=self.user_tester2,
            content='comment written by tester2.'
        )
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(self.post_001.comment_set.count(),2)

        #w/o login
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content, 'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        #w/ login: tester2
        self.client.login(username='tester2', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup=BeautifulSoup(response.content, 'html.parser')
        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        comment_002_delete_modal_btn = comment_area.find('a', id='comment-2-delete-modal-btn')
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        self.assertEqual(comment_002_delete_modal_btn.attrs['data-target'],'#deleteCommentModal-2')

        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete',really_delete_btn_002.text)
        self.assertEqual(really_delete_btn_002.attrs['href'],'/blog/delete_comment/2/')

        response = self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(self.post_001.title, soup.title.text)
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('comment written by tester2.', comment_area.text)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(),1)

        print("TEST finish: comment_delete")
    def test_search(self):
        post_about_python = Post.objects.create(
            title = 'This is the post about 에이.',
            content='Hellow World. We are the world.',
            author=self.user_tester2
        )

        response = self.client.get('/blog/search/에이/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        self.assertIn('Search: 에이 (2)', main_area.text) # POST_003.tag & post_about_python.title
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text) # tags
        self.assertIn(post_about_python.title, main_area.text) # title

        
        
            
        


        

        






