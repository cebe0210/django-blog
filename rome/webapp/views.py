from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Author, Sponsor, Comment
from .forms import CommentForm
from django.http import JsonResponse

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
        return context

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

class HistoireDetailView(DetailView):
    model = Article
    template_name = 'rome/histoire_detail_full.html'
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
