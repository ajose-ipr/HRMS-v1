"""
INSTALLATION & SETUP GUIDE FOR SITE GALLERY FEATURE

This document provides step-by-step instructions to install and configure the
Site Gallery feature in Horilla HRMS.

========================================
STEP 1: VERIFY INSTALLATION
========================================

The site_gallery app has been created with the following structure:

site_gallery/
├── __init__.py
├── apps.py                          # Django app configuration
├── models.py                        # Location, Project, Photo models
├── views.py                         # Gallery views and endpoints
├── urls.py                          # URL configuration
├── forms.py                         # Django forms
├── admin.py                         # Django admin configuration
├── tests.py                         # Unit tests
├── filters.py                       # FilterSet definitions
├── storage.py                       # Storage backend (local, S3, custom)
├── decorators.py                    # Permission decorators
├── context_processors.py            # Context processors
├── signals.py                       # Django signals
├── sidebar.py                       # Sidebar menu configuration
├── requirements.txt                 # Dependencies
├── README.md                        # Documentation
├── management/
│   └── commands/
│       └── create_gallery_demo_data.py  # Demo data generator
├── migrations/                      # Database migrations
├── templates/
│   └── site_gallery/
│       ├── gallery_list.html        # Main gallery view
│       └── upload_modal.html        # Upload modal
└── static/
    └── site_gallery/
        ├── css/
        │   └── gallery.css          # Gallery styles
        └── js/
            └── gallery.js           # Gallery JavaScript

========================================
STEP 2: UPDATE INSTALLED_APPS & SIDEBARS
========================================

✓ DONE: site_gallery has been added to INSTALLED_APPS in horilla/horilla_apps.py
✓ DONE: site_gallery has been added to SIDEBARS in horilla/horilla_apps.py

========================================
STEP 3: UPDATE URLS
========================================

✓ DONE: site_gallery URLs have been included in horilla/urls.py
✓ DONE: Media file serving has been enabled in horilla/urls.py

========================================
STEP 4: RUN MIGRATIONS
========================================

Execute the following commands to create the database tables:

    cd "d:\Work Files\Workspace\Project 6 (Emp Portal)"
    python manage.py makemigrations site_gallery
    python manage.py migrate site_gallery

This will create:
- site_gallery_location table
- site_gallery_project table
- site_gallery_photo table

========================================
STEP 5: CREATE DEMO DATA (OPTIONAL)
========================================

To populate the gallery with sample photos for testing:

    python manage.py create_gallery_demo_data --count=10

To clear existing data and create fresh demo data:

    python manage.py create_gallery_demo_data --count=10 --clear

========================================
STEP 6: VERIFY INSTALLATION
========================================

1. Start Django development server:
    python manage.py runserver

2. Log in to the application

3. You should see "Photo Gallery" in the sidebar menu

4. Click on "Photo Gallery" -> "Gallery" to access the gallery

========================================
FEATURES VERIFICATION CHECKLIST
========================================

□ Gallery displays photos in grid layout (newest first)
□ Filter bar works for Location, Project, and Uploader
□ Upload button opens modal dialog
□ Drag-and-drop works for file upload
□ File picker works as fallback
□ 20-photo limit is enforced
□ Photos are saved with correct metadata:
  - Uploader (auto-filled)
  - Upload date (auto-filled)
  - Location (optional, can create new)
  - Project (optional, can create new)
  - Caption (optional)
□ Admin users see delete button on hover
□ Non-admin users don't see delete button
□ Delete button removes photo from gallery
□ Responsive design works on mobile/tablet

========================================
CONFIGURATION OPTIONS
========================================

LOCAL FILE STORAGE (DEFAULT)
No additional configuration needed. Photos are stored in:
    MEDIA_ROOT/gallery/

AWS S3 STORAGE
Add to settings.py or .env:

    GALLERY_STORAGE_BACKEND = 'site_gallery.storage.S3GalleryStorage'
    AWS_ACCESS_KEY_ID = 'your-access-key'
    AWS_SECRET_ACCESS_KEY = 'your-secret-key'
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'us-east-1'

First install required packages:
    pip install django-storages boto3

CUSTOM STORAGE BACKEND
Create a custom backend class and configure:

    GALLERY_STORAGE_BACKEND = 'myapp.storage.MyCustomStorage'

========================================
DATABASE SCHEMA
========================================

Location Table:
- id (BigAutoField, Primary Key)
- name (CharField, max_length=100, unique=True)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)

Project Table:
- id (BigAutoField, Primary Key)
- name (CharField, max_length=100, unique=True)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)

Photo Table:
- id (BigAutoField, Primary Key)
- image (ImageField, upload_to='gallery/%Y/%m/%d/')
- uploader (ForeignKey to User, on_delete=CASCADE)
- upload_date (DateTimeField, auto_now_add=True)
- location (ForeignKey to Location, null=True, blank=True)
- project (ForeignKey to Project, null=True, blank=True)
- caption (TextField, blank=True, default='')

Indexes:
- (-upload_date) for chronological sorting
- (location) for location filtering
- (project) for project filtering
- (uploader) for uploader filtering

========================================
API ENDPOINTS
========================================

GET /gallery/
- View the photo gallery with filters
- Auth: Required (is_authenticated)
- Returns: HTML page

POST /gallery/upload/
- Upload photos with metadata
- Auth: Required
- Max files: 20 per request
- Fields: images, location_name, project_name, caption
- Returns: JSON with uploaded photos and errors

DELETE /gallery/<id>/
- Delete a photo
- Auth: Required (is_staff)
- Returns: JSON success/error

GET /gallery/api/
- Get gallery photos as JSON
- Auth: Required
- Query params: location, project, uploader
- Returns: JSON array of photos

GET/POST /api/locations/
- Get locations or create new
- Auth: Required
- Returns: JSON list or created location

GET/POST /api/projects/
- Get projects or create new
- Auth: Required
- Returns: JSON list or created project

========================================
PERMISSIONS & ACCESS CONTROL
========================================

View Gallery:
- Any authenticated user

Upload Photos:
- Any authenticated user
- Max 20 photos per upload
- Bulk upload supported

Delete Photos:
- Admin users only (is_staff=True)
- Delete button only visible to admins
- API enforces admin check

Edit Photos:
- Currently not supported (by design)
- Photos can only be uploaded or deleted

========================================
TROUBLESHOOTING
========================================

Q: Gallery sidebar menu not showing
A: 1. Clear browser cache
   2. Restart Django development server
   3. Verify site_gallery is in INSTALLED_APPS and SIDEBARS
   4. Check database migrations are run

Q: Upload photos but they don't display
A: 1. Check MEDIA_ROOT directory exists and is writable
   2. Verify MEDIA_URL is correctly configured
   3. Check that media serving is enabled in urls.py
   4. Check browser console for JavaScript errors

Q: "Maximum 20 photos" error on client side
A: This is expected behavior. The 20-photo limit is enforced:
   - Client-side: JavaScript prevents upload of 20+ files
   - Server-side: Django view enforces the same limit

Q: Photos uploaded but filters don't work
A: 1. Ensure locations/projects are selected during upload
   2. Try filtering with exact names
   3. Check database queries in Django debug toolbar

Q: S3 storage not working
A: 1. Verify AWS credentials are correct
   2. Verify bucket exists and has public-read permissions
   3. Install required packages: pip install django-storages boto3
   4. Check Django logs for specific errors

Q: Permission denied on delete
A: Only staff users (is_staff=True) can delete photos. 
   Make sure the user is marked as staff in admin panel.

========================================
RUNNING TESTS
========================================

Run all gallery tests:
    python manage.py test site_gallery

Run specific test class:
    python manage.py test site_gallery.tests.SiteGalleryModelTests

Run specific test method:
    python manage.py test site_gallery.tests.SiteGalleryModelTests.test_photo_creation

Coverage report:
    pip install coverage
    coverage run --source='site_gallery' manage.py test site_gallery
    coverage report

========================================
ADMIN INTERFACE
========================================

Access Django admin at: /admin/

Gallery Admin Features:
- View all photos with filters
- Search by caption or uploader
- Filter by date, location, project, or uploader
- Image preview in admin
- Delete photos from admin
- Add/edit locations and projects
- View photo metadata

========================================
PERFORMANCE CONSIDERATIONS
========================================

Caching:
- Locations and projects are cached to reduce database queries
- Cache is cleared when new items are created
- Consider enabling Django caching for production

Pagination:
- Current implementation loads all photos
- For large galleries (1000+ photos), consider adding pagination
- Modify gallery_list.html to add pagination

Image Optimization:
- Original images are stored as-is
- For production, consider:
  - Image compression on upload
  - Thumbnail generation
  - CDN integration

Database:
- Indexes are created for common filter queries
- Location, Project, and Photo models use BigAutoField
- Deletion cascades are handled appropriately

========================================
FUTURE ENHANCEMENTS
========================================

Possible features to add:
- [ ] Photo editing/cropping
- [ ] Pagination
- [ ] Full-text search
- [ ] Batch operations (multi-delete)
- [ ] Photo tagging system
- [ ] User-specific galleries
- [ ] Photo sharing/permissions
- [ ] Comments on photos
- [ ] Like/favorite functionality
- [ ] Analytics/statistics
- [ ] API rate limiting
- [ ] Webhook integration

========================================
SUPPORT & DOCUMENTATION
========================================

Main README: site_gallery/README.md
This file: site_gallery/INSTALLATION_GUIDE.md

For Horilla documentation: https://horilla.readthedocs.io/

========================================
VERSION INFORMATION
========================================

Site Gallery Version: 1.0.0
Horilla Version: Required 4.1+
Django Version: Required 4.1+
Python Version: Required 3.8+

========================================
END OF INSTALLATION GUIDE
========================================
"""
