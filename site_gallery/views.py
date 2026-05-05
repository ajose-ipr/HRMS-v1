"""
Views for site gallery feature
"""

import json
import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from PIL import Image
from io import BytesIO

from site_gallery.models import Location, Project, Photo
from site_gallery.forms import PhotoForm, LocationForm, ProjectForm, PhotoFilterForm


@login_required
@require_http_methods(["GET"])
def gallery_list(request):
    """
    Display the photo gallery with filters
    """
    photos = Photo.objects.select_related("uploader", "location", "project").all()

    # Apply filters
    location_id = request.GET.get("location")
    project_id = request.GET.get("project")
    uploader = request.GET.get("uploader")

    if location_id:
        photos = photos.filter(location_id=location_id)
    if project_id:
        photos = photos.filter(project_id=project_id)
    if uploader:
        photos = photos.filter(
            Q(uploader__username__icontains=uploader)
            | Q(uploader__first_name__icontains=uploader)
            | Q(uploader__last_name__icontains=uploader)
        )

    # Get unique locations and projects for filter dropdowns
    locations = Location.objects.all()
    projects = Project.objects.all()

    context = {
        "photos": photos,
        "locations": locations,
        "projects": projects,
        "filter_form": PhotoFilterForm(),
    }

    return render(request, "site_gallery/gallery_list.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def photo_upload(request):
    """
    Handle bulk photo upload with metadata
    """
    if request.method == "POST":
        return handle_photo_upload(request)

    # GET request - return upload form
    context = {
        "locations": Location.objects.all(),
        "projects": Project.objects.all(),
    }
    return render(request, "site_gallery/upload_modal.html", context)


def handle_photo_upload(request):
    """
    Process the photo upload
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": _("Not authenticated")}, status=401)

    uploaded_files = request.FILES.getlist("images")

    # Enforce 20-photo limit
    if len(uploaded_files) > 20:
        return JsonResponse(
            {"error": _("Maximum 20 photos per upload allowed")},
            status=400,
        )

    location_name = request.POST.get("location_name", "").strip()
    project_name = request.POST.get("project_name", "").strip()
    caption = request.POST.get("caption", "").strip()

    # Get or create location
    location = None
    if location_name:
        location, _ = Location.objects.get_or_create(name=location_name)

    # Get or create project
    project = None
    if project_name:
        project, _ = Project.objects.get_or_create(name=project_name)

    uploaded_photos = []
    errors = []

    for uploaded_file in uploaded_files:
        try:
            # Validate that it's an image
            img = Image.open(uploaded_file)
            img.verify()

            # Reset file pointer
            uploaded_file.seek(0)

            # Create photo instance
            photo = Photo.objects.create(
                image=uploaded_file,
                uploader=request.user,
                location=location,
                project=project,
                caption=caption,
            )

            uploaded_photos.append(
                {
                    "id": photo.id,
                    "image_url": photo.image.url,
                    "uploader": photo.uploader.get_full_name()
                    or photo.uploader.username,
                    "upload_date": photo.upload_date.isoformat(),
                    "caption": photo.caption,
                }
            )

        except Exception as e:
            errors.append(
                {
                    "filename": uploaded_file.name,
                    "error": str(e),
                }
            )

    response_data = {
        "uploaded": uploaded_photos,
        "errors": errors,
        "count": len(uploaded_photos),
    }

    if errors:
        response_data["partial_error"] = True

    return JsonResponse(response_data)


@login_required
@require_http_methods(["DELETE"])
def photo_delete(request, photo_id):
    """
    Delete a photo (admin only)
    """
    if not request.user.is_staff:
        return HttpResponseForbidden(
            json.dumps({"error": _("Only admins can delete photos")}),
            content_type="application/json",
        )

    photo = get_object_or_404(Photo, id=photo_id)

    try:
        photo.delete()
        return JsonResponse(
            {"success": True, "message": _("Photo deleted successfully")}
        )
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400,
        )


@login_required
@require_http_methods(["POST", "GET"])
def location_api(request):
    """
    Get list of locations or create a new one
    """
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return JsonResponse(
                {
                    "id": location.id,
                    "name": location.name,
                    "created": True,
                }
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # GET - return locations list
    locations = Location.objects.all().values("id", "name")
    return JsonResponse({"locations": list(locations)})


@login_required
@require_http_methods(["POST", "GET"])
def project_api(request):
    """
    Get list of projects or create a new one
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return JsonResponse(
                {
                    "id": project.id,
                    "name": project.name,
                    "created": True,
                }
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # GET - return projects list
    projects = Project.objects.all().values("id", "name")
    return JsonResponse({"projects": list(projects)})


@login_required
@require_http_methods(["GET"])
def gallery_api(request):
    """
    API endpoint to fetch gallery photos with filters (for AJAX/JSON)
    """
    photos = Photo.objects.select_related("uploader", "location", "project").all()

    # Apply filters
    location_id = request.GET.get("location")
    project_id = request.GET.get("project")
    uploader = request.GET.get("uploader")

    if location_id:
        photos = photos.filter(location_id=location_id)
    if project_id:
        photos = photos.filter(project_id=project_id)
    if uploader:
        photos = photos.filter(
            Q(uploader__username__icontains=uploader)
            | Q(uploader__first_name__icontains=uploader)
            | Q(uploader__last_name__icontains=uploader)
        )

    photos_data = [
        {
            "id": photo.id,
            "image_url": photo.image.url,
            "uploader": photo.uploader.get_full_name() or photo.uploader.username,
            "upload_date": photo.upload_date.isoformat(),
            "location": photo.location.name if photo.location else None,
            "project": photo.project.name if photo.project else None,
            "caption": photo.caption,
            "can_delete": request.user.is_staff,
        }
        for photo in photos
    ]

    return JsonResponse({"photos": photos_data, "count": len(photos_data)})
