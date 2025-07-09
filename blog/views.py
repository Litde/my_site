from django.shortcuts import render
from django.http import HttpResponse
from my_site.views import main_view
from .models import BlogPost  



def get_navigation_links(active_page):
    """Generate navigation links with the correct active page"""
    links = [
        {'name': 'Home', 'url': '/', 'active': False},
        {'name': 'Posts', 'url': '/blog/posts', 'active': False},
        {'name': 'About', 'url': '/blog/about', 'active': False},
        {'name': 'Contact', 'url': '/blog/contact', 'active': False},
    ]
    
    # Set the active page
    for link in links:
        if link['name'].lower() == active_page.lower():
            link['active'] = True
        else:
            link['active'] = False
    
    return links

def blog_main_view(request):
    return main_view(request)

def about_view(request):
    return render(request, 'blog/about.html', {
        'url': 'blog',
        'links': get_navigation_links('About'),
    })

def contact_view(request):
    return render(request, 'blog/contact.html', {
        'url': 'blog',
        'links': get_navigation_links('Contact'),
    })


def posts_main_view(request):
    posts = BlogPost.objects.all()
    if not posts:   
        return render(request, 'blog/posts.html', {
            'url': 'blog',
            'links': get_navigation_links('Posts'),
            'posts': [],  # Pass an empty list if no posts are available
        })
    
    return render(request, 'blog/posts.html', {
        'url': 'blog',
        'links': get_navigation_links('Posts'),
        'posts': posts,  # Pass the posts data to template
    })

def posts_view(request, post_id):
    try:
        posts = BlogPost.objects.all().values('id', 'title', 'content')  # Fetch posts from the database
        if not posts:
            return posts_main_view(request)
        
        post_id = int(post_id)
        post = next((post for post in posts if post['id'] == post_id), None)
        if post is None:
            return posts_main_view(request)

        return render(request, 'blog/post_text_template.html', {
            'url': 'blog',
            'links': get_navigation_links('Posts'),
            'article_title': post['title'],
            'article_text': post['content'],
            'article_date': 'January 2025',  # You can add dates to your posts data later
            'article_author': 'Blog Author',  # You can add authors to your posts data later
        })
    except (ValueError, TypeError):
        return posts_main_view(request)
