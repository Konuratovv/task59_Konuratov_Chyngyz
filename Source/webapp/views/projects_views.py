from audioop import reverse
from msilib.schema import ListView

from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from webapp.forms import IssueTrackerForm, SearchForm, ProjectForm
from webapp.models import Issue, Project
from django.db.models import Q


class ProjectListView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['search_form'] = SearchForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) |
                                       Q(description__icontains=self.search_value))
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "projects/create.html"
    model = Project
    form_class = ProjectForm

    def has_permission(self):
        return self.request.user.has_perm('webapp.add_project')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(self, request, *args, **kwargs)
    #     return redirect("accaunts:login")

    def get_success_url(self):
        return reverse('webapp:projects')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_valid(self, form):
        form.save()
        return redirect('webapp:projects')


class ProjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = "projects/update.html"
    model = Project

    def get_success_url(self):
        return reverse('webapp:projects')

    def has_permission(self):
        return self.request.user.has_perm('webapp.change_project')

    # def dispatch(self, request, *args, **kwargs):
    #     self.project = self.get_object(kwargs.get('pk'))
    #     return super().dispatch(request, *args, **kwargs)
    #
    # def get_object(self, pk):
    #     return get_object_or_404(Issue, id=pk)
    #
    # def get_initial(self):
    #     initial = {}
    #     for key in 'summary', 'description', 'status':
    #         initial[key] = getattr(self.project, key)
    #     initial['type'] = self.project.type.all()
    #     return initial
    #
    # def form_valid(self, form):
    #     self.project.save()
    #     return redirect('webapp:projects')


class ProjectDetailedView(PermissionRequiredMixin, DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        issues = project.issues.all()
        users = project.user.all()
        context['users'] = users
        context['issues'] = issues
        return context

    def has_permission(self):
        return self.request.user.has_perm(
            'webapp.view_project') or self.get_object().author == self.request.user or self.request.user in self.get_object().user.all()


class ProjectDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/delete.html"
    reverse_lazy('webapp:projects')

    def get_success_url(self):
        return reverse('webapp:projects')

    def has_permission(self):
        return self.request.user.has_perm('webapp.delete_project')
