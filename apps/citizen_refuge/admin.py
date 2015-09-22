from django.contrib import admin

from .models import CitizenSpace, DateRange


class DateRangeInline(admin.StackedInline):
    model = DateRange
    extra = 1


class CitizenSpaceAdmin(admin.ModelAdmin):
    inlines = [
        DateRangeInline,
    ]

admin.site.register(CitizenSpace, CitizenSpaceAdmin)
