from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView

def get_navigation_links(active_page):
    """Generate navigation links with the correct active page"""
    links = [
        {'name': 'Home', 'url': '/', 'active': False},
        {'name': 'Posts', 'url': '/blog/posts', 'active': False},
        {'name': 'Add Post', 'url': '/blog/add_post', 'active': False},
        {'name': 'Add Author', 'url': '/blog/add_author', 'active': False},
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

class BlogMainView(View):
    def get(self, request):
        return render(request, 'my_site/index.html', {
        'url': 'blog',
        'links': get_navigation_links('Home')
    })
    

