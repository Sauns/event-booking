from django.db import transaction
from events.models import Booking, TicketType
from events.tasks import expire_booking_task


class NotEnoughTicketsError(Exception):
    pass


class BookingService:

    @staticmethod
    def create_booking(user, ticket_type_id, quantity):
        with transaction.atomic():

            ticket_type = (
                TicketType.objects
                .select_for_update()
                .get(id=ticket_type_id)
            )

            if ticket_type.quantity_available < quantity:
                raise NotEnoughTicketsError("Not enough tickets")

            total_amount = ticket_type.price * quantity

            booking = Booking.objects.create(
                user=user,
                ticket_type=ticket_type,
                quantity=quantity,
                total_amount=total_amount,
                status="pending",
            )

            expire_booking_task.apply_async(
                args=[booking.id],
                countdown=900
            )

            ticket_type.quantity_available -= quantity
            ticket_type.save()

            return booking