from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import StaffForm, UserEditForm, ChangePasswordForm
from ..models import Staff


def staffs(request):
    get_staff = Staff.objects.all()
    form = StaffForm

    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff created successfully")
            return redirect('staff_list')
        else:
            messages.error(request, f"Staff note created successfully")
            return redirect('staff_list')

    context = {
        'staffs': get_staff,
        'form': form
    }

    return render(request, 'pages/registered-staff.html', context)
