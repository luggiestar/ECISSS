from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import AcademicYear
from ..forms import AcademicYearForm
from django.db.utils import IntegrityError


def academic_year_list(request):
    get_academic_year = AcademicYear.objects.all()
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Academic year created successfully")
            return redirect('academic_year_list')
        else:
            messages.error(request, f"{form.errors['name']}")
            return redirect('academic_year_list')

    context = {
        'academic_years': get_academic_year,
        'form': AcademicYearForm
    }

    return render(request, 'pages/academic-year.html', context)


def edit_academic_year(request, academic_year_id):
    instance = AcademicYear.objects.filter(id=academic_year_id).first()
    if request.method == 'POST':
        try:
            form = AcademicYearForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, f"Academic year edited successfully")
                    return redirect('academic_year_list')

                except IntegrityError:
                    messages.error(request, f"Academic year with the given name all ready exist")
                    return redirect('academic_year_list')

        except IntegrityError:
            messages.error(request, f"Academic year with the given id does not exist")
            return redirect('academic_year_list')

    context = {
        'form': AcademicYearForm(instance=instance)
    }

    return render(request, 'pages/edit-Academic-year.html', context)


def delete_academic_year(request):
    if request.method == 'POST':
        academic_year_id = request.POST['academic_year_id']
        try:
            get_academic_year = get_object_or_404(AcademicYear, id=academic_year_id)
            name = f'{get_academic_year.name}'
            get_academic_year.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('academic_year_list')
        except IntegrityError:
            messages.error(request, f"Academic year with the given id does not exist")
            return redirect('academic_year_list')