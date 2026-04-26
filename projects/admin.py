from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "participant_count", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "owner__email")
    filter_horizontal = ("participants",)

    @admin.display(description="Участники")
    def participant_count(self, obj):
        return obj.participants.count()
