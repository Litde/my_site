from django.contrib import admin
from .models import Book, Author, Adress, Country
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'published_date', 'price', 'get_published_countries')
    search_fields = ('title', 'author__name')  # Updated to search author name properly
    list_filter = ('rating', 'published_date', 'published_countries')
    
    def get_published_countries(self, obj):
        """Display published countries in list view"""
        return ", ".join([country.name for country in obj.published_countries.all()])
    get_published_countries.short_description = 'Published Countries'

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'adress')
    search_fields = ('name',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'get_books_count')
    search_fields = ('name', 'code')
    
    def get_books_count(self, obj):
        """Display number of books published in this country"""
        return obj.books.count()
    get_books_count.short_description = 'Books Published'

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Adress)
admin.site.register(Country, CountryAdmin)
