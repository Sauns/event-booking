from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventListSerializer, EventDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all().select_related("organizer")
    serializer_class = EventListSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_active", "organizer"]

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all() \
        .select_related("organizer") \
        .prefetch_related("ticket_types")
    serializer_class = EventDetailSerializer
    