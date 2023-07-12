from django.db.models import Q
from django.utils.html import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article


class ArticleListView(ListView):
    queryset = Article.objects.all().prefetch_related("tags")
    template_name = "articles/index.html"
    context_object_name = "articles"
    ordering = ("-updated_at",)
    paginate_by = 10

    # paginate_orphans = 1

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["form"] = self.form
        if self.search_value:
            context["query"] = urlencode({'search': self.search_value})
            context["search_value"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.search_value)
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(author__icontains=self.search_value))
        return queryset


class ArticleCreateView(FormView):
    # success_url = reverse_lazy("index")
    form_class = ArticleForm
    template_name = "articles/create_article.html"

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
    template_name = "articles/update_article.html"

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
        return render(request, "articles/update_article.html", {"form": form})
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
            return render(request, "articles/update_article.html", {"form": form})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.method == "GET":
        return render(request, "articles/delete_article.html", {"article": article})
    else:
        article.delete()
        return redirect("index")


def articles_delete_view(request):
    articles_ids = request.POST.getlist("articles")
    if articles_ids:
        articles = Article.objects.filter(id__in=articles_ids)
        articles.delete()
    return redirect("index")


class ArticleDetailView(DetailView):
    queryset = Article.objects.all().prefetch_related("tags")
    template_name = "articles/article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by("-updated_at")
        return context
