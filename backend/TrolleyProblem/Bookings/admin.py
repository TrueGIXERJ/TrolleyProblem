from django.contrib import admin
from .models import Booking, Equipment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    creates the admin interface for the booking model
    """

    # fields to display in the list view
    list_display = ('status', 'date', 'timeslot', 'room', 'user')

    # fields that are clickable in the list view to expand details
    list_display_links = ('date', 'timeslot', 'room', 'user')

    # filter options in the right sidebar
    list_filter = ('status',)

    # fields editable directly from the list view
    list_editable = ('status',)

    # default ordering of the bookings, earliest bookingdate first
    ordering = ('-date',)

    # readonly fields that prevent editing
    readonly_fields = ('created_date',)

    # organise fields into sections for clarity in the admin form
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'timeslot', 'room', 'notes', 'status'),
        }),
        ('Metadata', {
            'fields': ('created_date',),
        }),
    )

# register the Equipment model with default admin interface
admin.site.register(Equipment)