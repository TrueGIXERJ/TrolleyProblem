from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Equipment
from django.contrib import messages
from .forms import BookingForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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

                if getattr(settings, 'EMAIL_NOTIFICATIONS_ENABLED', False):
                    messages.success(request, "Your booking has been successfully created, a confirmation email will be sent shortly.")

                    subject = "Booking Confirmation"
                    context = {
                        'user': request.user,
                        'booking': booking,
                    }
                    html_message = render_to_string('email_templates/booking_confirmation.html', context)
                    plain_message = strip_tags(html_message)
                    recipient_email = request.user.email

                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email],
                        html_message=html_message,
                    )

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
