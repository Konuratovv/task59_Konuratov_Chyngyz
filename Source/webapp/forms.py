from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from webapp.models import Status, Type, Issue


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


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Search")
