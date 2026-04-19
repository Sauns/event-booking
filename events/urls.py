from django.urls import path
from .views import EventListAPIView, EventDetailAPIView

urlpatterns = [
    path("events/", EventListAPIView.as_view(), name="event-list"),
    path("events/<int:pk>/", EventDetailAPIView.as_view(), name="event-detail"),
]