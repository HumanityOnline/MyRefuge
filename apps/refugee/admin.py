from django.contrib import admin

from .models import Refugee, FamilyMember


class FamilyMemberInline(admin.StackedInline):
    model = FamilyMember
    extra = 1


class RefugeeAdmin(admin.ModelAdmin):
    inlines = [
        FamilyMemberInline,
    ]


admin.site.register(Refugee, RefugeeAdmin)
