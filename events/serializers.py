from rest_framework import serializers
from .models import Event, TicketType

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