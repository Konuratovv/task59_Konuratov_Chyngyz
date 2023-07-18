from django.urls import path

from webapp.views.issues_views import IssueListView, IssueCreateView, IssueDetailedView, delete_issue, IssueUpdateView

urlpatterns = [
    path('', IssueListView.as_view(), name='issues'),
    path('create/', IssueCreateView.as_view(), name='create'),
    path('detail/<int:pk>', IssueDetailedView.as_view(), name='detail'),
    path('delete/<int:pk>', delete_issue, name='delete'),
    path('update/<int:pk>', IssueUpdateView.as_view(), name="update")
]
