"""
Signal handlers for site gallery app
"""

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache

from site_gallery.models import Photo, Location, Project


@receiver(post_delete, sender=Photo)
def clear_gallery_cache_on_photo_delete(sender, instance, **kwargs):
    """Clear cache when a photo is deleted"""
    cache.delete("gallery_photos_list")


@receiver(pre_save, sender=Location)
def clear_gallery_cache_on_location_save(sender, instance, **kwargs):
    """Clear cache when a location is saved"""
    cache.delete("gallery_locations_list")


@receiver(pre_save, sender=Project)
def clear_gallery_cache_on_project_save(sender, instance, **kwargs):
    """Clear cache when a project is saved"""
    cache.delete("gallery_projects_list")
