from django.contrib import admin
from .models import Tag, Author, BlogPost

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_author', 'created_at', 'updated_at', 'get_tags')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_filter = ('created_at', 'updated_at', 'tags')
    filter_horizontal = ('tags',)  # Nice widget for many-to-many tags
    
    def get_tags(self, obj):
        """Display tags in list view"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'
    
    def get_author(self, obj):
        """Display full author name in list view"""
        return f"{obj.author.first_name} {obj.author.last_name}"
    get_author.short_description = 'Author'

admin.site.register(Tag, TagAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
