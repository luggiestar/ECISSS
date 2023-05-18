# Generated by Django 4.1.7 on 2023-04-17 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0010_academicyear_name_alter_academicterm_total_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='name',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
