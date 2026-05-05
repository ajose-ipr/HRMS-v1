"""
Django admin configuration for site gallery
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from site_gallery.models import Location, Project, Photo


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin interface for Location model"""

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model"""

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin interface for Photo model"""

    list_display = (
        "id",
        "uploader",
        "upload_date",
        "location",
        "project",
        "caption_preview",
    )
    list_filter = ("upload_date", "location", "project", "uploader")
    search_fields = ("caption", "uploader__username", "location__name", "project__name")
    readonly_fields = ("uploader", "upload_date", "image_preview")
    fieldsets = (
        (
            _("Image"),
            {"fields": ("image", "image_preview")},
        ),
        (
            _("Metadata"),
            {"fields": ("uploader", "upload_date", "location", "project", "caption")},
        ),
    )

    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="200" height="auto" />'
        return _("No image")

    image_preview.allow_tags = True
    image_preview.short_description = _("Preview")

    def caption_preview(self, obj):
        """Display truncated caption"""
        if obj.caption:
            return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
        return _("No caption")

    caption_preview.short_description = _("Caption")

    def save_model(self, request, obj, form, change):
        """Set uploader to current user on creation"""
        if not change:
            obj.uploader = request.user
        super().save_model(request, obj, form, change)

    actions = ["delete_selected"]
