from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Subject, Term
from ..forms import SubjectForm, TermForm


def subject_list(request):
    get_subject = Subject.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            get_form = form.save(commit=False)
            get_form.name = request.POST['name'].upper()
            get_form.save()

            messages.success(request, f"Subject created successfully")
            return redirect('subject_list')
        else:
            messages.error(request, f"Subject not created successfully")
            return redirect('subject_list')

    context = {
        'subjects': get_subject,
        'form': SubjectForm
    }

    return render(request, 'pages/subjects.html', context)


def edit_subject(request, subject_id):
    instance = Subject.objects.filter(id=subject_id).first()
    if request.method == 'POST':
        try:
            form = SubjectForm(request.POST, instance=instance)
            if form.is_valid():
                get_form = form.save(commit=False)
                get_form.name = request.POST['name'].upper()
                get_form.save()
                messages.success(request, f"Subject edited successfully")
                return redirect('subject_list')
        except:
            messages.error(request, f"Subject with the given id does not exist")
            return redirect('subject_list')
    context = {
        'form': SubjectForm(instance=instance)
    }

    return render(request, 'pages/edit-subject.html', context)


def delete_subject(request):
    if request.method == 'POST':
        subject_id = request.POST['subject_id']
        try:
            get_subject = get_object_or_404(Subject, id=subject_id)
            name = f'{get_subject.name}'
            get_subject.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('subject_list')
        except:
            messages.error(request, f"Subject with the given id does not exist")
            return redirect('subject_list')
