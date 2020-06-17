from datetime import timedelta
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F
from .models import *

# Create your views here.
@staff_member_required
def index(request):
    data = {
        "within_24_hours": len(Users.objects.filter(date__gt=datetime.now() - timedelta(days=1))),
        "within_past_week": len(Users.objects.filter(date__gt=datetime.now() - timedelta(days=7))),
        "within_past_month": len(Users.objects.filter(date__gt=datetime.now() - timedelta(days=30))),
        "total_users": len(Users.objects.all()),
        "active_users": len(Users.objects.filter(active=1)),
        "inactive_users": len(Users.objects.filter(active=0))
    }
    return render(request, "index.html", data)


@staff_member_required
def list_users(request):
    data = {
        "users": Users.objects.all()
    }
    data["users_length"] = len(data["users"])
    return render(request, "users.html", data)

@staff_member_required
def update_user_status(request, user_id):
    user = Users.objects.get(pk=user_id)
    user.active *= -1
    user.save()
    return redirect(list_users)

@staff_member_required
def delete_user(request, user_id):
    user = Users.objects.get(pk=user_id)
    user.delete()
    return redirect(list_users)
