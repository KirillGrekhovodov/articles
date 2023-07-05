from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from webapp.forms import ArticleForm
from webapp.models import Article, Category


def articles_list_view(request):
    articles = Article.objects.order_by("-updated_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def article_create_view(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, "create_article.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(
            #     title=form.cleaned_data.get("title"),
            #     author=form.cleaned_data.get("author"),
            #     content=form.cleaned_data.get("content"),
            #     status=form.cleaned_data.get("status"),
            #     publish_date=form.cleaned_data.get("publish_date"),
            #     category=form.cleaned_data.get("category"),
            # )
            article = form.save()
            return redirect("article_view", pk=article.pk)
        else:
            return render(request, "create_article.html", {"form": form})


def article_update_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        form = ArticleForm(instance=article)
        return render(request, "update_article.html", {"form": form})
    else:
        form = ArticleForm(instance=article, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("article_view", pk=article.pk)
        else:
            return render(request, "update_article.html", {"form": form})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        return render(request, "delete_article.html", {"article": article})
    else:
        article.delete()
        return redirect("index")


def article_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, id=pk)
    return render(request, "article.html", {"article": article})


class CategoryArticlesView(View):
    def get(self, request, *args, title_slug, **kwargs):
        category = get_object_or_404(Category, title_slug=title_slug)
        context = {"articles": category.articles.all().order_by("-updated_at"), "category_title": category.title}
        return render(request, "category_articles.html", context)
