# Generated by Django 4.1.7 on 2023-06-23 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0019_teachingreport_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachingreport',
            name='comment',
        ),
    ]
