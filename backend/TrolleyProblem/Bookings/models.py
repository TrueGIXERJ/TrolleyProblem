from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Equipment(models.Model):
    """
    Equipment model to store available equipment
    No more bookings can be created on a specific Date&Timeslot than there are equipment items
    Can be expanded to store information about specific items of equipment (Name/Type/Etc)
    """

    def __str__(self):
        # return a string representation for the equipment instance
        return f"Equipment ID: {self.id}"

    class Meta:
        # sets the singular name for the admin panel
        verbose_name = "Equipment"

class Booking(models.Model):
    """
    Booking model to manage information about a booking

    :user:  foreign key, connection to django's user model
    :date:  the date the booking is for
    :timeslot:  the timeslot the booking is for on the day - options are listed in TIME_CHOICES (1,2,3,4,5,OTHER)
    :room:  the room/location associated with the booking
    :notes: any additional information/notes about the booking
    :created_date:  the datetime that the booking was created on, added automatically
    :status:    the status of the booking: OPEN, IN_PROGRESS, or CLOSED. bookings that are CLOSED are automatically deleted
    :equipment: foreign key, assigns an instance of equipment to the booking
    """
    # choices for available timeslots
    TIME_CHOICES = [
        ('1', 'Timeslot 1'),
        ('2', 'Timeslot 2'),
        ('3', 'Timeslot 3'),
        ('4', 'Timeslot 4'),
        ('5', 'Timeslot 5'),
        ('OTHER', 'Other (Please Add In Notes)'),
    ]
    # choices for booking status
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='user',
    )
    date = models.DateField(
        verbose_name='Booking Date',
    )
    timeslot = models.CharField(
        max_length=15,
        choices=TIME_CHOICES,
        verbose_name='Timeslot',
    )
    room = models.CharField(
        max_length=10,
        verbose_name='Room',
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notes',
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation Date',
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='OPEN',
        verbose_name='Status',
    )
    Equipment = models.ForeignKey(
        Equipment, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        """
        return a string representation of the booking e.g.
        OPEN - 2024-12-02 - 5 - user1 - 2024-11-25 15:53:01.709580+00:00
        """
        return f"{self.status} - {self.date} - {self.timeslot} - {self.room} - {self.user.username} - {self.created_date}"

# receiver calls function when bookings are saved
@receiver(post_save, sender=Booking)
def delete_closed_booking(sender, instance, **kwargs):
    """
    delete a booking if its status is set to 'CLOSED', called after the instance is saved.
    """
    if instance.status == 'CLOSED':
        instance.delete()
