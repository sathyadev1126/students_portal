from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username