from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    employee_phone = models.IntegerField()
    designation = models.CharField(max_length=20)
    place = models.CharField(max_length=30)
    employee_username = models.CharField(max_length=25)
    employee_aadhar = models.ImageField(upload_to ="attende/aadhar", default="")
    employee_email = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.employee_name
