from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Term
from ..forms import TermForm


def term_list(request):
    get_term = Term.objects.all()
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            try:
                get_form = form.save(commit=False)
                get_form.name = request.POST['name'].upper()
                get_form.save()
                messages.success(request, f"Term created successfully")
                return redirect('term_list')
            except IntegrityError:
                messages.error(request, f"Term with the given name all ready exist")
                return redirect('term_list')
        else:
            messages.error(request, f"Term not created successfully")
            return redirect('term_list')

    context = {
        'terms': get_term,
        'form': TermForm
    }

    return render(request, 'pages/terms.html', context)


def edit_term(request, term_id):
    instance = Term.objects.filter(id=term_id).first()
    if request.method == 'POST':
        try:
            form = TermForm(request.POST, instance=instance)
            if form.is_valid():
                try:
                    get_form = form.save(commit=False)
                    get_form.name = request.POST['name'].upper()
                    get_form.save()
                    messages.success(request, f"Term edited successfully")
                    return redirect('term_list')
                except IntegrityError:
                    messages.error(request, f"Term with the given name all ready exist")
                    return redirect('term_list')
        except:
            messages.error(request, f"Term with the given id does not exist")
            return redirect('term_list')
    context = {
        'form': TermForm(instance=instance)
    }

    return render(request, 'pages/edit-term.html', context)


def delete_term(request):
    if request.method == 'POST':
        term_id = request.POST['term_id']
        try:
            get_term = get_object_or_404(Term, id=term_id)
            name = f'{get_term.name}'
            get_term.delete()
            messages.success(request, f"{name} deleted successfully")
            return redirect('term_list')
        except:
            messages.error(request, f"Term with the given id does not exist")
            return redirect('term_list')
