# Generated by Django 4.1.7 on 2023-06-24 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0025_alter_teachinglogbook_subtopic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachinglogbook',
            old_name='Workload',
            new_name='workload',
        ),
    ]