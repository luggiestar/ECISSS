from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ..forms import StaffForm, StaffEntryForm
from ..models import Staff


@login_required(login_url='/')
def staffs(request):
    #
    # get_school = Staff.objects.filter(user=request.user).first()
    # get_staff_school = get_school.school
    get_staff = Staff.objects.all()
    form = StaffForm
    staff_entry_form = StaffEntryForm

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
        'form': form,
        'staff_form': staff_entry_form
    }

    return render(request, 'pages/registered-staff.html', context)
