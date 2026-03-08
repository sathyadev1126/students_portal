from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import StudentProfile

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        roll = request.POST['roll']
        branch = request.POST['branch']
        year = request.POST['year']
        section = request.POST['section']

        user = User.objects.create_user(username=username, password=password)

        StudentProfile.objects.create(
            user=user,
            roll_number=roll,
            branch=branch,
            year=year,
            section=section,
            approved=False
        )

        return render(request, "registration_success.html")

    return render(request, "register.html")