from django.urls import reverse
from django.utils.translation import gettext_lazy as _

MENU = _("Expense Tracker")
IMG_SRC = "images/ui/expense.svg"

SUBMENUS = [
    {
        "menu": _("My Expenses"),
        "redirect": reverse("site_expense:my-expenses"),
    },
    {
        "menu": _("Team Expenses"),
        "redirect": reverse("site_expense:manager-expenses"),
    },
    {
        "menu": _("Monthly Analysis"),
        "redirect": reverse("site_expense:monthly-analysis"),
    },
]

def gallery_accessibility(request, submenu, user_perms, *args, **kwargs):
    return request.user.is_authenticated