from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
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
                choices=[("open", "Открыт"), ("closed", "Закрыт")]
            ),
        }

    def clean_github_url(self):
        url = (self.cleaned_data.get("github_url") or "").strip()
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на github.com.")
        return url or ""
