from django import forms

from constants import GITHUB_DOMAIN


class GithubUrlMixin:
    def clean_github_url(self):
        url = (self.cleaned_data.get("github_url") or "").strip()
        if url and GITHUB_DOMAIN not in url:
            raise forms.ValidationError(f"Ссылка должна вести на {GITHUB_DOMAIN}.")
        return url or ""
