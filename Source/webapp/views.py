from django.views import View

from django.shortcuts import render, redirect

from webapp.forms import IssueTrackerForm
from webapp.models import Issue


class IssueListView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.order_by("-updated_at")
        context = {'issues': issues}
        return render(request, 'index.html', context)


class IssueCreateView(View):
    def get(self, request, *args, **kwargs):
        form = IssueTrackerForm()
        return render(request, "create.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueTrackerForm(data=request.POST)
        if form.is_valid():
            note = Issue(summary=form.cleaned_data.get('summary'),
                         description=form.cleaned_data.get('description'),
                         status=form.cleaned_data.get('status'),
                         types=form.cleaned_data.get('types'))
            note.save()
            return redirect('issues')
        else:
            return render(request, "create.html", {'form': form})
