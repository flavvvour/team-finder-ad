from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from service import paginate

from .constants import USERS_PER_PAGE
from .forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:login")
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("projects:list")
    form = LoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect("projects:list")
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("projects:list")


def user_list(request):
    qs = User.objects.filter(is_active=True).order_by("-id")

    active_filter = request.GET.get("filter", "")
    if active_filter and request.user.is_authenticated:
        u = request.user
        if active_filter == "owners-of-favorite-projects":
            qs = qs.filter(owned_projects__in=u.favorites.all()).distinct()
        elif active_filter == "owners-of-participating-projects":
            qs = qs.filter(owned_projects__in=u.participated_projects.all()).distinct()
        elif active_filter == "interested-in-my-projects":
            qs = qs.filter(favorites__in=u.owned_projects.all()).distinct()
        elif active_filter == "participants-of-my-projects":
            qs = qs.filter(participated_projects__in=u.owned_projects.all()).distinct()
        else:
            active_filter = ""

    page = paginate(qs, request.GET.get("page"), USERS_PER_PAGE)
    return render(request, "users/participants.html", {
        "participants": page,
        "page_obj": page,
        "active_filter": active_filter,
    })


def user_detail(request, user_id):
    profile = get_object_or_404(
        User.objects.prefetch_related("owned_projects__participants"),
        pk=user_id,
        is_active=True,
    )
    return render(request, "users/user-details.html", {"user": profile})


@login_required
def edit_profile(request):
    form = EditProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        return redirect("users:detail", user_id=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})
