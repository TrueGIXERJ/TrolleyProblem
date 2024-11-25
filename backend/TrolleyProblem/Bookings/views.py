from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Equipment
from django.contrib import messages
from .forms import BookingForm

@login_required
def home_view(request):
    """
    shows the homepage which has a simple welcome message and a list of open bookings assigned to the logged-in user
    """
    # get bookings for the logged-in user
    user_bookings = Booking.objects.filter(user=request.user).order_by('date', 'timeslot')

    context = {
        'bookings': user_bookings,
    }
    return render(request, 'home.html', context)

@login_required
def create_booking_view(request):
    """
    allows the logged-in user to create a booking.
    validates created booking by checking against available equipment
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # get the cleaned data from the create booking form
            cleaned_data = form.cleaned_data
            date = cleaned_data['date']
            timeslot = cleaned_data['timeslot']

            # check against available equipment during specified date and timeslot
            equipment_count = Equipment.objects.count()  # number of equipment instances in the database
            booked_equipment = Booking.objects.filter(date=date, timeslot=timeslot).count()

            # if there is no available equipment, raise an error
            if equipment_count <= booked_equipment:
                messages.error(request, "No equipment is available for this timeslot on the selected date.")
                return render(request, 'create_booking.html', {'form': form})

            # get the first available equipment (i.e., one not yet assigned to a booking)
            available_equipment = Equipment.objects.exclude(id__in=Booking.objects.filter(date=date, timeslot=timeslot).values('Equipment')).first()

            if available_equipment:
                # create the booking and associate the equipment
                booking = form.save(commit=False)
                booking.user = request.user
                booking.equipment = available_equipment
                booking.save()

                messages.success(request, "Your booking has been successfully created!")
                return redirect('home')  # redirect to the home page after successful booking
            else:
                messages.error(request, "No available equipment for the selected date and timeslot.")
                return render(request, 'create_booking.html', {'form': form})

        else:
            messages.error(request, "There was an error with your booking. Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})

@login_required
def delete_booking_view(request, booking_id):
    """
    allow the user to delete a booking
    """
    # get the booking, returns 404 if it doesn't exist
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # if it's a POST request, delete the booking (security!)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking successfully deleted.')
        return redirect('home')

    # if the request isn't POST (e.g., GET), redirect to the home page
    return redirect('home')
