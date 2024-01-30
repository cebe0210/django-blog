from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Article, Author, Sponsor, Comment, Product
from .forms import CommentForm, CustomLoginForm
from django.http import JsonResponse
from django.contrib.auth import login
from django.db.models import Q
from functools import reduce  # Importez reduce
from operator import or_

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

def search_view(request):
    query = request.GET.get('q')
    if query:
        # Splittez les mots-clés
        keywords = query.split()

        # Recherchez d'abord les articles contenant tous les mots-clés
        results = Article.objects.filter(
            reduce(or_, [Q(title__icontains=keyword) | Q(content__icontains=keyword) for keyword in keywords])
        )

        # Si aucun résultat n'est trouvé, recherchez les articles contenant au moins un mot-clé
        if not results:
            results = Article.objects.filter(
                reduce(or_, [Q(title__icontains=keyword) | Q(content__icontains=keyword) for keyword in keywords])
            )

    else:
        results = Article.objects.all()

    context = {'results': results, 'query': query}
    return render(request, 'rome/search_results.html', context)