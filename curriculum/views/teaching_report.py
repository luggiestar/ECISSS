from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import AcademicYear, TeachingReport


@login_required(login_url='/')
def teaching_report(request, workload_id):
    get_academic_year = AcademicYear.objects.filter(is_current=True).first()
    get_teaching_report = TeachingReport.objects.filter(workload__teacher__user=request.user, workload__id=workload_id,
                                                        academic_year=get_academic_year)
    context = {
        'reports': get_teaching_report,
        'academic_year': get_academic_year,
    }
    return render(request, 'pages/teaching-report.html', context)
