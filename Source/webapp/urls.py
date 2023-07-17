from django.contrib import admin
from django.urls import path

from webapp.views import IssueListView, IssueCreateView

urlpatterns = [
    path('', IssueListView.as_view(), name='issues'),
    path('/create', IssueCreateView.as_view(), name='create')
]