from django.db import models


class ProjectQuerySet(models.QuerySet):
    def with_relations(self):
        return self.select_related("owner").prefetch_related("participants")
