from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

def get_navigation_links(active_page):
    """Generate navigation links with the correct active page"""
    links = [
        {'name': 'Home', 'url': '/', 'active': False},
        {'name': 'Posts', 'url': '/blog/posts/', 'active': False},
        {'name': 'About', 'url': '/blog/about/', 'active': False},
        {'name': 'Contact', 'url': '/blog/contact/', 'active': False},
    ]
    
    # Set the active page
    for link in links:
        if link['name'].lower() == active_page.lower():
            link['active'] = True
    
    return links

def main_view(request):
    return render(request, 'my_site/index.html', {
        'url': 'blog',
        'links': get_navigation_links('Home')
    })
