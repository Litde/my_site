from django.urls import path, include
from . import views as blog_views

app_name = 'blog'  # This creates the namespace

urlpatterns = [
    path('', blog_views.BlogMainView.as_view(), name='home'),
    path('about/', blog_views.about_view, name='about'),
    path('contact/', blog_views.contact_view, name='contact'),
    path('posts/', blog_views.BlogPostListView.as_view(), name='posts'),
    path('post/<int:post_id>/', blog_views.BlogPostDetailView.as_view(), name='post'),
    path('post/<int:post_id>/edit/', blog_views.edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', blog_views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/like/', blog_views.like_post_view, name='like_post'),
    path('add_post/', blog_views.add_post_view, name='add_post'),
    path('add_author/', blog_views.add_author_view, name='add_author'),
    path('login/', blog_views.login_view, name='login'),
    path('signup/', blog_views.signup_view, name='signup'),
    path('logout/', blog_views.logout_view, name='logout'),
]