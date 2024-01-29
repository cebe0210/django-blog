from django.urls import path
from .views import HomeView, ArticleDetailView, AuthorDetailView, like_article, CommentView, ItineraireDetailView, HistoireDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('like_article/<int:pk>/', like_article, name='like_article'),
    path('article/<int:pk>/comments/', CommentView.as_view(), name='article_comments'),
    # Ajoutez les patterns pour les autres catégories ici
    path('itineraire/<int:pk>/', ItineraireDetailView.as_view(), name='itineraire_detail'),
    path('histoire/<int:pk>/', HistoireDetailView.as_view(), name='histoire_detail'),
    # path('art/<int:pk>/', ArtDetailView.as_view(), name='art_detail'),
    # path('cuisine/<int:pk>/', CuisineDetailView.as_view(), name='cuisine_detail'),
    # ... Ajoutez les autres catégories selon votre modèle
]
