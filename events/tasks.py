from celery import shared_task
from django.db import transaction

from events.models import Booking


@shared_task
def expire_booking_task(booking_id):
    with transaction.atomic():
        try:
            booking = Booking.objects.select_for_update().get(id=booking_id)
        except Booking.DoesNotExist:
            return

        if booking.status != "pending":
            return

        ticket_type = booking.ticket_type

        ticket_type.quantity_available += booking.quantity
        ticket_type.save()

        booking.status = "expired"
        booking.save()