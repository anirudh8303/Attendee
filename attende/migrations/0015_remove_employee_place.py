# Generated by Django 3.1.3 on 2020-11-11 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attende', '0014_auto_20201111_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='place',
        ),
    ]