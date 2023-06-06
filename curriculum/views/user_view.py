from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import UserForm, UserEditForm, ChangePasswordForm, StaffEntryForm
from ..models import User


def users(request):
    get_user = User.objects.all()
    form = UserForm
    user_entry_form = StaffEntryForm
    context = {
        'users': get_user,
        'form': form,
        'user_form': user_entry_form
    }

    return render(request, 'pages/users.html', context)


def user_profile(request):
    get_profile = User.objects.filter(id=request.user.id).first()
    form = ChangePasswordForm
    context = {
        'profile': get_profile,
        'form': form
    }

    return render(request, 'pages/user-profile.html', context)


def save_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"User created successfully")
            return redirect('user_list')
        else:
            messages.error(request, f"User note created successfully")
            return redirect('user_list')


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            repeat_password = request.POST['repeat_password']

            if new_password == repeat_password: # Check if two password match
                user_instance = User.objects.filter(id=request.user.id).first()
                current_password = form.cleaned_data['current_password']
                if user_instance.check_password(current_password):  # Check current password
                    user_instance.set_password(new_password)
                    user_instance.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('user_profile')
                else:
                    messages.error(request, 'Current password is incorrect.')
                    return redirect('user_profile')
            else:
                messages.error(request, 'Password must be the same.')
                return redirect('user_profile')
        else:
            messages.error(request, 'Server error try again')
            return redirect('user_profile')


def edit_user(request, user_id):
    user_instance = User.objects.filter(id=user_id).first()
    form = UserEditForm(instance=user_instance)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"User updated successfully")
            return redirect('user_list')
        else:
            messages.success(request, f"User not updated successfully")
            return redirect('user_list')

    context = {
        'form': form
    }

    return render(request, 'pages/edit-user.html', context)


def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']

        get_user = get_object_or_404(User, id=user_id)
        name = f'{get_user.first_name} {get_user.last_name}'
        get_user.delete()
        messages.success(request, f"{name} deleted successfully")
        return redirect('user_list')


def set_superuser(request):
    user_id = request.GET['user_id']
    value = request.GET['value']

    get_user = get_object_or_404(User, id=user_id)
    get_user.is_superuser = value
    get_user.save()
    messages.success(request, "User Status updated successfully")
    return redirect('user_list')


def set_staff(request):
    user_id = request.GET['user_id']
    value = request.GET['value']
    # try:
    get_user = get_object_or_404(User, id=user_id)
    get_user.is_staff = value
    get_user.save()
    messages.success(request, "User Status updated successfully")

    return redirect('user_list')


def set_active(request):
    user_id = request.GET['user_id']
    value = request.GET['value']

    get_user = get_object_or_404(User, id=user_id)
    get_user.is_active = value
    get_user.save()
    messages.success(request, "User Status updated successfully")
    return redirect('user_list')

