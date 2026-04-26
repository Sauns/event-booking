from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import EventFilter
from .models import Event, Booking
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    BookingCreateSerializer,
    BookingListSerializer,
    PaymentConfirmSerializer,
)

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all().select_related("organizer")
    serializer_class = EventListSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all() \
        .select_related("organizer") \
        .prefetch_related("ticket_types")
    serializer_class = EventDetailSerializer

class BookingListCreateAPIView(ListCreateAPIView):
    queryset = Booking.objects.all().select_related("user", "ticket_type__event")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookingListSerializer
        return BookingCreateSerializer

class PaymentConfirmAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = PaymentConfirmSerializer
    permission_classes = [IsAuthenticated]