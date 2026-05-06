from django.db import transaction
from django.utils import timezone
from events.models import Booking, Payment
from events.tasks import expire_booking_task


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

            Payment.objects.create(
                booking=booking,
                amount=booking.total_amount,
                status=Payment.Status.PAID,
                provider=Payment.Provider.STRIPE,
                provider_payment_id=f"fake-{booking.id}",
                paid_at=timezone.now(),
            )

            if booking.expire_task_id:
                expire_booking_task.AsyncResult(booking.expire_task_id).revoke()
                booking.expire_task_id = None

            booking.status = Booking.Status.CONFIRMED
            booking.save(update_fields=["status", "expire_task_id"])

            return booking