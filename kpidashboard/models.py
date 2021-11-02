from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    # Integer value represents time in seconds
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    totalTalkTime = models.IntegerField(default=0)
    averageTalkTime = models.IntegerField(default=0)
    totalHoldTime = models.IntegerField(default=0)
    averageTalkTime = models.IntegerField(default=0)
    totalAfterCallWorkTime = models.IntegerField(default=0)
    averageAfterCallWorkTime = models.IntegerField(default=0)
    totalTalkTime = models.IntegerField(default=0)
    lastCallAnswerSpeed = models.IntegerField(default=0)
    averageAllCallAnswerSpeed = models.IntegerField(default=0)
    date = models.DateField()


class WorkgroupData(models.Model):
    # Integer value represents time in seconds
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    totalTalkTime = models.IntegerField(default=0)
    averageTalkTime = models.IntegerField(default=0)
    totalHoldTime = models.IntegerField(default=0)
    averageTalkTime = models.IntegerField(default=0)
    totalAfterCallWorkTime = models.IntegerField(default=0)
    averageAfterCallWorkTime = models.IntegerField(default=0)
    totalTalkTime = models.IntegerField(default=0)
    lastCallAnswerSpeed = models.IntegerField(default=0)
    averageAllCallAnswerSpeed = models.IntegerField(default=0)
    date = models.DateField()