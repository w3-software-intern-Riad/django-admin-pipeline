# models.py
from django.db import models
from django.utils import timezone
import os

from django.conf import settings


class Amenities(models.Model):
    name = models.CharField(max_length=200)
    hotel = models.ForeignKey(
        'HotelInformation', 
        related_name='amenities', 
        on_delete=models.CASCADE,
        null=True
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updateDate = timezone.now()
        else:
            print("Creating a new instance of Amenities")

        super().save(*args, **kwargs)

class Location(models.Model):
    CITY = 'city'
    STATE = 'state'
    COUNTRY = 'country'

    LOCATION_TYPE_CHOICES = [
        (CITY, 'City'),
        (STATE, 'State'),
        (COUNTRY, 'Country'),
    ]

    name = models.CharField(max_length=400)
    type = models.CharField(
        max_length=10,
        choices=LOCATION_TYPE_CHOICES,
        default=CITY,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    hotel = models.ForeignKey(
        'HotelInformation', 
        related_name='locations', 
        on_delete=models.CASCADE,
        null=True
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updateDate = timezone.now()
        else:
            print("Creating a new instance of Location")    
        super().save(*args, **kwargs)

class HotelInformation(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=50000,null=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updateDate = timezone.now()
        else:
            print("Creating a new instance of HotelInformation")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated images from local storage
        for image in self.images.all():
            if image.image:
                # Get the full file path
                image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
                print("Image path : ",image_path)
                if os.path.isfile(image_path):
                    try:
                        os.remove(image_path)
                        print(f"Successfully deleted image: {image_path}")
                    except Exception as e:
                        print(f"Error deleting image {image_path}: {str(e)}")
                else:
                    print(f"No image found at {image_path}")
            else:
                print(f"No image file associated with image record {image.id}")

        # Call the superclass delete method
        super().delete(*args, **kwargs)
    
        

class Images(models.Model):
    image = models.ImageField(upload_to='images/', null=True)
    hotel = models.ForeignKey(
        HotelInformation, 
        related_name='images',
        on_delete=models.CASCADE,
        null=True
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No image"

    def save(self, *args, **kwargs):
        if not self.image:
            print("No image provided for this instance.")

        if self.pk is not None:
            self.updateDate = timezone.now()
        else:
            if Images.objects.filter(hotel=self.hotel, image=self.image).exists():
                raise ValueError(f"An image with the name {self.image} already exists for this hotel.")

        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Handle errors and possibly log them
            raise ValueError(f"Error saving image: {str(e)}")
        
    def delete(self, *args, **kwargs):
        if self.image:
            # Get the full file path
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            
            # Check if file exists and delete it
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                    print(f"Successfully deleted image file: {image_path}")
                except Exception as e:
                    print(f"Error deleting image file {image_path}: {str(e)}")
            else:
                print(f"Image file not found: {image_path}")
        else:
            print("No image file to delete")

        # Call the superclass delete method to remove the database record
        super().delete(*args, **kwargs)