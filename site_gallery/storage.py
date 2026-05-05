"""
Storage backend for site gallery photos.

This module provides an abstraction layer for photo storage,
making it easy to swap between local and cloud storage (S3, etc.)
without changing the rest of the application.
"""

import os
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class GalleryStorageBackend:
    """
    Abstract base class for gallery storage backends.
    Subclasses should implement the storage method.
    """

    def get_storage(self):
        """
        Return the storage backend instance.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_storage()")


class LocalGalleryStorage(GalleryStorageBackend):
    """
    Local file system storage backend for gallery photos.
    Uses Django's MEDIA_ROOT / MEDIA_URL by default.
    """

    def get_storage(self):
        """Return the local file system storage"""
        gallery_root = os.path.join(settings.MEDIA_ROOT, "gallery")
        # Ensure directory exists
        Path(gallery_root).mkdir(parents=True, exist_ok=True)

        return FileSystemStorage(
            location=gallery_root,
            base_url=f"{settings.MEDIA_URL}gallery/",
        )


class S3GalleryStorage(GalleryStorageBackend):
    """
    AWS S3 storage backend for gallery photos.
    Requires django-storages and boto3.
    """

    def get_storage(self):
        """Return S3 storage if configured"""
        try:
            from storages.backends.s3boto3 import S3Boto3Storage

            class CustomS3Storage(S3Boto3Storage):
                location = "gallery"
                default_acl = "public-read"
                querystring_auth = False

            return CustomS3Storage()
        except ImportError:
            raise ImportError(
                "django-storages and boto3 are required for S3 storage. "
                "Install them with: pip install django-storages boto3"
            )


# Factory function to get the appropriate storage backend
def get_gallery_storage():
    """
    Get the configured storage backend.
    Uses LOCAL_GALLERY_STORAGE setting or defaults to LocalGalleryStorage.
    """
    storage_backend_class = getattr(
        settings, "GALLERY_STORAGE_BACKEND", LocalGalleryStorage
    )

    # If it's a string, import it
    if isinstance(storage_backend_class, str):
        from django.utils.module_loading import import_string

        storage_backend_class = import_string(storage_backend_class)

    backend = storage_backend_class()
    return backend.get_storage()
