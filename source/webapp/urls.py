from django.urls import path

from webapp.views import articles_list_view, \
    article_create_view, article_view, article_update_view, article_delete_view, CategoryArticlesView

urlpatterns = [
    path('', articles_list_view, name="index"),
    path('articles/add/', article_create_view, name="article_add"),
    path('article/<int:pk>/', article_view, name="article_view"),
    path('article/<int:pk>/update/', article_update_view, name="article_update_view"),
    path('article/<int:pk>/delete/', article_delete_view, name="article_delete_view"),
    path('category/<slug:title_slug>/', CategoryArticlesView.as_view(), name="category_articles_view"),
]
