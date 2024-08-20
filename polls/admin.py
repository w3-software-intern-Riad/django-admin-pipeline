from django import forms
from django.contrib import admin
from polls.models import HotelInformation, Images, Amenities, Location
import os

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    max_num = 10
    exclude = ('updateDate',)
    can_delete = True

class HotelInformationAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]
    list_display = ('title', 'description', 'get_locations',
                    'get_amenities', 'get_images', 'createDate', 'updateDate')
    exclude = ('updateDate',)
    search_fields = ['title']
    filter_horizontal = ('locations', 'amenities')
    list_filter = ('createDate', 'updateDate', 'locations', 'amenities')  # Added filter

    def get_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()]) if obj.locations.exists() else "No Locations"
    get_locations.short_description = 'Locations'

    def get_amenities(self, obj):
        return ", ".join([amenity.name for amenity in obj.amenities.all()]) if obj.amenities.exists() else "No Amenities"
    get_amenities.short_description = 'Amenities'

    def get_images(self, obj):
        return ", ".join([os.path.basename(image.image.name) for image in obj.images.all()]) if obj.images.exists() else "No Images"
    get_images.short_description = 'Images'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Handle Location
        location_name = form.cleaned_data.get('location_name')
        if location_name:
            location, created = Location.objects.get_or_create(
                name=location_name,
                type=form.cleaned_data.get('location_type'),
                latitude=form.cleaned_data.get('latitude'),
                longitude=form.cleaned_data.get('longitude')
            )
            obj.locations.add(location)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # This will trigger the delete method in the model

class ImageInformationAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'hotel', 'createDate', 'updateDate')
    search_fields = ['image']
    exclude = ('updateDate',)
    list_filter = ('createDate', 'updateDate', 'hotel')  # Added filter

    def image_name(self, obj):
        return os.path.basename(obj.image.name) if obj.image else "No image"
    image_name.short_description = 'Image'

    def hotel(self, obj):
        return obj.hotel.title if obj.hotel else "No Hotel"
    hotel.short_description = 'Hotel'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # This will trigger the delete method in the model

class LocationInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'get_hotels', 'latitude',
                    'longitude', 'createDate', 'updateDate')
    search_fields = ['name', 'hotels__title']
    exclude = ('updateDate',)
    list_filter = ('type', 'createDate', 'updateDate')  # Added filter

    def get_hotels(self, obj):
        return ", ".join([hotel.title for hotel in obj.hotels.all()]) if obj.hotels.exists() else "No Hotels"
    get_hotels.short_description = 'Hotels'

class AmenitiesInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_hotels', 'createDate', 'updateDate')
    search_fields = ['name', 'hotels__title']
    exclude = ('updateDate',)
    list_filter = ('createDate', 'updateDate')  # Added filter

    def get_hotels(self, obj):
        return ", ".join([hotel.title for hotel in obj.hotels.all()]) if obj.hotels.exists() else "No Hotels"
    get_hotels.short_description = 'Hotels'

# Register the models with the customized admin classes
admin.site.register(HotelInformation, HotelInformationAdmin)
admin.site.register(Images, ImageInformationAdmin)
admin.site.register(Location, LocationInformationAdmin)
admin.site.register(Amenities, AmenitiesInformationAdmin)