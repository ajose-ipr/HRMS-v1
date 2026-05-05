"""
Sidebar configuration for site gallery
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _


MENU = _("Photo Gallery")
IMG_SRC = "images/ui/gallery.svg"

SUBMENUS = [
    {
        "menu": _("Gallery"),
        "redirect": reverse("site_gallery:gallery-list"),
    },
]


def gallery_accessibility(request, submenu, user_perms, *args, **kwargs):
    """
    All authenticated users can access the gallery.
    """
    return request.user.is_authenticated
