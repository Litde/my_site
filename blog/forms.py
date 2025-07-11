from django import forms
from django.contrib.auth.models import User
from blog.models import Author, BlogPost, Tag

class NewPostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False, 
        help_text="Enter tags separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'})
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'excerpt', 'author', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter an engaging title for your post', 'maxlength': 200}),
            'excerpt': forms.Textarea(attrs={'placeholder': 'A brief summary of your post (optional)', 'maxlength': 500, 'rows': 3}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post content here...', 'rows': 10}),
            'author': forms.Select(attrs={'placeholder': 'Select an author'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['title'].required = True
        self.fields['content'].required = True
        self.fields['author'].required = True
        
        # Image is never required (especially when editing existing posts)
        self.fields['image'].required = False
        
        # Populate author choices
        self.fields['author'].queryset = Author.objects.all()
        
        # If editing an existing post, populate tags field and update image help text
        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags'].initial = ', '.join([tag.name for tag in tags])
            
            # Update image field help text for editing
            if self.instance.image:
                self.fields['image'].help_text = "Current image will be kept if no new image is uploaded"
            else:
                self.fields['image'].help_text = "Upload an image for this post (optional)"
        else:
            self.fields['image'].help_text = "Upload an image for this post (optional)"

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            self.save_m2m()
            
            # Handle tags
            tags_string = self.cleaned_data.get('tags', '')
            if tags_string:
                # Clear existing tags
                instance.tags.clear()
                # Add new tags
                tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
        
        return instance


class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User  
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a unique username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter a secure password'}),
            'confirm_password': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Both fields are required.")
        
        return cleaned_data
