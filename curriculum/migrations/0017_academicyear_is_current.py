# Generated by Django 4.1.7 on 2023-06-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0016_alter_teachingcalendar_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicyear',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]
