from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for Application model.

    Provides a clean interface for managing applications in the Django admin.
    """

    list_display = ("protocol", "url", "port", "full_address")
    list_filter = ("protocol",)
    search_fields = ("url", "port")
    ordering = ("protocol", "url", "port")

    fieldsets = (("Application Details", {"fields": ("protocol", "url", "port")}),)

    def full_address(self, obj):
        """Display the full address in the admin list view."""
        return obj.full_address

    full_address.short_description = "Full Address"
