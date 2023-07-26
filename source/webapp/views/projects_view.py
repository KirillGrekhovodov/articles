from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.html import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, SearchForm, ProjectForm, ProjectUsersForm
from webapp.models import Article, Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = ("-updated_at",)
    paginate_by = 3

    # paginate_orphans = 1


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create_project.html"
    permission_required = "webapp.add_project"

    def get_success_url(self):
        return reverse("webapp:index_project")

    # def dispatch(self, request, *args, **kwargs):
    #     result = super().dispatch(request, *args, **kwargs)
    #     if request.user.has_perm("webapp.add_article"):
    #         return result
    #     raise PermissionDenied()

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect("accounts:login")

    # def get_success_url(self):
    #     return reverse("webapp:article_view", kwargs={"pk": self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/update_project.html"
    permission_required = "webapp.change_project"

    def has_permission(self):
        # return self.request.user.groups.filter(name="moderators")
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:index_project")

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial["title"] = "hardcore_title"
    #     return initial


class ChangeUsersInProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUsersForm
    template_name = "projects/change_users_in_project.html"
    permission_required = "webapp.add_users_in_project"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:index_project")
