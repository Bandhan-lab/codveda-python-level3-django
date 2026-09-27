from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    user = request.user
    has_dashboard_access = (
        user.is_superuser
        or user.is_staff
        or user.has_perm("dashboard.access_member_dashboard")
    )

    if not has_dashboard_access:
        return render(request, "dashboard/forbidden.html", status=403)

    groups = list(user.groups.values_list("name", flat=True))
    role = (
        "Administrator"
        if user.is_superuser
        else "Staff"
        if user.is_staff
        else groups[0]
        if groups
        else "Member"
    )
    return render(
        request,
        "dashboard/home.html",
        {
            "role": role,
            "groups": groups,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "has_dashboard_access": has_dashboard_access,
        },
    )
