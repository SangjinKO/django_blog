from django.shortcuts import render
from blog.models import Post

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )

def my_flix(request):
    return render(
        request,
        'single_pages/my_flix.html'
    )


# Create your views here.
