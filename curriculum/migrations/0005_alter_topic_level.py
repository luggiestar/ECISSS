# Generated by Django 4.1.7 on 2023-04-10 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0004_academicyear_level_subject_teachingcalendar_topic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_level', to='curriculum.level'),
        ),
    ]