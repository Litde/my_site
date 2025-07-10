from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.full_name()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=500, blank=True, null=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Blog Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Store hashed passwords
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)

#     def __str__(self):
#         return self.username
    

