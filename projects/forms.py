from django import forms

from constants import PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN
from mixins import GithubUrlMixin

from .models import Project


class ProjectForm(GithubUrlMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        labels = {
            "name": "Название",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
            "status": "Статус",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "status": forms.Select(
                choices=[(PROJECT_STATUS_OPEN, "Открыт"), (PROJECT_STATUS_CLOSED, "Закрыт")]
            ),
        }

