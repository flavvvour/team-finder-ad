from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from service import paginate

from constants import PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN

from .constants import PROJECTS_PER_PAGE
from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects_qs = Project.objects.with_relations()
    page = paginate(projects_qs, request.GET.get("page"), PROJECTS_PER_PAGE)
    return render(request, "projects/project_list.html", {
        "projects": page,
        "page_obj": page,
    })


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.with_relations(),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", project_id=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:detail", project_id=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if favorited := user.favorites.filter(pk=project.pk).exists():
        user.favorites.remove(project)
    else:
        user.favorites.add(project)
    return JsonResponse({"status": "ok", "favorited": not favorited})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if user == project.owner:
        return JsonResponse(
            {"status": "error", "message": "Owner cannot leave own project."}, status=HTTPStatus.BAD_REQUEST
        )
    if participating := project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({"status": "ok", "participant": not participating})


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if project.status != PROJECT_STATUS_OPEN:
        return JsonResponse(
            {"status": "error", "message": "Project is already closed."}, status=HTTPStatus.BAD_REQUEST
        )
    project.status = PROJECT_STATUS_CLOSED
    project.save()
    return JsonResponse({"status": "ok", "project_status": PROJECT_STATUS_CLOSED})


@login_required
def favorites(request):
    projects = request.user.favorites.with_relations()
    return render(request, "projects/favorite_projects.html", {"projects": projects})
