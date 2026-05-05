"""
Models for site gallery feature.

Defines Location, Project, and Photo models for the site photo gallery.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from site_gallery.storage import get_gallery_storage


class Location(models.Model):
    """Location tag for photos"""

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Location name (e.g., Office, Conference Room, Outdoor)"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """Project tag for photos"""

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Project name"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Photo model for the gallery"""

    image = models.ImageField(
        upload_to="gallery/%Y/%m/%d/",
        storage=get_gallery_storage,
        help_text=_("Photo image file"),
    )
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gallery_photos",
        help_text=_("User who uploaded the photo"),
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Date and time of upload"),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="photos",
        help_text=_("Location tag for the photo"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="photos",
        help_text=_("Project tag for the photo"),
    )
    caption = models.TextField(
        blank=True,
        default="",
        help_text=_("Optional caption or description"),
    )

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        ordering = ["-upload_date"]
        indexes = [
            models.Index(fields=["-upload_date"]),
            models.Index(fields=["location"]),
            models.Index(fields=["project"]),
            models.Index(fields=["uploader"]),
        ]

    def __str__(self):
        return f"Photo by {self.uploader.username} on {self.upload_date.strftime('%Y-%m-%d')}"

    def delete(self, *args, **kwargs):
        """Delete photo file when model instance is deleted"""
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
