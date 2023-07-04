from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
from webapp.models import Article


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("-updated_at")
        context = {"articles": articles}
        return render(request, "index.html", context)


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        print(form)
        return render(request, "create_article.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            tags = form.cleaned_data.pop("tags")
            article = Article.objects.create(title=form.cleaned_data.get("title"),
                                             content=form.cleaned_data.get("content"),
                                             author=form.cleaned_data.get("author"),
                                             )
            article.tags.set(tags)
            return redirect("article_view", pk=article.pk)
        else:
            print(form.errors)
            return render(request, "create_article.html", {"form": form})


def article_update_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        form = ArticleForm(initial={
            "title": article.title,
            "author": article.author,
            "content": article.content,
            "tags": article.tags.all()
        })
        return render(request, "update_article.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            tags = form.cleaned_data.pop("tags")
            article.title = form.cleaned_data.get("title")
            article.content = form.cleaned_data.get("content")
            article.author = form.cleaned_data.get("author")
            article.save()
            article.tags.set(tags)
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


class ArticleDetailView(TemplateView):
    # template_name = "article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = get_object_or_404(Article, id=kwargs['pk'])
        return context

    def get_template_names(self):
        return "article.html"
