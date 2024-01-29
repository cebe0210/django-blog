from django.db import models
from django.urls import reverse
from django.utils import timezone

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
        Architecture = 'ARC', 'Architecture'
        Histoire = 'HIST', 'Histoire'
        Art = 'ART', 'Art'
        Cuisine = 'CUIS', 'Cuisine'
        Itineraire = 'ITIN', 'Itineraire'
    category = models.CharField(choices=Category.choices, max_length=5, default='HIST')
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
    itineraire = models.BooleanField(choices=STATUS_CHOICES, default=False)
    
    def get_absolute_url(self):
        if self.is_itineraire():
            return reverse('itineraire_detail', args=[str(self.id)])
        else:
            return reverse('article_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title
    
    def is_itineraire(self):
        return self.itineraire

    
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


    
