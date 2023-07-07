from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from webapp.forms import ArticleForm
from webapp.models import Article


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by("-updated_at")
        context = {"articles": articles}
        return render(request, "index.html", context)


class ArticleCreateView(FormView):
    # success_url = reverse_lazy("index")
    form_class = ArticleForm
    template_name = "create_article.html"

    # def get_success_url(self):
    #     return reverse("article_view", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # tags = form.cleaned_data.pop("tags")
        # article = Article.objects.create(title=form.cleaned_data.get("title"),
        #                                  content=form.cleaned_data.get("content"),
        #                                  author=form.cleaned_data.get("author"),
        #                                  )
        # article.tags.set(tags)
        # self.object = article
        # return super().form_valid(form)
        article = form.save()
        return redirect("article_view", pk=article.pk)


class ArticleUpdateView(FormView):
    form_class = ArticleForm
    template_name = "update_article.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object(kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, pk):
        return get_object_or_404(Article, id=pk)

    # def get_initial(self):
    #     initial = {}
    #     for key in 'title', 'content', 'author':
    #         initial[key] = getattr(self.article, key)
    #     # initial["title"] = self.article.title
    #     initial['tags'] = self.article.tags.all()
    #     return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        form.save()
        # tags = form.cleaned_data.pop('tags')
        # self.article.title = form.cleaned_data.get("title")
        # self.article.content = form.cleaned_data.get("content")
        # self.article.author = form.cleaned_data.get("author")
        # self.article.save()
        # self.article.tags.set(tags)
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         setattr(self.article, key, value)
        # self.article.save()
        # self.article.tags.set(tags)
        return redirect("article_view", pk=self.article.pk)


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
