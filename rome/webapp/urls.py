from django.urls import path
from .views import HomeView, ArticleDetailView, AuthorDetailView, ItineraireDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('itineraire/<int:pk>/', ItineraireDetailView.as_view(), name='itineraire_detail'),
]
