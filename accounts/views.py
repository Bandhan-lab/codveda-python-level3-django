from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def _member_group():
    group, _ = Group.objects.get_or_create(name="Member")
    permission = Permission.objects.get(
        content_type__app_label="dashboard",
        codename="access_member_dashboard",
    )
    group.permissions.add(permission)
    return group


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.groups.add(_member_group())
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("dashboard")

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
