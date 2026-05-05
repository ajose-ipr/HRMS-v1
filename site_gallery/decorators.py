"""
Decorators for site gallery app
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _


def gallery_upload_required(view_func):
    """
    Decorator to ensure user is authenticated and has upload permission.
    All authenticated users can upload by default.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            from django.urls import reverse

            return redirect(f"{reverse('login')}?next={request.path}")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def gallery_delete_required(view_func):
    """
    Decorator to ensure user is admin for photo deletion.
    Only staff/admin users can delete photos.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden(
                _("You do not have permission to perform this action.")
            )
        return view_func(request, *args, **kwargs)

    return wrapped_view
