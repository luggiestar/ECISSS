from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import AcademicTerm
from ..forms import AcademicTermForm
from django.db.utils import IntegrityError


def academic_term_list(request):
    get_academic_term = AcademicTerm.objects.all()
    if request.method == 'POST':
        form = AcademicTermForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Academic year created successfully")
            return redirect('academic_term_list')
        else:
            messages.error(request, f"{form.errors['__all__']}")
            return redirect('academic_term_list')

    context = {
        'academic_terms': get_academic_term,
        'form': AcademicTermForm
    }

    return render(request, 'pages/academic-term.html', context)


def edit_academic_term(request, academic_term_id):
    instance = AcademicTerm.objects.filter(id=academic_term_id).first()
    if request.method == 'POST':
        try:
            form = AcademicTermForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, f"Academic term edited successfully")
                    return redirect('academic_term_list')

                except IntegrityError:
                    messages.error(request, f"Academic term with the given name all ready exist")
                    return redirect('academic_term_list')

        except IntegrityError:
            messages.error(request, f"Academic term with the given id does not exist")
            return redirect('academic_term_list')

    context = {
        'form': AcademicTermForm(instance=instance)
    }

    return render(request, 'pages/edit-Academic-term.html', context)


def delete_academic_term(request):
    if request.method == 'POST':
        academic_term_id = request.POST['academic_term_id']
        try:
            get_academic_term = get_object_or_404(AcademicTerm, id=academic_term_id)
            name = f'{get_academic_term.academic_year}-{get_academic_term.term}'
            get_academic_term.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('academic_term_list')
        except IntegrityError:
            messages.error(request, f"Academic year with the given id does not exist")
            return redirect('academic_term_list')
