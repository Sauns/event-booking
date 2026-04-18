from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer


class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
