from django.urls import path
from django.views.generic import RedirectView

from webapp.views.articles_view import \
    article_update_view, article_delete_view, ArticleListView, ArticleCreateView, ArticleDetailView, \
    articles_delete_view

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="index")),
    path('articles/', ArticleListView.as_view(), name="index"),
    path('articles/add/', ArticleCreateView.as_view(), name="article_add"),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name="article_view"),
    path('article/<int:pk>/update/', article_update_view, name="article_update_view"),
    path('article/<int:pk>/delete/', article_delete_view, name="article_delete_view"),
    path('articles/delete/', articles_delete_view, name="articles_delete_view")
]
