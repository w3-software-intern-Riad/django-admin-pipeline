# polls/management/commands/import_data.py

import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from polls.models import HotelInformation, Location, Images
import psycopg
from django.core.files import File
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Import data from another database into HotelInformation'

    def add_arguments(self, parser):
        parser.add_argument('--source-db', type=str, help='Source database connection string')
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--scrapy-images-dir', type=str, help='Directory path of the images in Scrapy project')

    def handle(self, *args, **kwargs):
        source_db = kwargs['source_db']
        username = kwargs['username']
        password = kwargs['password']
        scrapy_images_dir = kwargs['scrapy_images_dir']

        if not source_db or not username or not password or not scrapy_images_dir:
            self.stdout.write(self.style.ERROR('Please provide all required arguments: source database, admin credentials, and Scrapy images directory.'))
            return

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user or not user.is_superuser:
            self.stdout.write(self.style.ERROR('Authentication failed or user is not an admin.'))
            return

        # Connect to the source database
        conn = psycopg.connect(source_db)
        cursor = conn.cursor()

        # Fetch data from the source database
        cursor.execute('''
            SELECT "propertyTitle", latitude, longitude, location, rating, price, "roomType", images
            FROM public.hotels
        ''')
        rows = cursor.fetchall()

        # Ensure the images/ directory exists
        django_images_dir = 'images/'
        if not os.path.exists(django_images_dir):
            os.makedirs(django_images_dir)

        # Process and insert data into the HotelInformation model
        for row in rows:
            propertyTitle, latitude, longitude, location, rating, price, roomType, images = row

            # Create the HotelInformation record
            hotel = HotelInformation.objects.create(
                title=propertyTitle,
                rating=rating,
                price=price,
                roomType=roomType
            )

            # Create the Location record
            Location.objects.create(
                name=location,
                latitude=latitude,
                longitude=longitude,
                hotel=hotel  # Set the foreign key
            )

            # Create the Images records
            for image_name in images:
                image_path = os.path.join(scrapy_images_dir, image_name)
                if os.path.exists(image_path):
                    # Use Django's file storage to save the image
                    with open(image_path, 'rb') as img_file:
                        django_image_path = default_storage.save(f'images/{image_name}', File(img_file))

                        # Save the image in the database
                        Images.objects.create(
                            image=django_image_path,  # Save the relative path to the image
                            hotel=hotel  # Set the foreign key
                        )
                else:
                    self.stdout.write(self.style.WARNING(f'Image {image_name} not found in Scrapy images directory.'))

        self.stdout.write(self.style.SUCCESS('Successfully imported data into HotelInformation and copied images.'))
