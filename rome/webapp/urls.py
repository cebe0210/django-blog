from django.urls import path
from .views import HomeView, ArticleDetailView, AuthorDetailView, like_article, CommentView, ItineraireDetailView, HistoireDetailView, ProductListView, ProductDetailView, login_View

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
    # path('eshop/<int:pk>/', EshopView.as_view(), name='eshop_detail'),
    
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('login/', login_View, name='login'),
]
