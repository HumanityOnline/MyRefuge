from django.contrib import admin

from .models import CitizenSpace, DateRange, SpacePhoto


class DateRangeInline(admin.StackedInline):
    model = DateRange
    extra = 1


class SpacePhotoInline(admin.StackedInline):
    model = SpacePhoto
    extra = 2


class CitizenSpaceAdmin(admin.ModelAdmin):
    inlines = [
        DateRangeInline,
        SpacePhotoInline
    ]

admin.site.register(CitizenSpace, CitizenSpaceAdmin)
