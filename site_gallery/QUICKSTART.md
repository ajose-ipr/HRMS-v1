"""
QUICK START GUIDE FOR SITE GALLERY

This guide provides the fastest way to get started with the Site Photo Gallery feature.

================================================================================
STEP 1: RUN MIGRATIONS (REQUIRED)
================================================================================

From the project root directory:

    python manage.py makemigrations site_gallery
    python manage.py migrate site_gallery

Expected output:
    Migrations for 'site_gallery':
      site_gallery/migrations/0001_initial.py
        - Create model Location
        - Create model Project
        - Create model Photo
    Operations to perform:
      Apply all migrations: site_gallery
    Running migrations:
      Applying site_gallery.0001_initial... OK

================================================================================
STEP 2: CREATE ADMIN USER (IF NEEDED)
================================================================================

If you don't have a superuser account yet:

    python manage.py createsuperuser

Follow the prompts to create your admin account.

================================================================================
STEP 3: (OPTIONAL) CREATE DEMO DATA
================================================================================

To populate the gallery with sample photos for testing:

    python manage.py create_gallery_demo_data --count=10

This creates:
- 10 sample photos with different colors
- 5 sample locations
- 5 sample projects
- Demo user account (if needed)

To clear and recreate demo data:

    python manage.py create_gallery_demo_data --count=10 --clear

================================================================================
STEP 4: START DEVELOPMENT SERVER
================================================================================

    python manage.py runserver

Or specify a port:

    python manage.py runserver 8000

Server will be available at: http://localhost:8000/

================================================================================
STEP 5: ACCESS THE GALLERY
================================================================================

1. Log in to the application: http://localhost:8000/login/
2. From the main dashboard, look for "Photo Gallery" in the left sidebar
3. Click on it to access the gallery
4. Click "Upload Photos" to start uploading

================================================================================
STEP 6: VERIFY INSTALLATION
================================================================================

Check that everything is working:

□ Sidebar shows "Photo Gallery" menu
□ Gallery page loads with responsive grid
□ Upload button opens modal dialog
□ Filter dropdowns show locations/projects
□ Drag-and-drop area is visible in upload modal
□ File list updates when you select files
□ Upload button submits files
□ Photos appear in grid after upload
□ Most recent photos appear first
□ Filters work correctly
□ If you're a superuser, delete button appears on hover

================================================================================
ACCESSING THE ADMIN INTERFACE
================================================================================

Admin panel: http://localhost:8000/admin/

In the admin panel, you can:
- View all uploaded photos
- Search photos by caption or uploader
- Filter photos by date, location, project, or uploader
- View image preview
- Add/edit/delete locations and projects
- Delete photos

Admin Actions:
- Select photos and delete (bulk delete)
- Search by caption text
- Advanced filtering

================================================================================
COMMON COMMANDS
================================================================================

View all gallery photos:
    python manage.py shell
    >>> from site_gallery.models import Photo
    >>> Photo.objects.all()

Get photo count:
    >>> Photo.objects.count()

Clear all photos:
    >>> Photo.objects.all().delete()

Create a location:
    >>> from site_gallery.models import Location
    >>> Location.objects.create(name="My Office")

Create a project:
    >>> from site_gallery.models import Project
    >>> Project.objects.create(name="My Project")

View all locations:
    >>> Location.objects.all()

View all projects:
    >>> Project.objects.all()

================================================================================
SETTINGS CONFIGURATION
================================================================================

The gallery works with default settings, but you can customize:

MEDIA_ROOT (default: BASE_DIR / "media/")
MEDIA_URL (default: "/media/")

For S3 storage, add to settings.py:
    GALLERY_STORAGE_BACKEND = 'site_gallery.storage.S3GalleryStorage'
    AWS_ACCESS_KEY_ID = 'your-key'
    AWS_SECRET_ACCESS_KEY = 'your-secret'
    AWS_STORAGE_BUCKET_NAME = 'your-bucket'

For custom storage:
    GALLERY_STORAGE_BACKEND = 'path.to.CustomStorageClass'

================================================================================
TESTING
================================================================================

Run all tests:
    python manage.py test site_gallery

Run specific test class:
    python manage.py test site_gallery.tests.SiteGalleryModelTests

Run with coverage:
    pip install coverage
    coverage run --source='site_gallery' manage.py test site_gallery
    coverage report
    coverage html  # Creates htmlcov/index.html

================================================================================
TROUBLESHOOTING
================================================================================

Issue: Photos not showing after upload
Solution:
    1. Check that MEDIA_ROOT directory exists: ls -la media/
    2. Check permissions: chmod 755 media/
    3. Verify media serving is enabled in urls.py
    4. Check browser console for errors (F12)

Issue: Upload fails with "Max 20 photos"
Solution:
    This is by design. Select fewer than 20 photos or upload in multiple batches.

Issue: Can't delete photo (no delete button)
Solution:
    Only admin/staff users can delete. In admin panel (/admin/):
    1. Go to Users
    2. Edit your user
    3. Check "Staff status"
    4. Save and reload gallery page

Issue: Gallery sidebar menu not showing
Solution:
    1. Restart Django server
    2. Clear browser cache (Ctrl+Shift+Delete)
    3. Check that "site_gallery" is in INSTALLED_APPS
    4. Check that "site_gallery" is in SIDEBARS

Issue: Image upload validation error
Solution:
    1. Ensure Pillow is installed: pip install Pillow
    2. Try with a different image format (JPEG, PNG)
    3. Check file is actually an image (not renamed text file)
    4. Restart Django server

Issue: S3 upload fails
Solution:
    1. Install required packages: pip install django-storages boto3
    2. Verify AWS credentials are correct
    3. Check bucket exists and has correct permissions
    4. Check Django logs for specific error message

================================================================================
FILE LOCATIONS
================================================================================

Gallery app: d:\Work Files\Workspace\Project 6 (Emp Portal)\site_gallery\

Key files:
- Views: site_gallery/views.py
- Models: site_gallery/models.py
- URLs: site_gallery/urls.py
- Templates: site_gallery/templates/site_gallery/
- Static: site_gallery/static/site_gallery/
- Admin: site_gallery/admin.py
- Tests: site_gallery/tests.py

Media directory: d:\Work Files\Workspace\Project 6 (Emp Portal)\media\

Uploaded photos: media/gallery/%Y/%m/%d/

================================================================================
IMPORTANT NOTES
================================================================================

1. First-time Setup
   - Run makemigrations and migrate
   - Create a superuser account
   - Log in and verify everything works

2. File Permissions
   - Ensure media directory is writable by Django process
   - Use proper file permissions (755 for dirs, 644 for files)

3. Database
   - Migrations must be run before using the app
   - Database changes are handled automatically by Django

4. Static Files
   - Run collectstatic in production
   - Static files are for development in debug mode

5. Media Files
   - Photos are stored in media/gallery/ with subdirectories
   - Original quality is preserved
   - Consider CDN in production

6. Security
   - Only authenticated users can access gallery
   - Only staff users can delete photos
   - All permissions checked server-side
   - CSRF protection enabled

================================================================================
NEXT STEPS
================================================================================

After successful installation:

1. Explore the gallery features:
   - Upload some photos
   - Create locations and projects
   - Test filtering
   - Test delete (if admin user)

2. Customize styling:
   - Edit site_gallery/static/site_gallery/css/gallery.css
   - Update gallery_list.html template as needed

3. Configure storage backend:
   - Read INSTALLATION_GUIDE.md for S3 setup
   - Implement custom storage if needed

4. Add to your workflow:
   - Train users on the new gallery feature
   - Set up proper backup strategy
   - Monitor usage and disk space

5. Extend functionality:
   - Add more metadata fields
   - Implement image cropping
   - Add photo comments/ratings
   - Create analytics dashboard

================================================================================
GETTING HELP
================================================================================

Documentation:
- README.md: Feature overview
- INSTALLATION_GUIDE.md: Detailed setup guide
- IMPLEMENTATION_SUMMARY.md: Technical details

Code:
- See tests.py for usage examples
- Check views.py for API endpoints
- Review models.py for database structure

Resources:
- Horilla documentation: https://horilla.readthedocs.io/
- Django documentation: https://docs.djangoproject.com/
- Pillow documentation: https://pillow.readthedocs.io/

================================================================================
END OF QUICK START GUIDE
================================================================================
"""
