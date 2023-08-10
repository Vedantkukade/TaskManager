from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskModel(models.Model):
    name=models.CharField(max_length=100)
    detail=models.CharField(max_length=200)
    category=models.CharField(max_length=30)
    status=models.IntegerField()
    end_date=models.DateField()
    is_deleted=models.BooleanField(default=False)
    created_on=models.DateField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')