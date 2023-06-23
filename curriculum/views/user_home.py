from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from ..models import User, Staff, School, Subject, TeachingProgressSummary


@login_required(login_url='/')
def dashboard(request):
    user_count = User.objects.all().count()
    staff_count = Staff.objects.all().count()
    school_count = School.objects.all().count()
    subject_count = Subject.objects.all().count()

    get_staff = Staff.objects.filter(user=request.user).first()
    summaries = TeachingProgressSummary.objects.filter(school=get_staff.school)
    total = TeachingProgressSummary.objects.filter(school=get_staff.school).aggregate(
        total_perc=Sum('percentage'))['total_perc']
    print(total)
    context = {
        'user_count': user_count,
        'staff_count': staff_count,
        'school_count': school_count,
        'subject_count': subject_count,
        'summaries': summaries,
        'total': total
    }
    return render(request, 'pages/index.html', context)
