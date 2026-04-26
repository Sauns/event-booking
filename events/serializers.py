from rest_framework import serializers
from .models import Event, TicketType, Booking
from .services.booking_service import BookingService, NotEnoughTicketsError
from .services.payment_service import PaymentService

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "start_datetime",
            "organizer",
        ]

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = [
            "id",
            "name",
            "price",
            "quantity_available",
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "venue",
            "start_datetime",
            "end_datetime",
            "organizer",
            "ticket_types",
        ]

class BookingCreateSerializer(serializers.Serializer):
    ticket_type_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            return BookingService.create_booking(
                user=user,
                ticket_type_id=validated_data["ticket_type_id"],
                quantity=validated_data["quantity"],
            )
        except NotEnoughTicketsError as e:
            raise serializers.ValidationError(str(e))

class BookingListSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source="ticket_type.event_id", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "ticket_type",
            "event_id",
            "quantity",
            "total_amount",
            "status",
            "booked_at",
            "updated_at",
        ]

class PaymentConfirmSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()

    def create(self, validated_data):
        try:
            return PaymentService.confirm_payment(
                booking_id=validated_data["booking_id"]
            )
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking not found")
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return {
            "booking_id": instance.id,
            "status": instance.status,
        }