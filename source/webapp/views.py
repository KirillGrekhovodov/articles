from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Article


def articles_list_view(request):
    articles = Article.objects.order_by("-updated_at")
    context = {"articles": articles}
    return render(request, "index.html", context)


def article_create_view(request):
    if request.method == "GET":
        return render(request, "create_article.html")
    else:
        article = Article.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            author=request.POST.get("author")
        )
        return redirect("article_view", pk=article.pk)


def article_update_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        return render(request, "update_article.html", {"article": article})
    else:
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.author = request.POST.get("author")
        article.save()
        return redirect("article_view", pk=article.pk)


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
