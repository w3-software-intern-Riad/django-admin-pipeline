# models.py
from django.db import models
from django.utils import timezone
import os
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError


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
    rating = models.FloatField(null=False,default=0)  
    price = models.FloatField(null=False,default=0)    
    roomType = models.CharField(max_length=400,null=False,default="Single")  # Make roomType optional
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
            if image.image and default_storage.exists(image.image.name):
            # Get the full file path
                image_path = default_storage.path(image.image.name)
                if os.path.isfile(image_path):
                    os.remove(image_path)
                else:
                    print("No image found at", image_path)

            else:
                if not image.image:
                    print(f"No image file associated with {image}")
                elif not default_storage.exists(image.image.name):
                    print(f"Image file {image.image.name} does not exist in storage")
    
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
        if self.image:
            # Extract the filename
            filename = os.path.basename(self.image.name)
            self.image.name = filename

            # Check if the file is already in the database
            existing_image = Images.objects.filter(image=self.image.name).exclude(hotel=self.hotel).first()
            if existing_image:
                raise ValidationError(f"An image with the name '{self.image.name}' is already associated with another hotel.")

            # Check if the file already exists in the local file storage
            if default_storage.exists(f'images/{filename}'):
                raise ValidationError(f"An image with the name '{filename}' already exists in the file storage.")

        else:
            print("No image provided for this instance.")

        if self.pk is not None:
            self.updateDate = timezone.now()
        else:
            print("Creating a new instance; updateDate will not be set.")

        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Handle errors and possibly log them
            raise ValueError(f"Error saving image: {str(e)}")