from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LucernaUser


@admin.register(LucernaUser)
class LucernaUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Lucerna", {"fields": ("clearance_level",)}),
    )
    list_display = UserAdmin.list_display + ("clearance_level",)
    list_filter = UserAdmin.list_filter + ("clearance_level",)
