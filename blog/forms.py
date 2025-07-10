from django import forms
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
        
        # Populate author choices
        self.fields['author'].queryset = Author.objects.all()
        
        # If editing an existing post, populate tags field
        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['tags'].initial = ', '.join([tag.name for tag in tags])

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
