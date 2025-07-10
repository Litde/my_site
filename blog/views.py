from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import BlogPost, Author, Tag  
from.forms import NewPostForm, NewAuthorForm
from django.views import View
from django.views.generic import ListView

class BlogMainView(View):
    def get(self, request):
        return render(request, 'blog/index.html', {
            'url': 'blog',
            'links': get_navigation_links('Home'),
        })


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

# def blog_main_view(request):
#     return main_view(request)

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

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'blog'
        context['links'] = get_navigation_links('Posts')
        return context
    

class BlogPostDetailView(View):
    def get(self, request, post_id):
        try:
            # Fetch the specific post with related author
            post = BlogPost.objects.select_related('author').get(id=post_id)
            
            return render(request, 'blog/post_text_template.html', {
                'url': 'blog',
                'links': get_navigation_links('Posts'),
                'article_title': post.title,
                'article_text': post.content,
                'article_date': post.created_at.strftime('%B %d, %Y'),
                'article_author': post.author.full_name(),
                'article_image': post.image.url if post.image else None,
                'post': post,  # Pass the full post object for additional data if needed
            })
        except BlogPost.DoesNotExist: 
            return BlogPostListView.as_view()(request)
        except (ValueError, TypeError):
            return BlogPostListView.as_view()(request)


def add_post_view(request):
    form = NewPostForm()
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Check for duplicate slug
                title = form.cleaned_data['title']
                slug = title.lower().replace(' ', '-')
                
                if BlogPost.objects.filter(slug=slug).exists():
                    messages.error(request, 'A post with this slug already exists. Please choose a different title.')
                else:
                    # Save the post
                    blog_post = form.save()
                    messages.success(request, f'Post "{blog_post.title}" has been created successfully!')
                    return redirect('blog:add_post')
                    
            except Exception as e:
                messages.error(request, f'Error creating post: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    # For GET request or if POST failed, show the form
    return render(request, 'blog/add_post.html', {
        'url': 'blog',
        'links': get_navigation_links('Add Post'),
        'form': form,
    })

def add_author_view(request):
    form = NewAuthorForm()
    
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Author "{author.full_name()}" has been added successfully!')
            return redirect('blog:add_author')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'blog/add_author.html', {
        'url': 'blog',
        'links': get_navigation_links('Add Author'),
        'form': form,
    })

