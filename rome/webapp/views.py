from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Article, Author, Sponsor  # Supprimez 'Itineraire' de l'import

class HomeView(ListView):
    model = Article
    template_name = 'rome/home.html'
    context_object_name = 'articles'
    ordering = ['-date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        context['authors'] = Author.objects.all()
        context['itineraires'] = Article.objects.all()
        # Filter out articles with empty author IDs
        context['articles'] = Article.objects.exclude(author__id=None)
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'rome/article_detail_full.html'
    context_object_name = 'article'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'rome/author_detail.html'
    context_object_name = 'author'
    
class ItineraireDetailView(DetailView):
    model = Article
    template_name = 'rome/itineraire_detail_full.html'
    context_object_name ='itineraire'