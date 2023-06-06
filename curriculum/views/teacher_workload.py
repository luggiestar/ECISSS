from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Staff, Workload, AcademicYear


@login_required(login_url='/')
def teacher_workload(request):
    get_academic_year = AcademicYear.objects.filter(is_current=True).first()
    workloads = Workload.objects.filter(teacher__user=request.user, academic_year=get_academic_year)
    context = {
        'workloads': workloads,
        'academic_year': get_academic_year,
    }
    return render(request, 'pages/teacher-workload.html', context)

