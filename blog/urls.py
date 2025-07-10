from django.urls import path, include
from . import views as blog_views

app_name = 'blog'  # This creates the namespace

urlpatterns = [
    path('', blog_views.blog_main_view, name='home'),
    path('about/', blog_views.about_view, name='about'),
    path('contact/', blog_views.contact_view, name='contact'),
    path('posts/', blog_views.posts_main_view, name='posts'),
    path('post/<int:post_id>/', blog_views.posts_view, name='post'),
    path('add_post/', blog_views.add_post_view, name='add_post'),
    path('add_author/', blog_views.add_author_view, name='add_author'),
]