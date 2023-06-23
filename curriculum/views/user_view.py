from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import UserForm, UserEditForm, ChangePasswordForm, StaffEntryForm, RoleForm
from ..models import User, Role


@login_required(login_url='/')
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


@login_required(login_url='/')
def user_profile(request):
    get_profile = User.objects.filter(id=request.user.id).first()
    form = ChangePasswordForm
    context = {
        'profile': get_profile,
        'form': form
    }

    return render(request, 'pages/user-profile.html', context)


@login_required(login_url='/')
def user_role(request):
    get_role = Role.objects.filter()
    form = RoleForm()
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Role created successfully")
            return redirect('user_role')
        else:
            messages.error(request, f"Role note created successfully")
            return redirect('user_role')

    context = {
        'roles': get_role,
        'form': form
    }

    return render(request, 'pages/user-role.html', context)


@login_required(login_url='/')
def delete_role(request):
    if request.method == 'POST':
        role_id = request.POST['role_id']

        get_role = get_object_or_404(Role, id=role_id)
        name = f'{get_role.name}'
        get_role.delete()
        messages.success(request, f"{name} deleted successfully")
        return redirect('user_role')


@login_required(login_url='/')
def edit_role(request, role_id):
    role_instance = User.objects.filter(id=role_id).first()
    form = RoleForm(instance=role_instance)

    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Role updated successfully")
            return redirect('user_list')
        else:
            messages.error(request, f"{form.errors}  Role not updated successfully")
            return redirect('user_list')

    context = {
        'form': form
    }

    return render(request, 'pages/edit-user.html', context)


@login_required(login_url='/')
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


@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            repeat_password = request.POST['repeat_password']

            if new_password == repeat_password:  # Check if two password match
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


@login_required(login_url='/')
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
            messages.error(request, f"{form.errors}  User not updated successfully")
            return redirect('user_list')

    context = {
        'form': form
    }

    return render(request, 'pages/edit-user.html', context)


@login_required(login_url='/')
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']

        get_user = get_object_or_404(User, id=user_id)
        name = f'{get_user.first_name} {get_user.last_name}'
        get_user.delete()
        messages.success(request, f"{name} deleted successfully")
        return redirect('user_list')


@login_required(login_url='/')
def set_superuser(request):
    user_id = request.GET['user_id']
    value = request.GET['value']

    get_user = get_object_or_404(User, id=user_id)
    get_user.is_superuser = value
    get_user.save()
    messages.success(request, "User Status updated successfully")
    return redirect('user_list')


@login_required(login_url='/')
def set_staff(request):
    user_id = request.GET['user_id']
    value = request.GET['value']
    # try:
    get_user = get_object_or_404(User, id=user_id)
    get_user.is_staff = value
    get_user.save()
    messages.success(request, "User Status updated successfully")

    return redirect('user_list')


@login_required(login_url='/')
def set_active(request):
    user_id = request.GET['user_id']
    value = request.GET['value']

    get_user = get_object_or_404(User, id=user_id)
    get_user.is_active = value
    get_user.save()
    messages.success(request, "User Status updated successfully")
    return redirect('user_list')
