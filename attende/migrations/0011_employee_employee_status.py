# Generated by Django 3.1.3 on 2020-11-09 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attende', '0010_auto_20201108_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_status',
            field=models.IntegerField(default=0),
        ),
    ]