from django.contrib import admin
from polls.models import HotelInformation, Images, Amenities, Location
import os
from django.utils.html import format_html
from django.urls import reverse


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    max_num = 10
    exclude = ('updateDate',)
    can_delete = True


class AmenitiesInLine(admin.TabularInline):
    model = Amenities
    extra = 1
    max_num = 50
    exclude = ('updateDate',)
    can_delete = True


class LocationInLine(admin.TabularInline):
    model = Location
    extra = 1
    max_num = 1
    exclude = ('updateDate',)


class HotelInformationAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, LocationInLine, AmenitiesInLine]
    list_display = ('title', 'description',  'get_location',
                    'get_amenities', 'get_images', 'createDate', 'updateDate')
    exclude = ('updateDate',)
    search_fields = ['title']

    def get_location(self, obj):
        if obj.locations.exists():
            location = obj.locations.first()
            return f"{location.name} ({location.get_type_display()}), Lat: {location.latitude}, Lon: {location.longitude}"
        return "No Location"

    get_location.short_description = 'Location'

    def get_amenities(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()]) if obj.amenities.exists() else "No Amenities"

    get_amenities.short_description = 'Amenities'

    def get_images(self, obj):
        return ", ".join([os.path.basename(image.image.name) for image in obj.images.all()]) if obj.images.exists() else "No Images"

    get_images.short_description = 'Images'


class ImageInformationAdmin(admin.ModelAdmin):
    
    list_display = ('image_name', 'hotel', 'createDate', 'updateDate')
    search_fields = ['image']
    exclude = ('updateDate',)
    def image_name(self, obj):
        return os.path.basename(obj.image.name) if obj.image else "No image"
    image_name.short_description = 'Image'
    def hotel(self, obj):
        return obj.hotel.title if obj.hotel else "No Hotel"
    hotel.short_description = 'Hotel'


class LocationInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'latitude', 'longitude', 'createDate', 'updateDate')
    search_fields = ['name', 'hotel__title']
    exclude = ('updateDate',)
    def hotel(self, obj):
        return obj.hotel.title if obj.hotel else "No Hotel"
    hotel.short_description = 'Hotel'


class AmenitiesInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'createDate', 'updateDate')
    search_fields = ['name', 'hotel__title']
    exclude = ('updateDate',)
    def hotel(self, obj):
        return obj.hotel.title if obj.hotel else "No Hotel"
    hotel.short_description = 'Hotel'


# Register the models with the customized admin classes
admin.site.register(HotelInformation, HotelInformationAdmin)
admin.site.register(Images,ImageInformationAdmin)
admin.site.register(Location, LocationInformationAdmin)
admin.site.register(Amenities, AmenitiesInformationAdmin)
