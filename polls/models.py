# models.py
from django.db import models
from django.utils import timezone
import os
from django.core.files import File
from django.core.files.storage import default_storage

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
        super().save(*args, **kwargs)

class HotelInformation(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    rating = models.FloatField(null=True, blank=True)  # Make rating optional
    price = models.FloatField(null=True, blank=True)    # Make price optional
    roomType = models.CharField(max_length=400, null=True, blank=True)  # Make roomType optional
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updateDate = timezone.now()
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
                    print("No Image is found")    
    
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
        return os.path.basename(self.image.name)

    def save(self, *args, **kwargs):
        if self.image:
            # Extract only the filename before saving
            filename = os.path.basename(self.image.name)
            # Create a new file with the same name
            
            f = File(self.image, name=filename)
            self.image = f

        if self.pk is not None:
            self.updateDate = timezone.now()
        
        super().save(*args, **kwargs)