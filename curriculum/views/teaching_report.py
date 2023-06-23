from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import TeachingCalendar, Workload, TeachingReport, Staff
from ..forms import TeachingReportForm
import datetime


@login_required(login_url='/')
def teaching_report(request, workload_id):
    get_workload = Workload.objects.filter(id=workload_id, teacher__user=request.user).first()

    subject = get_workload.subject
    level = get_workload.level
    today = datetime.date.today()

    get_teaching_calendar = TeachingCalendar.objects.filter(topic__subject=subject, topic__level=level,
                                                            start_date__lte=today, end_date__gte=today).first()
    form = TeachingReportForm()

    get_current_report = TeachingReport.objects.filter(calendar=get_teaching_calendar).count()
    if request.method == "POST":

        form = TeachingReportForm(request.POST)
        if form.is_valid():
            get_save = form.save(commit=False)

            workload_id = request.POST['workload_id']
            calendar = request.POST['calendar']

            get_workload = Workload.objects.filter(id=workload_id).first()
            get_calendar = TeachingCalendar.objects.filter(id=calendar).first()

            get_save.workload = get_workload
            get_save.calendar = get_calendar
            get_save.save()
            messages.success(request, "Report Saved successfully")
            return redirect('teaching_report', workload_id)
        else:
            messages.error(request, f"Report not Saved successfully {form.errors}")
            return redirect('teaching_report', workload_id)

    context = {
        'calendar': get_teaching_calendar,
        'form': form,
        'workload_id': workload_id,
        'count_current': get_current_report
    }
    return render(request, 'pages/teaching-report.html', context)


@login_required(login_url='/')
def teaching_report_verify(request):
    # select according to user school
    get_reports = TeachingReport.objects.filter(is_verified=False)
    context = {
        'reports': get_reports
    }
    return render(request, 'pages/teaching-report-verifying.html', context)


@login_required(login_url='/')
def teaching_report_history(request):
    get_staff = Staff.objects.filter(user=request.user).first()
    role = get_staff.role.name

    if request.user.is_superuser or role == "academic master" or role == "head master":
        get_reports = TeachingReport.objects.all()

    elif role == "teacher":
        get_reports = TeachingReport.objects.filter(workload__teacher__user=request.user)

    context = {
        'reports': get_reports
    }
    return render(request, 'pages/teaching-report-history.html', context)


@login_required(login_url='/')
def verify_report(request, report_id):
    get_report = TeachingReport.objects.filter(is_verified=False, id=report_id).first()

    if request.method == "POST":
        report_id = request.POST['report_id']
        get_verifier = Staff.objects.filter(user=request.user).first()
        update_report = TeachingReport.objects.filter(is_verified=False, id=report_id).first()
        update_report.is_verified = True
        update_report.verifier = get_verifier
        update_report.save()
        messages.success(request, "Report Verified successfully")
        return redirect('verify')

    context = {
        'report': get_report,
    }
    return render(request, 'pages/report-verifying.html', context)
