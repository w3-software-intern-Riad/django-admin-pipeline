# polls/management/commands/import_data.py

import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from polls.models import HotelInformation, Location, Images
import psycopg
from colorama import Style, init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from django.conf import settings


# Initialize Colorama
init(autoreset=True)

# Define custom style dictionary
custom_style = Style.from_dict({
    'prompt': 'fg:#00ff00 bold',  # Cyan text, bold
})


class Command(BaseCommand):
    help = 'Import data from another database into HotelInformation'

    def add_arguments(self, parser):
        # parser.add_argument('--source-db', type=str, help='Source database connection string')
        # parser.add_argument('--username', type=str, help='Admin username')
        # parser.add_argument('--password', type=str, help='Admin password')
        # parser.add_argument('--scrapy-images-dir', type=str, help='Directory path of the images in Scrapy project')
        pass

    def handle(self, *args, **kwargs):

        print("\n\x1b[36m\x1b[1m=== Admin Login ===\x1b[0m\n")
        username = prompt('Admin username: ', style=custom_style)
        password = prompt('Admin password: ',
                          style=custom_style, is_password=True)
        if not username or not password:
            self.stdout.write(self.style.ERROR(
                'Please provide all required arguments:  admin credentials'))
        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user or not user.is_superuser:
            self.stdout.write(self.style.ERROR(
                'Authentication failed or user is not an admin.'))
            return
        else:
            print("\x1b[36m\x1b[1m=== Admin is authenticated ===\x1b[0m\n")
        # Print a styled title

        print("\x1b[36m\x1b[1m=== Import Data Command ===\x1b[0m\n")

        # Prompt user for database connection details
        dbname = prompt('Database name (scrapy database): ',
                        style=custom_style)
        dbuser = prompt('Database username: ', style=custom_style)
        dbpassword = prompt('Database password: ',
                            style=custom_style, is_password=True)
        dbhost = prompt('Database host (e.g., localhost): ',
                        style=custom_style)
        dbport = prompt('Database port (e.g., 5432): ', style=custom_style)
        scrapy_images_dir = prompt(
            'Directory path of the images in Scrapy project: ', style=custom_style)

        # Check for missing fields
        if not dbname or not dbuser or not dbpassword or not dbhost or not dbport:
            self.stdout.write(self.style.ERROR(
                'Error: All database connection fields must be provided.'))
            return
        source_db = f"dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}"

        if not source_db or not scrapy_images_dir:
            self.stdout.write(self.style.ERROR(
                'Please provide all required arguments: source database,Scrapy images directory.'))
            return

        # Connect to the source database
        try:
            conn = psycopg.connect(source_db)
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to connect to the source database: {e}'))
            return
        cursor = conn.cursor()

        # Execute SQL query and handle errors
        try:
            cursor.execute('''
                SELECT "propertyTitle", latitude, longitude, location, rating, price, "roomType", images
                FROM public.hotels
            ''')
            rows = cursor.fetchall()
        except psycopg.Error as e:
            self.stdout.write(self.style.ERROR(
                f'Error executing SQL query: {e}'))
            return

         # Ensure the images/ directory exists
        django_images_dir = os.path.join(settings.MEDIA_ROOT, 'images/')
        try:
            if not os.path.exists(django_images_dir):
                os.makedirs(django_images_dir)
        except OSError as e:
            self.stdout.write(self.style.ERROR(
                f'Error creating directory {django_images_dir}: {e}'))
            return

        # Process and insert data into the HotelInformation model
        for row in rows:
            if len(row) < 8:
                self.stdout.write(self.style.ERROR(
                    'Error: Database schema is incorrect or incomplete. Some fields are missing.'))
                continue

            propertyTitle, latitude, longitude, location, rating, price, roomType, images = row

            # Check for missing field values
            if not all([propertyTitle, latitude, longitude, location, rating, price, roomType, images]):
                self.stdout.write(self.style.ERROR(
                    'Error: One or more fields are missing in the row.'))
                continue

            try:
                hotel = HotelInformation.objects.create(
                    title=propertyTitle,

                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error creating HotelInformation record: {e}'))
                continue

            # Create the Location record
            try:

                location_obj, created = Location.objects.get_or_create(
                    name=location,
                    latitude=latitude,
                    longitude=longitude,

                )
            # Add the location to the hotel's locations many-to-many field
                hotel.locations.add(location_obj)

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error creating Location record: {e}'))
                continue

            # Create the Images records
            processed_images = set()  # To keep track of processed images

            for image_name in images:  # Assuming 'images' is a comma-separated string of image filenames

                if image_name in processed_images:
                    self.stdout.write(self.style.WARNING(
                        f'Image {image_name} already processed, skipping.'))
                    continue

                image_path = os.path.join(scrapy_images_dir, image_name)
                if os.path.isfile(image_path):
                    try:
                        destination_path = os.path.join(
                            django_images_dir, image_name)

                        # Check if the image already exists for this hotel
                        if Images.objects.filter(hotel=hotel, image=destination_path).exists():
                            self.stdout.write(self.style.WARNING(
                                f'Image {destination_path} already exists for this hotel, skipping.'))
                            continue

                        # Copy the file to Django's images directory
                        shutil.copy2(image_path, destination_path)

                        # Save the image record in the database
                        Images.objects.create(
                            hotel=hotel,
                            image=f'images/{image_name}'
                        )

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully copied and saved {image_name}'))
                        processed_images.add(destination_path)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'Error processing {image_name}: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'{image_name} is not a file, skipping.'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully imported data into HotelInformation and copied images.'))
