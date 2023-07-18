from django.urls import path

from webapp.views.issues_views import IssueListView, IssueCreateView, IssueDetailedView, delete_issue, IssueUpdateView
from webapp.views.projects_views import ProjectListView, ProjectCreateView, ProjectDetailedView, ProjectUpdateView, \
    delete_project

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('issues/', IssueListView.as_view(), name="issues"),
    path('issue/create/', IssueCreateView.as_view(), name='create'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/detail/<int:pk>', ProjectDetailedView.as_view(), name='project_detail'),
    path('issue/detail/<int:pk>', IssueDetailedView.as_view(), name='detail'),
    path('issue/delete/<int:pk>', delete_issue, name='delete'),
    path('project/delete/<int:pk>', delete_project, name='project_delete'),
    path('issue/update/<int:pk>', IssueUpdateView.as_view(), name="update"),
    path('project/update/<int:pk>', ProjectUpdateView.as_view(), name="project_update")
]
