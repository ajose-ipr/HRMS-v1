"""
Management command to create demo gallery data for testing
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from site_gallery.models import Location, Project, Photo


class Command(BaseCommand):
    """Create demo gallery data"""

    help = "Create demo gallery data with sample photos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of demo photos to create (default: 10)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing gallery data before creating demo data",
        )

    def handle(self, *args, **options):
        """Execute the command"""
        if options["clear"]:
            self.stdout.write("Clearing existing gallery data...")
            Photo.objects.all().delete()
            Location.objects.all().delete()
            Project.objects.all().delete()

        # Create locations
        locations_data = [
            "Office - Main Floor",
            "Conference Room A",
            "Break Room",
            "Outdoor - Parking Lot",
            "Cafeteria",
        ]
        locations = []
        for loc_name in locations_data:
            location, created = Location.objects.get_or_create(name=loc_name)
            locations.append(location)
            if created:
                self.stdout.write(f"Created location: {loc_name}")

        # Create projects
        projects_data = [
            "Website Redesign",
            "Mobile App",
            "Backend API",
            "Team Event",
            "Office Setup",
        ]
        projects = []
        for proj_name in projects_data:
            project, created = Project.objects.get_or_create(name=proj_name)
            projects.append(project)
            if created:
                self.stdout.write(f"Created project: {proj_name}")

        # Get or create demo user
        demo_user, created = User.objects.get_or_create(
            username="demo_uploader",
            defaults={
                "email": "demo@horilla.com",
                "first_name": "Demo",
                "last_name": "User",
            },
        )
        if created:
            self.stdout.write("Created demo user: demo_uploader")

        # Create demo photos
        colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Purple
            (0, 128, 128),  # Teal
            (128, 128, 0),  # Olive
        ]

        captions = [
            "Beautiful office space",
            "Team collaboration moment",
            "Great view from the window",
            "Conference room setup",
            "Team lunch celebration",
            "Project milestone reached",
            "Outdoor team activity",
            "Morning coffee break",
            "Meeting in progress",
            "Happy team at work",
        ]

        count = options["count"]
        for i in range(count):
            # Generate a simple colored image
            color = colors[i % len(colors)]
            image = Image.new("RGB", (800, 600), color=color)

            # Save to bytes
            image_bytes = BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)

            # Create uploaded file
            uploaded_file = InMemoryUploadedFile(
                image_bytes,
                "ImageField",
                f"demo_photo_{i}.jpg",
                "image/jpeg",
                image_bytes.getbuffer().nbytes,
                None,
            )

            # Create photo
            photo = Photo.objects.create(
                image=uploaded_file,
                uploader=demo_user,
                location=locations[i % len(locations)],
                project=projects[i % len(projects)],
                caption=captions[i % len(captions)],
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created photo {i + 1}/{count}: {photo.caption}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {count} demo photos!"
            )
        )
        self.stdout.write("Access the gallery at: http://localhost:8000/gallery/")
