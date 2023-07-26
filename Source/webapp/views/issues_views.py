from msilib.schema import ListView

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from webapp.forms import IssueTrackerForm, SearchForm
from webapp.models import Issue, Project
from django.db.models import Q


class IssueListView(ListView):
    model = Issue
    template_name = "issues/index.html"
    context_object_name = "issues"
    ordering = "-updated_at"
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
            queryset = queryset.filter(Q(summary__icontains=self.search_value) |
                                       Q(description__icontains=self.search_value))
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class IssueCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # success_url = reverse_lazy("webapp:project_detail")
    form_class = IssueTrackerForm
    template_name = "issues/create.html"

    def has_permission(self):
        return self.request.user.has_perm('webapp.add_issue')

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save()
        issue.project = project
        issue.save()
        return redirect('webapp:project_detail', pk=project.pk)


class IssueUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = IssueTrackerForm
    template_name = "issues/update.html"
    model = Issue

    def form_valid(self, form):
        self.issue.save()
        return redirect('projects')

    def has_permission(self):
        return self.request.user.has_perm('webapp.change_issue')


class IssueDetailedView(PermissionRequiredMixin, DetailView):
    model = Issue
    template_name = "issues/detail.html"

    def has_permission(self):
        return self.request.user.has_perm('webapp.view_issue')


class IssueDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = "issues/delete.html"
    reverse_lazy('webapp:project_detail')

    def has_permission(self):
        return self.request.user.has_perm('webapp.delete_issue')
