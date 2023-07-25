from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from webapp.models import Status, Type, Issue, Project


class IssueTrackerForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["summary", "description", "status", "type"]
        widgets = {
            "content": widgets.Textarea(attrs={"cols": 30, "rows": 5}),
            "type": widgets.CheckboxSelectMultiple
        }

        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('summary') and cleaned_data.get('description') and \
                    cleaned_data['summary'] == cleaned_data['description']:
                raise ValidationError('Description of the issue should not duplicate the summary')
            return cleaned_data


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "start_date", "end_date"]
        widgets = {
            'start_date': widgets.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            }),
            'end_date': widgets.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('title') and cleaned_data.get('description') and \
                cleaned_data['title'] == cleaned_data['description']:
            raise ValidationError('Description of the issue should not duplicate the title')
        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Search")
