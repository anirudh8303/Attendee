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

class WorkDates(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    emp_date = models.DateField()
    emp_work_status = models.CharField(max_length=50, default="", blank=True)
    emp_latitude = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    emp_longitude = models.DecimalField(max_digits=10, decimal_places=5, default=0)
    emp_work_modelNumber  = models.IntegerField(blank=True, null=True)
    emp_totalProdution  = models.IntegerField(blank=True, null=True)
    emp_running = models.IntegerField(blank=True, null=True)
    emp_maintainParts = models.CharField(max_length=500, default="", blank=True)
    emp_partsReason = models.CharField(max_length=500, default="", blank=True)
    maintain_partsImg = models.ImageField(upload_to="attende/aadhar", default="", blank=True)
    travel_from = models.CharField(max_length=100, default="", blank=True)
    travel_to = models.CharField(max_length=100, default="", blank=True)
    travel_by = models.CharField(max_length=100, default="", blank=True)
    travel_duration = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    travel_purpose = models.CharField(max_length=100, default="", blank=True)
    travel_force =  models.IntegerField(blank=True, null=True)
    accompanied_emp2 = models.IntegerField(blank=True, null=True)
    accompanied_emp3 =  models.IntegerField(blank=True, null=True)
    accompanied_emp4 =  models.IntegerField(blank=True, null=True)
    accompanied_emp5 =  models.IntegerField(blank=True, null=True)