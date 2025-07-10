from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import BlogPost, Author, Tag  
from .forms import NewPostForm, NewAuthorForm, LoginForm, RegisterForm
from django.views import View
from django.views.generic import ListView


class BlogMainView(View):
    def get(self, request):
        return render(request, 'blog/index.html', {
            'url': 'blog',
            'links': get_navigation_links('Home', request.user),
        })


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

# def blog_main_view(request):
#     return main_view(request)

def about_view(request):
    return render(request, 'blog/about.html', {
        'url': 'blog',
        'links': get_navigation_links('About', request.user),
    })

def contact_view(request):
    return render(request, 'blog/contact.html', {
        'url': 'blog',
        'links': get_navigation_links('Contact', request.user),
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
        context['links'] = get_navigation_links('Posts', self.request.user)
        return context
    

class BlogPostDetailView(View):
    def get(self, request, post_id):
        try:
            # Fetch the specific post with related author
            post = BlogPost.objects.select_related('author').get(id=post_id)
            
            return render(request, 'blog/post_text_template.html', {
                'url': 'blog',
                'links': get_navigation_links('Posts', request.user),
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
        'links': get_navigation_links('Add Post', request.user),
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
        'links': get_navigation_links('Add Author', request.user),
        'form': form,
    })

def login_view(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or username}!')
                return redirect('blog:posts')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'blog/login.html', {
        'url': 'blog',
        'links': get_navigation_links('Log In', request.user),
        'form': form,
    })

def signup_view(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Create the user
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password']
                )
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('blog:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'blog/signup.html', {
        'url': 'blog',
        'links': get_navigation_links('Sign Up', request.user),
        'form': form,
    })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('blog:login')

