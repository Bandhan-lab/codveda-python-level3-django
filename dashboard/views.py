from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    user = request.user
    groups = list(user.groups.values_list("name", flat=True))
    role = "Administrator" if user.is_superuser else "Staff" if user.is_staff else groups[0] if groups else "Member"
    return render(request, "dashboard/home.html", {
        "role": role,
        "groups": groups,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    })
