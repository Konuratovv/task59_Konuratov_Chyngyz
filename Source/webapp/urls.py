from django.urls import path

from webapp.views.issues_views import IssueListView, IssueCreateView, IssueDetailedView, IssueUpdateView, \
    IssueDeleteView
from webapp.views.projects_views import ProjectListView, ProjectCreateView, ProjectDetailedView, ProjectUpdateView, \
     ProjectDeleteView
from webapp.views.user_views import UserManageView

app_name = "webapp"

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/issue/create/', IssueCreateView.as_view(), name='create'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/detail/<int:pk>', ProjectDetailedView.as_view(), name='project_detail'),
    path('issue/detail/<int:pk>', IssueDetailedView.as_view(), name='detail'),
    path('issue/delete/<int:pk>', IssueDeleteView.as_view(), name='delete'),
    path('project/delete/<int:pk>', ProjectDeleteView.as_view(), name='project_delete'),
    path('issue/update/<int:pk>', IssueUpdateView.as_view(), name="update"),
    path('project/update/<int:pk>', ProjectUpdateView.as_view(), name="project_update"),
    path('project/<int:pk>/user/manage', UserManageView.as_view(), name="add_user")
]
