from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_only_big_chars

# Create your models here.

class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True, validators=[validate_only_big_chars])

    def __str__(self):
        return self.name
    
    

class Adress(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['city', 'street']
        
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}"
    
    

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    adress = models.OneToOneField(Adress, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[
        MinValueValidator(0.0), 
        MaxValueValidator(5.0)
    ])
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_countries = models.ManyToManyField(Country, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author} ({self.rating})"
    
    


    