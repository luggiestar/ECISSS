from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import WorkLoadForm
from ..models import Workload, Staff


@login_required(login_url='/')
def workload(request):
    get_staff = Staff.objects.filter(user=request.user).first()
    get_workload = Workload.objects.filter(teacher__school=get_staff.school)

    form = WorkLoadForm

    if request.method == "POST":
        form = WorkLoadForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request, "Workload created successfully")
        else:
            messages.error(request, "Workload not created successfully")
    context = {
        'workloads': get_workload,
        'form': form
    }
    return render(request, 'pages/workload.html', context)


@login_required(login_url='/')
def delete_workload(request):
    workload_id = request.POST['workload_id']
    get_workload = Workload.objects.filter(id=workload_id).first()
    get_workload.delete()

    return redirect("teaching_workload")


@login_required(login_url='/')
def edit_workload(request, workload_id):
    workload_instance = Workload.objects.filter(id=workload_id).first()
    form = WorkLoadForm(instance=workload_instance)

    if request.method == 'POST':
        form = WorkLoadForm(request.POST, instance=workload_instance)
        if form.is_valid():
            messages.success(request, f"Workload updated successfully")
            return redirect('teaching_workload')
        else:
            messages.success(request, f"Workload not updated successfully")
            return redirect('teaching_workload')

    context = {
        'form': form
    }

    return render(request, 'pages/edit-workload.html', context)
