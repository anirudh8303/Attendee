# Generated by Django 3.1.3 on 2020-11-10 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attende', '0012_employee_employee_workingdates'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='travel_Image',
            field=models.ImageField(blank=True, default='', upload_to='attende/travel'),
        ),
    ]