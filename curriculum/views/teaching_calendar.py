from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import TeachingCalendar
from ..forms import TeachingCalendarForm
from django.db.utils import IntegrityError


def teaching_calendar_list(request):
    get_teaching_calendar = TeachingCalendar.objects.all()
    if request.method == 'POST':
        form = TeachingCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Teaching calendar created successfully")
            return redirect('teaching_calendar_list')
        else:
            messages.error(request, f"{form.errors['__all__']}")
            return redirect('teaching_calendar_list')

    context = {
        'teaching_calendars': get_teaching_calendar,
        'form': TeachingCalendarForm
    }

    return render(request, 'pages/teaching-calendar.html', context)


def edit_teaching_calendar(request, teaching_calendar_id):
    instance = TeachingCalendar.objects.filter(id=teaching_calendar_id).first()
    if request.method == 'POST':
        try:
            form = TeachingCalendarForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, f"Teaching calendar edited successfully")
                    return redirect('teaching_calendar_list')

                except IntegrityError:
                    messages.error(request, f"Teaching calendar with the given name all ready exist")
                    return redirect('teaching_calendar_list')

        except IntegrityError:
            messages.error(request, f"Teaching calendar with the given id does not exist")
            return redirect('teaching_calendar_list')

    context = {
        'form': TeachingCalendarForm(instance=instance)
    }

    return render(request, 'pages/edit-teaching-calendar.html', context)


def delete_teaching_calendar(request):
    if request.method == 'POST':
        teaching_calendar_id = request.POST['teaching_calendar_id']
        try:
            get_academic_term = get_object_or_404(TeachingCalendar, id=teaching_calendar_id)
            get_academic_term.delete()
            messages.success(request, f"Deleted successfully")
            return redirect('teaching_calendar_list')
        except IntegrityError:
            messages.error(request, f"Teaching calendar with the given id does not exist")
            return redirect('teaching_calendar_list')
