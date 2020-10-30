# Generated by Django 3.0 on 2020-10-27 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attende', '0002_employee_employee_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_date', models.DateField()),
                ('emp_work_status', models.CharField(blank=True, default='', max_length=50)),
                ('emp_latitude', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('emp_longitude', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('emp_work_modelNumber', models.IntegerField(blank=True, null=True)),
                ('emp_totalProdution', models.IntegerField(blank=True, null=True)),
                ('emp_running', models.IntegerField(blank=True, null=True)),
                ('emp_maintainParts', models.CharField(blank=True, default='', max_length=500)),
                ('emp_partsReason', models.CharField(blank=True, default='', max_length=500)),
                ('maintain_partsImg', models.ImageField(blank=True, default='', upload_to='attende/aadhar')),
                ('travel_from', models.CharField(blank=True, default='', max_length=100)),
                ('travel_to', models.CharField(blank=True, default='', max_length=100)),
                ('travel_by', models.CharField(blank=True, default='', max_length=100)),
                ('travel_duration', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('travel_purpose', models.CharField(blank=True, default='', max_length=100)),
                ('travel_force', models.IntegerField(blank=True, null=True)),
                ('accompanied_emp2', models.IntegerField(blank=True, null=True)),
                ('accompanied_emp3', models.IntegerField(blank=True, null=True)),
                ('accompanied_emp4', models.IntegerField(blank=True, null=True)),
                ('accompanied_emp5', models.IntegerField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='attende.Employee')),
            ],
        ),
    ]