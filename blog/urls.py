from django.urls import path, include
from . import views as blog_views

app_name = 'blog'  # This creates the namespace

urlpatterns = [
    path('', blog_views.blog_main_view, name='blog_main'),
    path('about/', blog_views.about_view, name='blog_about'),
    path('contact/', blog_views.contact_view, name='blog_contact'),
    path('posts/', blog_views.posts_main_view, name='blog_posts'),
    path('post/<int:post_id>/', blog_views.posts_view, name='post'),
]