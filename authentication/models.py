from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    userId = models.OneToOneField(to=User, on_delete=models.CASCADE)
    agent = models.BooleanField(default='False')
    supervisor = models.BooleanField(default='False')