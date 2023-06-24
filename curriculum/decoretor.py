from django.http import HttpResponseForbidden

from .models import Staff


def academic_required():
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Check if the user has the required role
            get_staff = Staff.objects.get(user=request.user)
            if get_staff.role.name == "academic master":
                return view_func(request, *args, **kwargs)
            else:
                # Redirect or raise an exception, depending on your requirements
                return HttpResponseForbidden('You do not have permission to access this page.')

        return wrapper

    return decorator


def head_required():
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Check if the user has the required role
            get_staff = Staff.objects.get(user=request.user)
            if get_staff.role.name == "head master":
                return view_func(request, *args, **kwargs)
            else:
                # Redirect or raise an exception, depending on your requirements
                return HttpResponseForbidden('You do not have permission to access this page.')

        return wrapper

    return decorator


