from msilib.schema import ListView

from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView

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


class ProjectCreateView(FormView):
    success_url = reverse_lazy("projects")
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        form.save()
        return redirect('projects')


class ProjectUpdateView(FormView):
    form_class = IssueTrackerForm
    template_name = "issues/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object(kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, pk):
        return get_object_or_404(Issue, id=pk)

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'status':
            initial[key] = getattr(self.issue, key)
        initial['type'] = self.issue.type.all()
        return initial

    def form_valid(self, form):
        self.issue.save()
        return redirect('issues')


class ProjectDetailedView(DetailView):
    model = Project
    template_name = "projects/detail.html"


def delete_project(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    if request.method == "GET":
        return render(request, "issues/delete_product.html", {'issue': issue})
    else:
        issue.delete()
        return redirect('issues')
