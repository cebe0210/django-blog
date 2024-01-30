from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')

class Author(models.Model):
    name = models.CharField(max_length=64)
    biography = models.TextField()
    picture = models.ImageField(upload_to='img/autor/')
    STATUS_CHOICES = [
        (True, 'Actif'),
        (False, 'Inactif'),
    ]
    active = models.BooleanField(choices=STATUS_CHOICES, default=True)

    def __str__(self):
        return self.name if self.name else "Auteur sans nom"
    
class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    class Category(models.TextChoices):
        Article = 'Article', 'Article'
        Histoire = 'Histoire', 'Histoire'
        Art = 'Art', 'Art'
        Cuisine = 'Cuisine', 'Cuisine'
        Itineraire = 'Itineraire', 'Itineraire'
    category = models.CharField(choices=Category.choices, max_length=16, default='ARTI')
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    use_external_image = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    image_description = models.TextField(blank=True, null=True)
    map_link = models.URLField(max_length=200, null=True, blank=True)
    carousel_images = models.ManyToManyField(CarouselImage, blank=True)
    STATUS_CHOICES = [
        (True, 'Actif'),
        (False, 'Inactif'),
    ]
    active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    likes = models.PositiveIntegerField(default=0)
    
    def get_absolute_url(self):
        category_views = {
            self.Category.Itineraire: 'itineraire_detail',
            self.Category.Histoire: 'histoire_detail',
            self.Category.Art: 'art_detail',
            self.Category.Cuisine: 'cuisine_detail',
            self.Category.Article: 'article_detail',
        }
        view_name = category_views.get(self.category, 'article_detail')
        return reverse(view_name, kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title
    
    # def is_itineraire(self):
    #     return self.itineraire

class Comment(models.Model):
    author = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=1024)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        (True, 'Actif'),
        (False, 'Inactif'),
    ]
    active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author} - {self.title}"
    
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='img/')
    STATUS_CHOICES = [
        (True, 'Actif'),
        (False, 'Inactif'),
    ]
    active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    page = models.URLField(max_length=100, blank=False)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='img/eshop/')
    stock = models.IntegerField( )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    STATUS_CHOICES = [
        (True, 'Actif'),
        (False, 'Inactif'),
    ]
    active = models.BooleanField(choices=STATUS_CHOICES, default=True)
    
    def get_absolute_url(self):
        return reverse("product_list", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title    
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    # Ajoutez d'autres champs selon vos besoins
    eshop_points = models.IntegerField(default=0)
    blog_comments_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
