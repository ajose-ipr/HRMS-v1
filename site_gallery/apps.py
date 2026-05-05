"""
Django app config for site_gallery
"""

from django.apps import AppConfig


class SiteGalleryConfig(AppConfig):
    """Site Gallery application configuration"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "site_gallery"

    def ready(self):
        """Initialize app on Django startup"""
        import site_gallery.signals  # noqa
