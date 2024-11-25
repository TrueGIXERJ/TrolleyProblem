from django import forms
from .models import Booking, Equipment
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    """
    A form for creating (and, in theory, updating) bookings.
    validates data by ensuring the booking date is valid and that there is available equipment for the selected date & timeslot
    """
    class Meta:
        model = Booking
        fields = ['date', 'timeslot', 'room', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'timeslot': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'date': 'Date',
            'timeslot': 'Timeslot',
            'room': 'Room',
            'notes': 'Notes (Optional)',
        }
    
    def clean_date(self):
        """
        Ensure the selected booking date is in the future.
        """
        selected_date = self.cleaned_data['date']

        today = datetime.today()
        earliest_allowed = today + timedelta(days=1)

        if selected_date < earliest_allowed.date():
            raise forms.ValidationError("Bookings must be made at least 24 hours in advance.")

        return selected_date

    def clean(self):
        """
        Check if there is enough equipment for the selected timeslot and date.
        """
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        timeslot = cleaned_data.get('timeslot')

        # ensure there is available equipment for the selected date & time
        equipment_count = Equipment.objects.count()  # number of equipment instances in the database
        booked_equipment = Booking.objects.filter(date=selected_date, timeslot=timeslot).count() # already booked equipment

        # if all equipment is booked during this period, raise an error
        if equipment_count <= booked_equipment:
            raise forms.ValidationError("No equipment is available for this timeslot on the selected date.")
        
        return cleaned_data
