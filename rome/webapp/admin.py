from django.contrib import admin
from .models import Author, Article, Sponsor, Comment

@admin.register(Author)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'author', 'active')
    list_filter = ('category', 'date', 'author', 'active')
    search_fields = ('title', 'content', 'author__name')
    
@admin.register(Sponsor)
class SposorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'article', 'parent_comment')