from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Level
from ..forms import LevelForm
from django.db.utils import IntegrityError


def level_list(request):
    get_level = Level.objects.all()
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            try:
                get_form = form.save(commit=False)
                get_form.name = request.POST['name'].upper()
                get_form.save()

                messages.success(request, f"Level created successfully")
                return redirect('level_list')
            except IntegrityError:
                messages.error(request, f"Level with the given name all ready exist")
                return redirect('level_list')
        else:
            messages.error(request, f"Level not created successfully")
            return redirect('level_list')

    context = {
        'levels': get_level,
        'form': LevelForm
    }

    return render(request, 'pages/levels.html', context)


def edit_level(request, level_id):
    instance = Level.objects.filter(id=level_id).first()
    if request.method == 'POST':
        try:
            form = LevelForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    get_form = form.save(commit=False)
                    get_form.name = request.POST['name'].upper()
                    get_form.save()
                    messages.success(request, f"Level edited successfully")
                    return redirect('level_list')
                except IntegrityError:
                    messages.error(request, f"Level with the given name all ready exist")
                    return redirect('level_list')
        except:
            messages.error(request, f"Level with the given id does not exist")
            return redirect('level_list')
    context = {
        'form': LevelForm(instance=instance)
    }

    return render(request, 'pages/edit-level.html', context)


def delete_level(request):
    if request.method == 'POST':
        level_id = request.POST['level_id']
        try:
            get_level = get_object_or_404(Level, id=level_id)
            name = f'{get_level.name}'
            get_level.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('level_list')
        except:
            messages.error(request, f"Level with the given id does not exist")
            return redirect('level_list')
