"""
URL configuration for site gallery
"""

from django.urls import path

from site_gallery import views

app_name = "site_gallery"

urlpatterns = [
    # Gallery views
    path("gallery/", views.gallery_list, name="gallery-list"),
    path("gallery/api/", views.gallery_api, name="gallery-api"),
    
    # Upload views
    path("gallery/upload/", views.photo_upload, name="photo-upload"),
    
    # Delete view
    path("gallery/<int:photo_id>/delete/", views.photo_delete, name="photo-delete"),
    
    # Location API
    path("api/locations/", views.location_api, name="location-api"),
    
    # Project API
    path("api/projects/", views.project_api, name="project-api"),
]
