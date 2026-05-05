"""
Site Gallery App Documentation

A comprehensive photo gallery feature for Horilla HRMS with the following capabilities:

## Features

### Access & Permissions
- Any logged-in user can upload and view all photos
- Only admins can delete photos

### Gallery Display
- Photo grid layout (responsive, automatically adjusts to screen size)
- Sorted chronologically (newest first)
- Filter bar with dropdowns for: Location, Project, and Uploader
- Hover effects and smooth animations

### Upload
- Bulk upload supported (max 20 photos per upload)
- Works on both mobile and desktop browsers
- Drag-and-drop + file picker UI in an upload modal
- 20-photo limit enforced on the client side

### Metadata (captured per photo)
- Uploader: auto-filled from logged-in user
- Date of upload: auto-filled with server time
- Location tag: dropdown of existing locations; user can type and create new on the fly
- Project: same behaviour as location
- Caption / description: optional free text

### Storage
- Local file storage using Django's MEDIA_ROOT / MEDIA_URL
- Abstracted behind a storage backend class for easy swapping to S3 or cloud providers
- See storage.py for configuration

### Moderation
- Admins can delete any photo
- Delete button only visible to admin users

## Installation & Setup

### 1. App is already created in: `site_gallery/`

### 2. Models are defined in `site_gallery/models.py`:
   - Location: stores location tags
   - Project: stores project tags
   - Photo: stores photo metadata and file reference

### 3. Storage backend in `site_gallery/storage.py`:
   - LocalGalleryStorage: Uses local file system (default)
   - S3GalleryStorage: For AWS S3 (requires django-storages + boto3)
   - Pluggable design for custom backends

### 4. Views & URLs:
   - GET /gallery/: List all photos with filter support
   - POST /gallery/upload/: Bulk upload with metadata
   - DELETE /gallery/<id>/: Admin-only delete
   - GET/POST /gallery/api/locations/: Fetch list or create new location
   - GET/POST /gallery/api/projects/: Fetch list or create new project

### 5. Permissions:
   - Uses Django's authentication and permission system
   - is_authenticated for upload/view
   - is_staff for delete

### 6. Template:
   - Main gallery view: site_gallery/templates/site_gallery/gallery_list.html
   - Upload modal: site_gallery/templates/site_gallery/upload_modal.html
   - CSS: site_gallery/static/site_gallery/css/gallery.css

### 7. Sidebar integration:
   - Configured in site_gallery/sidebar.py
   - Visible to all authenticated users
   - Appears as "Photo Gallery" in main sidebar

## Configuration

### Storage Backend Configuration

**Using Local Storage (default):**
No additional configuration needed. Photos are stored in `MEDIA_ROOT/gallery/`

**Using AWS S3:**
```python
# In settings.py or .env
GALLERY_STORAGE_BACKEND = 'site_gallery.storage.S3GalleryStorage'

# Also configure AWS settings:
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
```

**Using Custom Backend:**
Create a custom backend class inheriting from GalleryStorageBackend and configure it:
```python
GALLERY_STORAGE_BACKEND = 'myapp.storage.MyCustomStorage'
```

## Running Migrations

```bash
python manage.py makemigrations site_gallery
python manage.py migrate site_gallery
```

## Running Tests

```bash
python manage.py test site_gallery
```

## Database Schema

### Location Model
- id: BigAutoField (Primary Key)
- name: CharField (max_length=100, unique=True)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)

### Project Model
- id: BigAutoField (Primary Key)
- name: CharField (max_length=100, unique=True)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)

### Photo Model
- id: BigAutoField (Primary Key)
- image: ImageField (uploads to gallery/%Y/%m/%d/)
- uploader: ForeignKey(User, on_delete=CASCADE)
- upload_date: DateTimeField (auto_now_add=True)
- location: ForeignKey(Location, on_delete=SET_NULL, null=True, blank=True)
- project: ForeignKey(Project, on_delete=SET_NULL, null=True, blank=True)
- caption: TextField (blank=True, default="")

## API Endpoints

### Gallery List
- **URL**: `/gallery/`
- **Method**: GET
- **Auth**: Required (login_required)
- **Returns**: HTML page with photo gallery

### Photo Upload
- **URL**: `/gallery/upload/`
- **Method**: POST
- **Auth**: Required
- **Accepts**: Multipart form data with images, location_name, project_name, caption
- **Returns**: JSON with uploaded photos and any errors

### Photo Delete
- **URL**: `/gallery/<id>/delete/`
- **Method**: DELETE
- **Auth**: Required (is_staff)
- **Returns**: JSON success/error response

### Location API
- **URL**: `/api/locations/`
- **Method**: GET/POST
- **Auth**: Required
- **GET Returns**: List of all locations
- **POST Creates**: New location

### Project API
- **URL**: `/api/projects/`
- **Method**: GET/POST
- **Auth**: Required
- **GET Returns**: List of all projects
- **POST Creates**: New project

### Gallery API
- **URL**: `/gallery/api/`
- **Method**: GET
- **Auth**: Required
- **Query Parameters**: location, project, uploader
- **Returns**: JSON array of photos with metadata

## Frontend Features

### Responsive Grid Layout
- Auto-adjusts to 4 columns on desktop
- 2-3 columns on tablets
- 1-2 columns on mobile
- Smooth animations on hover

### File Upload
- Drag and drop support
- File picker fallback
- File validation (image files only)
- Real-time file list display
- 20-file limit with client-side validation

### Filtering
- Location dropdown
- Project dropdown
- Uploader text search
- Clear filters option

### Admin Features
- Delete button visible only to staff users
- Hover overlay on photos for admin-only delete action
- Confirmation dialog before deletion

## Troubleshooting

### Images not displaying
1. Check that MEDIA_ROOT and MEDIA_URL are correctly configured in settings.py
2. Ensure the media directory exists and is writable
3. Check that media URL routing is enabled in urls.py

### Upload fails
1. Ensure PIL/Pillow is installed: `pip install Pillow`
2. Check file permissions on media directory
3. Verify 20-photo limit is enforced client-side

### Sidebar not showing
1. Clear cache and restart Django development server
2. Ensure site_gallery is in INSTALLED_APPS
3. Ensure site_gallery is in SIDEBARS in horilla_apps.py

### S3 storage not working
1. Install required packages: `pip install django-storages boto3`
2. Configure AWS credentials in settings.py or environment variables
3. Restart Django server

## Admin Interface

Access the admin interface at `/admin/`:
- View, add, and delete photos
- Search photos by caption or uploader
- Filter by upload date, location, project, or uploader
- Image preview in admin
- Truncated caption display

## Development Notes

### Adding Custom Tags
To extend the gallery with custom tags beyond Location and Project:
1. Create a new model similar to Location/Project
2. Add a ForeignKey to Photo model
3. Create a new form field
4. Update the views to handle the new field
5. Update templates to display the new field

### Customizing Storage
To add a new storage backend:
1. Create a class inheriting from GalleryStorageBackend
2. Implement the get_storage() method
3. Set GALLERY_STORAGE_BACKEND in settings.py

### Extending Permissions
To restrict gallery access by company or department:
1. Override the gallery_accessibility function in sidebar.py
2. Add custom permission checks
3. Filter photos in views based on user's company/department
"""
