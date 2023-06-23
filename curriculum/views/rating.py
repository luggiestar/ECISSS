from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ..forms import StaffForm, StaffEntryForm
from ..models import *


def rating(request):
    topics = Topic.objects.all()
    # subjects = Subject.objects.annotate(num_topic=Count('topic_subject')).values('num_topic', 'name')
    workload = TeachingReport.objects.filter(calendar__topic__in=topics)
    print(workload.count())
    context = {
        'topics': topics,
    }
    return render(request, 'pages/rating.html', context)
