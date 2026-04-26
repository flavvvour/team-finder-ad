from django.conf import settings
from django.db import models
from django.urls import reverse

from constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
)


class ProjectQuerySet(models.QuerySet):
    def with_relations(self):
        return self.select_related("owner").prefetch_related("participants")


class Project(models.Model):
    objects = ProjectQuerySet.as_manager()
    STATUS_CHOICES = [(PROJECT_STATUS_OPEN, "Open"), (PROJECT_STATUS_CLOSED, "Closed")]

    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=max(len(value) for value, _ in STATUS_CHOICES),
        choices=STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participated_projects",
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"project_id": self.pk})

    def __str__(self):
        return self.name
