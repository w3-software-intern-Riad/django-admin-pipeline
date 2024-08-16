from django.db import models
from django.utils import timezone
import os
from django.conf import settings


class Amenities(models.Model):
    name = models.CharField(max_length=200, unique=True)
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
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(null=True, blank=True)    

    class Meta:
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updateDate = timezone.now()
        super().save(*args, **kwargs)


class HotelInformation(models.Model):
    title = models.CharField(max_length=500, unique=True)
    description = models.TextField(max_length=50000, null=True, blank=True)
    locations = models.ManyToManyField(Location, related_name='hotels')
    amenities = models.ManyToManyField(Amenities, related_name='hotels')
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
            if image.image:
                image_path = os.path.join(
                    settings.MEDIA_ROOT, str(image.image))
                if os.path.isfile(image_path):
                    try:
                        os.remove(image_path)
                    except Exception as e:
                        print(f"Error deleting image {image_path}: {str(e)}")
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
                raise ValueError(
                    f"An image with the name {self.image} already exists for this hotel.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"Error deleting image file {image_path}: {str(e)}")
        super().delete(*args, **kwargs)
