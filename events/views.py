from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .filters import EventFilter
from .models import Event
from .serializers import EventListSerializer, EventDetailSerializer

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
    