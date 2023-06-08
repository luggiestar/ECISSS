from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import AcademicYear, TeachingCalendar, Workload
import datetime

@login_required(login_url='/')
def teaching_report(request, workload_id):
    get_workload = Workload.objects.filter(id=workload_id, teacher__user=request.user).first()
    subject = get_workload.subject
    level = get_workload.level
    today = datetime.date.today()
    get_teaching_calendar = TeachingCalendar.objects.filter(topic__subject=subject, topic__level=level,
                                                            start_date__lte=today, end_date__gte=today).first()
    context = {
        'calendar': get_teaching_calendar
    }
    return render(request, 'pages/teaching-report.html', context)
