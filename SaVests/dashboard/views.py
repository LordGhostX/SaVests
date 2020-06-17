from datetime import timedelta
from datetime import datetime
import csv
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core.mail import send_mass_mail
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
        "inactive_users": len(Users.objects.filter(active=-1))
    }
    return render(request, "index.html", data)


@staff_member_required
def list_users(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    if name and email:
        user = Users(name=name, email=email)
        user.save()
        return redirect(list_users)
    data = {
        "users": Users.objects.order_by("-date")
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


@staff_member_required
def download_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user-data-{}.csv"'.format(int(datetime.now().timestamp()))

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Active', 'Date'])
    for i in Users.objects.all():
        active = "Active" if i.active ==  1 else "Inactive"
        writer.writerow([i.name, i.email, active, i.date])

    return response


@staff_member_required
def send_email(request):
    num_successful = -1
    if request.method == "POST":
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        sender = request.POST.get("sender")
        if subject and content:
            messages = []
            for i in Users.objects.all():
                messages.append((subject, content, sender, [i.email]))
            num_successful = send_mass_mail(tuple(messages), fail_silently=False)
    data = {
        "total_users": len(Users.objects.all()),
        "num_successful": num_successful
    }
    return render(request, "email.html", data)
