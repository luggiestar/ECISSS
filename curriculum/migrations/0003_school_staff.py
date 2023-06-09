# Generated by Django 4.1.7 on 2023-04-10 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_alter_user_options_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_district', to='curriculum.district')),
            ],
            options={
                'verbose_name': 'School',
                'verbose_name_plural': 'School',
                'db_table': 'school',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_staff', to='curriculum.school')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
                'db_table': 'staff',
            },
        ),
    ]
