# Generated by Django 4.1.7 on 2023-04-11 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0006_role_alter_region_options_staff_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6)),
            ],
            options={
                'verbose_name': 'Term',
                'verbose_name_plural': 'Term',
                'db_table': 'term',
            },
        ),
        migrations.RemoveField(
            model_name='academicyear',
            name='name',
        ),
        migrations.RemoveField(
            model_name='teachingcalendar',
            name='academic_year',
        ),
        migrations.RemoveField(
            model_name='teachingreport',
            name='teacher',
        ),
        migrations.CreateModel(
            name='Workload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workload_acy', to='curriculum.academicyear')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workload_level', to='curriculum.level')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workload_subject', to='curriculum.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workload_teacher', to='curriculum.staff')),
            ],
            options={
                'verbose_name': 'Workload',
                'verbose_name_plural': 'Workload',
                'db_table': 'workload',
            },
        ),
        migrations.CreateModel(
            name='AcademicTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_week', models.IntegerField()),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='act_acy', to='curriculum.academicyear')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_year_term', to='curriculum.term')),
            ],
            options={
                'verbose_name': 'Academic Term',
                'verbose_name_plural': 'Academic Term',
                'db_table': 'academic_term',
            },
        ),
        migrations.AddField(
            model_name='teachingcalendar',
            name='academic_term',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ac_tc', to='curriculum.academicterm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teachingreport',
            name='workload',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='report_workload', to='curriculum.workload'),
            preserve_default=False,
        ),
    ]
