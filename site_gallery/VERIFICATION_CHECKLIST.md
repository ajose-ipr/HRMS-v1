"""
SITE GALLERY - FINAL VERIFICATION CHECKLIST

Use this checklist to verify that the Site Gallery feature is properly installed
and configured in your Horilla HRMS instance.

================================================================================
PRE-INSTALLATION CHECKS
================================================================================

□ Django version is 4.1 or higher
  Verify: python manage.py --version

□ Pillow is installed
  Verify: python -c "import PIL; print(PIL.__version__)"

□ PostgreSQL or other database is running
  Verify: python manage.py dbshell (should not error)

□ Project structure is intact
  Verify: ls site_gallery/ (should show app files)

================================================================================
INSTALLATION VERIFICATION
================================================================================

□ site_gallery in INSTALLED_APPS
  Location: horilla/horilla_apps.py
  Check: grep "site_gallery" horilla/horilla_apps.py | grep INSTALLED_APPS

□ site_gallery in SIDEBARS
  Location: horilla/horilla_apps.py
  Check: grep "site_gallery" horilla/horilla_apps.py | grep SIDEBARS

□ site_gallery URLs included in main urls.py
  Location: horilla/urls.py
  Check: grep "site_gallery" horilla/urls.py

□ Media URL routing enabled
  Location: horilla/urls.py
  Check: grep "MEDIA_URL" horilla/urls.py (should not be commented)

□ All required files exist
  Verify each file:
    ✓ site_gallery/__init__.py
    ✓ site_gallery/apps.py
    ✓ site_gallery/models.py
    ✓ site_gallery/views.py
    ✓ site_gallery/forms.py
    ✓ site_gallery/urls.py
    ✓ site_gallery/admin.py
    ✓ site_gallery/storage.py
    ✓ site_gallery/sidebar.py
    ✓ site_gallery/signals.py
    ✓ site_gallery/context_processors.py
    ✓ site_gallery/decorators.py
    ✓ site_gallery/filters.py
    ✓ site_gallery/tests.py
    ✓ site_gallery/admin.py
    ✓ migrations/__init__.py
    ✓ templates/site_gallery/gallery_list.html
    ✓ templates/site_gallery/upload_modal.html
    ✓ static/site_gallery/css/gallery.css
    ✓ static/site_gallery/js/gallery.js
    ✓ management/commands/create_gallery_demo_data.py

================================================================================
MIGRATION VERIFICATION
================================================================================

□ Migrations created
  Command: python manage.py makemigrations site_gallery
  Should create: site_gallery/migrations/0001_initial.py

□ Migrations applied
  Command: python manage.py migrate site_gallery
  Should output: Applying site_gallery.0001_initial... OK

□ Database tables created
  Verify: python manage.py dbshell
    \dt site_gallery_*
    Should show:
    - site_gallery_location
    - site_gallery_project
    - site_gallery_photo

□ Migrations folder structure correct
  Check:
    ✓ site_gallery/migrations/__init__.py exists
    ✓ site_gallery/migrations/0001_initial.py exists

================================================================================
DATABASE VERIFICATION
================================================================================

□ Location table created
  Check: python manage.py dbshell
    SELECT * FROM site_gallery_location;

□ Project table created
  Check: python manage.py dbshell
    SELECT * FROM site_gallery_project;

□ Photo table created
  Check: python manage.py dbshell
    SELECT * FROM site_gallery_photo;

□ Foreign key relationships intact
  Check tables have proper foreign keys to User and each other

□ Database indexes created
  Check: SHOW INDEXES FROM site_gallery_photo;

================================================================================
RUNTIME VERIFICATION
================================================================================

□ Django server starts without errors
  Command: python manage.py runserver
  Expected: "Starting development server at http://127.0.0.1:8000/"

□ No migration errors on startup
  Expected: No errors in "Applying site_gallery" when server starts

□ App loads in Django shell
  Command: python manage.py shell
    >>> from site_gallery.models import Photo, Location, Project
    >>> # Should not raise ImportError

□ Signals are registered
  Command: python manage.py shell
    >>> from django.dispatch import Signal
    >>> from site_gallery import signals
    >>> # Should not raise ImportError

================================================================================
USER INTERFACE VERIFICATION
================================================================================

□ Admin interface accessible
  URL: http://localhost:8000/admin/
  Should show:
    ✓ Site Gallery section
    ✓ Locations link
    ✓ Projects link
    ✓ Photos link

□ Gallery sidebar menu visible
  1. Log in to the application
  2. Check left sidebar
  3. Should see "Photo Gallery" menu item
  4. Should have "Gallery" submenu

□ Gallery page loads
  URL: http://localhost:8000/gallery/
  Should show:
    ✓ Empty gallery message or existing photos
    ✓ Upload Photos button
    ✓ Filter section
    ✓ Photo grid (if photos exist)

□ Upload modal opens
  1. Click "Upload Photos" button
  2. Modal should appear with:
    ✓ Location field
    ✓ Project field
    ✓ Caption field
    ✓ Drag-and-drop area
    ✓ Upload and Cancel buttons

================================================================================
FUNCTIONALITY VERIFICATION
================================================================================

□ File upload works
  1. Select an image file
  2. Click Upload
  3. Photo should appear in gallery

□ Metadata saves correctly
  1. Upload photo with location, project, caption
  2. Check /admin/site_gallery/photo/
  3. Photo should have all metadata

□ Location creation works
  1. Enter new location name in upload modal
  2. Upload a photo
  3. Check admin - new location should exist

□ Project creation works
  1. Enter new project name in upload modal
  2. Upload a photo
  3. Check admin - new project should exist

□ 20-photo limit enforced
  1. Try to select 21+ photos
  2. Should see error: "Maximum 20 photos per upload allowed"

□ Filtering works
  1. Upload photos with different locations/projects
  2. Use location filter - should show only photos with that location
  3. Use project filter - should show only photos with that project
  4. Use uploader filter - should show only photos by that user

□ Chronological ordering works
  1. Upload multiple photos with different times
  2. Newest photo should appear first

□ Responsive design works
  1. View gallery on desktop - should show 4 columns
  2. View gallery on tablet - should show 2-3 columns
  3. View gallery on mobile - should show 1 column

□ Admin delete works (if staff user)
  1. Log in as staff user
  2. Hover over photo in gallery
  3. Delete button should appear
  4. Click delete and confirm
  5. Photo should be removed

□ Non-admin cannot delete
  1. Log in as regular user
  2. Hover over photo - delete button should NOT appear
  3. Navigate directly to delete URL - should get 403 Forbidden

================================================================================
ADMIN INTERFACE VERIFICATION
================================================================================

□ Photo admin page loads
  URL: http://localhost:8000/admin/site_gallery/photo/
  Should show:
    ✓ List of all photos
    ✓ Search by caption/uploader
    ✓ Filters by date/location/project/uploader
    ✓ Image preview
    ✓ Delete action

□ Location admin page loads
  URL: http://localhost:8000/admin/site_gallery/location/
  Should show:
    ✓ List of all locations
    ✓ Add/Edit/Delete options

□ Project admin page loads
  URL: http://localhost:8000/admin/site_gallery/project/
  Should show:
    ✓ List of all projects
    ✓ Add/Edit/Delete options

================================================================================
API VERIFICATION
================================================================================

□ Gallery API endpoint works
  URL: http://localhost:8000/gallery/api/
  Should return JSON with photos array

□ Locations API endpoint works
  URL: http://localhost:8000/api/locations/
  Should return JSON with locations array

□ Projects API endpoint works
  URL: http://localhost:8000/api/projects/
  Should return JSON with projects array

□ Filter parameters work
  URL: http://localhost:8000/gallery/api/?location=1&project=1
  Should return filtered photos

================================================================================
PERMISSION VERIFICATION
================================================================================

□ Anonymous user cannot access gallery
  1. Log out
  2. Visit http://localhost:8000/gallery/
  3. Should redirect to login page

□ Regular user can view gallery
  1. Log in as regular user
  2. Visit http://localhost:8000/gallery/
  3. Should see gallery page

□ Regular user can upload
  1. Log in as regular user
  2. Use upload modal
  3. Upload should succeed

□ Regular user cannot delete
  1. Log in as regular user
  2. Hover over photo - no delete button
  3. Try to access delete API - should get 403

□ Staff user can delete
  1. Log in as staff user
  2. Hover over photo - delete button appears
  3. Delete should succeed

================================================================================
STATIC FILES VERIFICATION
================================================================================

□ CSS file exists and is referenced
  File: site_gallery/static/site_gallery/css/gallery.css
  Check: grep -r "gallery.css" templates/

□ JavaScript file exists and is referenced
  File: site_gallery/static/site_gallery/js/gallery.js
  Check: grep -r "gallery.js" templates/

□ CSS loads without 404 errors
  1. Load gallery page
  2. Check browser DevTools Network tab
  3. gallery.css should load successfully

□ JavaScript loads without 404 errors
  1. Load gallery page
  2. Check browser DevTools Network tab
  3. gallery.js should load successfully

□ Styles apply correctly
  1. Load gallery page
  2. Check that grid layout has proper spacing
  3. Check that buttons are styled
  4. Check that responsive breakpoints work

================================================================================
MEDIA STORAGE VERIFICATION
================================================================================

□ Media directory exists
  Verify: ls -la media/
  Should exist and be writable

□ Gallery subdirectory created
  Verify: ls -la media/gallery/
  May be empty initially

□ Uploaded photos stored correctly
  1. Upload a photo
  2. Check: ls -la media/gallery/
  3. Should have date-based subdirectories

□ File permissions are correct
  Check: ls -la media/gallery/
  Should have 755 for directories, 644 for files

□ MEDIA_URL configured correctly
  Check settings.py for MEDIA_URL = "/media/"

□ Media files are accessible
  1. Check browser console - no 404s for images
  2. Images should display properly in gallery

================================================================================
TESTING VERIFICATION
================================================================================

□ Tests exist and run
  Command: python manage.py test site_gallery
  Should run without errors

□ Test suite passes
  Expected: OK (at minimum)
  All test cases should pass

□ Model tests pass
  Command: python manage.py test site_gallery.tests.SiteGalleryModelTests

□ View tests pass
  Command: python manage.py test site_gallery.tests.SiteGalleryViewTests

□ Upload tests pass
  Command: python manage.py test site_gallery.tests.PhotoUploadTests

□ Filter tests pass
  Command: python manage.py test site_gallery.tests.PhotoFilterTests

================================================================================
DEMO DATA VERIFICATION (OPTIONAL)
================================================================================

□ Create demo data command works
  Command: python manage.py create_gallery_demo_data --count=5
  Should create sample photos, locations, and projects

□ Demo photos display in gallery
  Visit: http://localhost:8000/gallery/
  Should see colored demo photos

□ Demo locations available
  Check filter dropdown - should show demo locations

□ Demo projects available
  Check filter dropdown - should show demo projects

================================================================================
PERFORMANCE VERIFICATION
================================================================================

□ Page load time is acceptable
  Gallery page should load in < 1 second
  Check with DevTools Network tab

□ Image loading is responsive
  1. Upload a large image (2-3 MB)
  2. Should upload successfully
  3. Thumbnail should load quickly

□ Filtering is responsive
  1. Change filters
  2. Results should update quickly
  3. No significant lag

□ Database queries are reasonable
  Use Django Debug Toolbar to check:
  - Gallery page: < 10 queries
  - Upload: < 15 queries
  - Delete: < 5 queries

================================================================================
DOCUMENTATION VERIFICATION
================================================================================

□ README.md exists and is complete
  File: site_gallery/README.md
  Should contain feature overview and configuration

□ INSTALLATION_GUIDE.md exists
  File: site_gallery/INSTALLATION_GUIDE.md
  Should contain step-by-step setup instructions

□ QUICKSTART.md exists
  File: site_gallery/QUICKSTART.md
  Should contain quick start guide

□ IMPLEMENTATION_SUMMARY.md exists
  File: site_gallery/IMPLEMENTATION_SUMMARY.md
  Should contain technical implementation details

================================================================================
FINAL CHECKLIST
================================================================================

□ All files created and verified
□ All migrations run successfully
□ Database tables created
□ Admin interface working
□ Gallery page accessible
□ Upload functionality working
□ Filtering working
□ Delete working (for admins)
□ Responsive design working
□ Static files loading
□ Media files storing correctly
□ Tests passing
□ Documentation complete

================================================================================
SIGN-OFF
================================================================================

Date Completed: _______________
Verified By: _______________
Environment: Development / Staging / Production (circle one)
Status: ✓ READY FOR USE

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

================================================================================
TROUBLESHOOTING
================================================================================

If any checkbox fails, review the corresponding section in:
- QUICKSTART.md
- INSTALLATION_GUIDE.md
- IMPLEMENTATION_SUMMARY.md

Or check the specific file:
- models.py - for database issues
- views.py - for API/logic issues
- gallery_list.html - for UI issues
- gallery.css - for styling issues
- storage.py - for file storage issues

================================================================================
END OF VERIFICATION CHECKLIST
================================================================================
"""
