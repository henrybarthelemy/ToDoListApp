from .models import Task
from django import forms


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "finished"
        ]
