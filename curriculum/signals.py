import decimal
import json
import string

import requests

from django.db import transaction
from django.db.models import Sum

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import request
from django.db.models.functions import Coalesce
from decimal import Decimal
from .models import *
from django.db.models import Sum


@receiver(post_save, sender=Workload, dispatch_uid='initiate_teaching_prgress')
def initiate_teaching_prgress(sender, instance, created, raw=False, **kwargs):
    # use the Coalesce function to substitute None values with a default value of 0
    # if created:
    if instance:
        try:
            initiate_progress = TeachingProgressSummary(
                subject=instance.subject,
                level=instance.level,
                school=instance.school,
                academic_year=instance.academic_year,
            )
            initiate_progress.save()
        except:
            pass


@receiver(post_save, sender=TeachingReport, dispatch_uid='update_teaching_prgress')
def update_teaching_prgress(sender, instance, created, raw=False, **kwargs):
    # use the Coalesce function to substitute None values with a default value of 0
    # if created:
    if created:
        get_verified_topic_total = TeachingReport.objects.filter(workload__subject=instance.workload.subject,
                                                                 is_verified=True).count()
        get_total_subject_topic = Topic.objects.filter(subject=instance.workload.subject,level=instance.workload.level).count()
        get_percentage = Decimal(get_verified_topic_total) /Decimal(get_total_subject_topic) * Decimal(100)
        TeachingProgressSummary.objects.filter(
            subject = instance.workload.subject,
            level = instance.workload.level,
            school = instance.workload.teacher.school,
            academic_year = instance.workload.academic_year
        ).update(percentage=get_percentage)


