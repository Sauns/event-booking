from django.db import transaction
from events.models import Booking


class PaymentService:

    @staticmethod
    def confirm_payment(booking_id):
        with transaction.atomic():

            booking = (
                Booking.objects
                .select_for_update()
                .get(id=booking_id)
            )

            # Idempotent behavior: repeated payment confirmation is successful
            # when booking is already confirmed.
            if booking.status == Booking.Status.CONFIRMED:
                return booking

            # Only pending bookings can be confirmed.
            if booking.status != Booking.Status.PENDING:
                raise ValueError("Booking is not available for payment")

            booking.status = Booking.Status.CONFIRMED
            booking.save()

            return booking