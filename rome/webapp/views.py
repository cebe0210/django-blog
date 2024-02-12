from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Article, Author, Sponsor, Comment, Product, UserProfile
from .forms import CommentForm, CustomLoginForm, UserProfileForm
from django.http import JsonResponse
from django.contrib.auth import login
from django.db.models import Q
from functools import reduce  
from operator import or_
from unidecode import unidecode
import requests  
from rome.secret import OPENWEATHERMAP_API_KEY
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime

class HomeView(ListView):
    model = Article
    template_name = 'rome/home.html'
    context_object_name = 'articles'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        context['authors'] = Author.objects.all()
        context['contents'] = Article.objects.exclude(author__id=None)
        weather_data = self.get_weather_data()
        context.update(weather_data)
        context['itineraire_list'] = Article.objects.filter(category=Article.Category.Itineraire)
        return context

    def get_weather_data(self):
        lat = 41.5330
        lon = 12.3040
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_url = f"{base_url}?lat={lat}&lon={lon}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            weather_condition = data['weather'][0]['main']
            weather_description = data['weather'][0]['description']
            weather_icon_id = data['weather'][0]['id']
            icon_path = self.select_weather_icon(weather_icon_id)
            itineraire_list = Article.objects.filter(category=Article.Category.Itineraire)
            return {
                'temperature': temp,
                'weather_condition': weather_condition,
                'weather_description': weather_description,
                'weather_icon': icon_path,
                'weather_id': weather_icon_id,
                'itineraire_list': itineraire_list,
            }
        else:
            print("Erreur lors de la récupération des données météorologiques:", response.status_code, response.text)
            return {}

    def select_weather_icon(self, weather_icon_id):
    # Simplification pour le moment de la journée
        now = datetime.datetime.now()
        if 6 <= now.hour < 18:
            day_part = 'day'
        else:
            day_part = 'night'
        
        # Vérifier si l'ID météo nécessite une gestion jour/nuit
        if weather_icon_id in [800, 801, 802, 803, 804]:  # IDs où jour/nuit importe
            icon_filename = WEATHER_ICON_MAP.get(weather_icon_id, 'default.svg').replace('day', day_part)
        else:
            icon_filename = WEATHER_ICON_MAP.get(weather_icon_id, 'default.svg')
        
        return f'weather-icons/{icon_filename}'

WEATHER_ICON_MAP = {
    # Thunderstorm
    200: 'isolated-thunderstorms-day.svg',
    201: 'isolated-thunderstorms-day.svg',
    202: 'isolated-thunderstorms-day.svg',
    210: 'isolated-thunderstorms-day.svg',
    211: 'thunderstorms.svg',
    212: 'severe-thunderstorm.svg',
    221: 'scattered-thunderstorms.svg',
    230: 'isolated-thunderstorms-day.svg',
    231: 'isolated-thunderstorms-night.svg',
    232: 'severe-thunderstorm.svg',

    # Drizzle
    300: 'rainy-1.svg',
    301: 'rainy-2.svg',
    302: 'rainy-3.svg',

    # Rain
    500: 'rainy-1-day.svg',
    501: 'rainy-2-day.svg',
    502: 'rainy-3-day.svg',
    511: 'rain-and-sleet-mix.svg',
    520: 'rainy-1-night.svg',
    521: 'rainy-2-night.svg',
    522: 'rainy-3-night.svg',

    # Snow
    600: 'snowy-1-day.svg',
    601: 'snowy-2-day.svg',
    602: 'snowy-3-day.svg',
    611: 'snow-and-sleet-mix.svg',
    612: 'snow-and-sleet-mix.svg',
    615: 'rain-and-snow-mix.svg',
    616: 'rain-and-snow-mix.svg',
    620: 'snowy-1-night.svg',
    621: 'snowy-2-night.svg',
    622: 'snowy-3-night.svg',

    # Atmosphere
    701: 'fog-day.svg',
    711: 'haze.svg',
    721: 'haze-day.svg',
    731: 'dust.svg',
    741: 'fog.svg',
    751: 'dust.svg',
    761: 'dust.svg',
    762: 'dust.svg',
    771: 'wind.svg',
    781: 'tornado.svg',

    # Clear
    800: 'clear-day.svg', 

    # Clouds
    801: 'cloudy-1-day.svg',
    802: 'cloudy-2-day.svg',
    803: 'cloudy-3-day.svg',
    804: 'cloudy.svg',
}
def select_weather_icon(weather_icon_id, timestamp):
    """
    Sélectionne le nom de fichier de l'icône basé sur l'ID de condition météo.
    Utilise le timestamp pour déterminer si c'est le jour ou la nuit.
    """
    # Exemple simplifié, nécessite une logique pour gérer jour/nuit
    icon_filename = WEATHER_ICON_MAP.get(weather_icon_id, 'default.svg')
    return f'static/images/weather_icons/{icon_filename}'

def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.likes += 1
    article.save()
    return JsonResponse({'likes': article.likes})

class ArticleDetailView(DetailView):
    model = Article

    def get_template_names(self):
        category_templates = {
            Article.Category.Itineraire: 'rome/itineraire_detail_full.html',
            Article.Category.Histoire: 'rome/histoire_detail_full.html',
            Article.Category.Art: 'rome/art_detail_full.html',
            Article.Category.Cuisine: 'rome/cuisine_detail_full.html',
            Article.Category.Article: 'rome/article_detail_full.html',
        }
        category = self.object.category
        print(f"Category: {category}")  # Catégorie de l'article
        print(f"Template Name: {self.template_name}")  # Nom du modèle de vue
        return [category_templates.get(category, 'rome/article_detail_full.html')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajoutez ici d'autres données spécifiques à chaque catégorie si nécessaire
        article = context['article']
        context['comments'] = Comment.objects.filter(article=article)
        context['comment_form'] = CommentForm()
        return context


class ItineraireDetailView(DetailView):
    model = Article
    template_name = 'rome/itineraire_detail_full.html'  # Assurez-vous d'avoir ce template
    context_object_name = 'itineraire'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itineraire = context['itineraire']
        context['comments'] = Comment.objects.filter(article=itineraire)
        context['comment_form'] = CommentForm()
        return context
class ItineraireListView(ListView):
    template_name = 'rome/itineraire_list.html'
    context_object_name = 'itineraire'
    
    def get_queryset(self):
        return Article.objects.filter(category=Article.Category.Itineraire)

    
class HistoireDetailView(DetailView):
    model = Article
    template_name = 'rome/itineraire_list.html'
    context_object_name = 'histoire'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        histoire = context['histoire']
        context['comments'] = Comment.objects.filter(article=histoire)
        context['comment_form'] = CommentForm()
        return context
    
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'rome/author_detail.html'
    context_object_name = 'author'

class CommentView(DetailView):
    model = Comment
    template_name = 'rome/comment.html'
    context_object_name = 'comment'
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'rome/product_detail.html'
    context_object_name = 'product'

class ProductListView(ListView):
    model = Product
    template_name = 'rome/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter d'autres contexte si nécessaire
        return context
    
def login_View(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomLoginForm()

    context = {
        'form': form,
    }
    
    return render(request, 'rome/login.html', context)

# class Unaccent(Func):
#     function = 'UNACCENT'
def normalize_search_term(term):
    # Conversion en minuscules
    term = term.lower()
    # Suppression des accents
    term = unidecode(term)
    return term


def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        normalized_query = normalize_search_term(query)
        keywords = normalized_query.split()
        query_filters = Q()
        for keyword in keywords:
            query_filters |= Q(title__icontains=keyword) | Q(content__icontains=keyword)
        results = Article.objects.filter(query_filters)
    else:
        results = Article.objects.all()
    context = {'results': results, 'query': query}
    return render(request, 'rome/search_results.html', context)

def normalize_search_term(term):
    term = term.lower()
    term = unidecode(term)
    return term

@method_decorator(login_required, name='dispatch')
class editProfileView(View):
    template_name = 'rome/edit_profile.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)
        form = UserProfileForm(instance=profile)
        return render(request, self.template_name, {'form': form, 'userprofile': profile})

    def post(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'userprofile': profile})