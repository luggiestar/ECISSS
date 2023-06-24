from BeemAfrica import Authorize, SMS
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import *


@receiver(post_save, sender=Workload, dispatch_uid='update_teaching_progress')
def initiate_teaching_progress(sender, instance, created, raw=False, **kwargs):
    # use the Coalesce function to substitute None values with a default value of 0
    # if created:
    if instance:
        initiate_progress = TeachingProgressSummary(
            subject=instance.subject,
            level=instance.level,
            school=instance.teacher.school,
            academic_year=instance.academic_year,
        )
        initiate_progress.save()


@receiver(post_save, sender=User, dispatch_uid='send_user_message')
def send_user_message(sender, instance, created, raw=False, **kwargs):
    # use the Coalesce function to substitute None values with a default value of 0
    if created:
        phone = instance.phone[1:]
        fname = instance.first_name
        lname = instance.last_name
        username = instance.username
        message = f"Dear {fname} {lname}\nusername:{username} \npassword:{lname}"
        send_sms_func(phone, message)


@receiver(post_save, sender=TeachingReport, dispatch_uid='update_teaching_progress')
def update_teaching_progress(sender, instance, created, raw=False, **kwargs):
    # use the Coalesce function to substitute None values with a default value of 0
    # if created:
    if instance:
        get_verified_topic_total = TeachingReport.objects.filter(workload__subject=instance.workload.subject,
                                                                 is_verified=True).count()
        get_total_subject_topic = Topic.objects.filter(subject=instance.workload.subject,
                                                       level=instance.workload.level).count()
        get_percentage = Decimal(get_verified_topic_total) / Decimal(get_total_subject_topic) * Decimal(100)
        TeachingProgressSummary.objects.filter(
            subject=instance.workload.subject,
            level=instance.workload.level,
            school=instance.workload.teacher.school,
            academic_year=instance.workload.academic_year
        ).update(percentage=get_percentage)
        print("okkey")
    else:
        print("error")


def send_sms_func(phone, message):
    secret_key = "YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg=="
    access_key = "2799f1a807695012"
    Authorize(access_key, secret_key)
    phone = f'255{phone}'
    SMS.send_sms(message, phone)