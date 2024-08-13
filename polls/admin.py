from django.contrib import admin
from polls.models import HotelInformation, Images, Amenities, Location

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1  # Number of empty forms to display
    max_num = 10  # Maximum number of forms
    exclude = ('updateDate',)


class AmenitiesInLine(admin.TabularInline):
    model=Amenities
    extra=1
    max_num=50
    exclude = ('updateDate',)

class LocationInLine(admin.TabularInline):
    model=Location
    extra=1
    max_num=1
    exclude = ('updateDate',)
class HotelInformationAdmin(admin.ModelAdmin):
    inlines = [ImagesInline,LocationInLine,AmenitiesInLine]
    list_display = ('title', 'description', 'createDate', )
    exclude = ('updateDate',) 
    


   

admin.site.register(HotelInformation, HotelInformationAdmin)

