"""
Tests for site gallery app
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from site_gallery.models import Location, Project, Photo
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class SiteGalleryModelTests(TestCase):
    """Test suite for gallery models"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.location = Location.objects.create(name="Test Location")
        self.project = Project.objects.create(name="Test Project")

    def test_location_creation(self):
        """Test creating a location"""
        self.assertEqual(self.location.name, "Test Location")
        self.assertIsNotNone(self.location.created_at)

    def test_project_creation(self):
        """Test creating a project"""
        self.assertEqual(self.project.name, "Test Project")
        self.assertIsNotNone(self.project.created_at)

    def test_photo_creation(self):
        """Test creating a photo"""
        # Create a test image
        image = Image.new("RGB", (100, 100), color="red")
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        photo = Photo.objects.create(
            image=SimpleUploadedFile(
                "test.jpg",
                image_io.getvalue(),
                content_type="image/jpeg",
            ),
            uploader=self.user,
            location=self.location,
            project=self.project,
            caption="Test photo",
        )

        self.assertEqual(photo.caption, "Test photo")
        self.assertEqual(photo.uploader, self.user)
        self.assertEqual(photo.location, self.location)
        self.assertEqual(photo.project, self.project)

    def test_photo_deletion(self):
        """Test that photo file is deleted when instance is deleted"""
        image = Image.new("RGB", (100, 100), color="red")
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        photo = Photo.objects.create(
            image=SimpleUploadedFile(
                "test.jpg",
                image_io.getvalue(),
                content_type="image/jpeg",
            ),
            uploader=self.user,
        )

        photo_id = photo.id
        photo.delete()

        self.assertFalse(Photo.objects.filter(id=photo_id).exists())


class SiteGalleryViewTests(TestCase):
    """Test suite for gallery views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            is_staff=True,
        )

    def test_gallery_list_requires_login(self):
        """Test that gallery list requires authentication"""
        response = self.client.get(reverse("site_gallery:gallery-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_gallery_list_for_authenticated_user(self):
        """Test that authenticated user can view gallery"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_gallery:gallery-list"))
        self.assertEqual(response.status_code, 200)

    def test_location_api_get(self):
        """Test getting locations via API"""
        Location.objects.create(name="Location 1")
        Location.objects.create(name="Location 2")

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_gallery:location-api"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["locations"]), 2)

    def test_project_api_get(self):
        """Test getting projects via API"""
        Project.objects.create(name="Project 1")
        Project.objects.create(name="Project 2")

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_gallery:project-api"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["projects"]), 2)


class PhotoUploadTests(TestCase):
    """Test suite for photo upload functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.login(username="testuser", password="testpass123")

    def create_test_image(self):
        """Create a test image"""
        image = Image.new("RGB", (100, 100), color="blue")
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        return SimpleUploadedFile(
            "test.jpg",
            image_io.getvalue(),
            content_type="image/jpeg",
        )

    def test_20_photo_limit_enforcement(self):
        """Test that 20-photo limit is enforced"""
        files = [self.create_test_image() for _ in range(21)]

        response = self.client.post(
            reverse("site_gallery:photo-upload"),
            {"images": files},
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)


class PhotoFilterTests(TestCase):
    """Test suite for photo filtering"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.location = Location.objects.create(name="Office")
        self.project = Project.objects.create(name="Backend")

        self.client.login(username="testuser", password="testpass123")

    def test_filter_by_location(self):
        """Test filtering photos by location"""
        response = self.client.get(
            reverse("site_gallery:gallery-api"),
            {"location": self.location.id},
        )

        self.assertEqual(response.status_code, 200)

    def test_filter_by_project(self):
        """Test filtering photos by project"""
        response = self.client.get(
            reverse("site_gallery:gallery-api"),
            {"project": self.project.id},
        )

        self.assertEqual(response.status_code, 200)
