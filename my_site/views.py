from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from blog.models import BlogPost

def get_navigation_links(active_page, user=None):
    """Generate navigation links with the correct active page"""
    links = [
        {'name': 'Home', 'url': '/', 'active': False},
        {'name': 'Posts', 'url': '/blog/posts', 'active': False}, 
        {'name': 'Add Post', 'url': '/blog/add_post', 'active': False},
        {'name': 'Add Author', 'url': '/blog/add_author', 'active': False},
        {'name': 'About', 'url': '/blog/about', 'active': False},
        {'name': 'Contact', 'url': '/blog/contact', 'active': False},
    ]
    
    # Add authentication-specific links
    if user and user.is_authenticated:
        links.append({'name': 'Logout', 'url': '/blog/logout', 'active': False})
    else:
        links.extend([
            {'name': 'Log In', 'url': '/blog/login', 'active': False},
            {'name': 'Sign Up', 'url': '/blog/signup', 'active': False},
        ])
    
    # Set the active page
    for link in links:
        if link['name'].lower() == active_page.lower():
            link['active'] = True
        else:
            link['active'] = False
    
    return links

class BlogMainView(View):
    def get(self, request):
        # Get the latest 3 posts for featured section
        featured_posts = BlogPost.objects.select_related('author').order_by('-created_at')[:3]
        
        return render(request, 'my_site/index.html', {
        'url': 'blog',
        'links': get_navigation_links('Home', request.user),
        'post_count': BlogPost.objects.count(),
        'featured_posts': featured_posts,
    })
    

