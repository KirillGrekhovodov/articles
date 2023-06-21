from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound

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

        # url = reverse("article_view", kwargs={"pk": article.pk})
        # return HttpResponseRedirect(url)


def article_view(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, id=pk)
    # try:
    #     article = Article.objects.get(id=pk)
    # except Article.DoesNotExist:
    #     return HttpResponseNotFound()
    #     raise Http404()
    return render(request, "article.html", {"article": article})
