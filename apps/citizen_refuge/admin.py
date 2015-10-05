from django.contrib import admin

from .models import CitizenRefuge, CitizenSpace, DateRange, SpacePhoto


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

    readonly_fields = ('public_address', 'city', 'country',)

admin.site.register(CitizenSpace, CitizenSpaceAdmin)
admin.site.register(CitizenRefuge)
