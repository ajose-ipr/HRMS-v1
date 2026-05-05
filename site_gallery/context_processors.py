"""
Context processors for site gallery
"""

from django.db.models import Count

from site_gallery.models import Location, Project


def gallery_context(request):
    """
    Add gallery-related context to all templates
    """
    if not request.user.is_authenticated:
        return {}

    context = {
        "gallery_stats": {
            "total_locations": Location.objects.count(),
            "total_projects": Project.objects.count(),
        }
    }

    return context
