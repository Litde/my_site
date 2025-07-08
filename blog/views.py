from django.shortcuts import render
from django.http import HttpResponse
from my_site.views import main_view

posts = [
    {'id': 1, 'title': 'Building a Complete Django Blog Application', 'content': 'Learn how to create a full-featured blog application using Django, including user authentication, post management, and a beautiful frontend. This comprehensive guide covers everything from setup to deployment.'},
    {'id': 2, 'title': 'Understanding Django Models and Migrations', 'content': 'Dive deep into Django models and migrations. This post explains how to define models, create migrations, and manage your database schema effectively in a Django project.'},
    {'id': 3, 'title': 'Creating Custom Django Admin Interfaces', 'content': 'Enhance your Django admin interface with custom views and actions. This article shows you how to tailor the admin experience to better suit your application needs.'},
    {'id': 4, 'title': 'Django REST Framework: Building APIs with Ease', 'content': 'Explore how to build RESTful APIs using Django REST Framework. This post covers serializers, viewsets, and how to handle authentication and permissions in your API.'},
    {'id': 5, 'title': 'Deploying Django Applications on Heroku', 'content': 'Learn the steps to deploy your Django application on Heroku. This guide includes setting up a PostgreSQL database, configuring static files, and managing environment variables.'},
    {'id': 6, 'title': 'Testing Django Applications: Best Practices', 'content': 'Understand the importance of testing in Django applications. This post discusses unit tests, integration tests, and how to use Django’s testing framework effectively.'},  
    {'id': 7, 'title': 'Django Security Best Practices', 'content': 'Security is crucial in web applications. This article outlines best practices for securing your Django application, including CSRF protection, secure password storage, and more.'},
    {'id': 8, 'title': 'Using Django Signals for Decoupled Applications', 'content': 'Learn how to use Django signals to create decoupled applications. This post explains the concept of signals and how to implement them in your Django projects.'},
]

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
    return render(request, 'blog/posts.html', {
        'url': 'blog',
        'links': get_navigation_links('Posts'),
        'posts': posts,  # Pass the posts data to template
    })

def posts_view(request, post_id):
    try:
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
