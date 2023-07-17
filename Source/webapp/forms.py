from django import forms
from django.forms import widgets

from webapp.models import Status, Type


class IssueTrackerForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label="Краткое описание")
    description = forms.CharField(max_length=2000, required=True, label="Описание", widget=widgets.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label="Статус")
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label="Типы")
