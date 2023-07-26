from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from webapp.forms import ProjectForm, UserForm
from webapp.models import Project


class UserManageView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Project
    success_url = reverse_lazy("webapp:project_detail")
    form_class = UserForm
    template_name = "users/user_add.html"

    def has_permission(self):
        return self.request.user.has_perm('auth.add_user')

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        user = form.save()
        user.project = project
        user.save()
        return redirect('webapp:project_detail', pk=project.pk)
