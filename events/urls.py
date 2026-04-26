from django.urls import path
from .views import EventListAPIView, EventDetailAPIView, BookingListCreateAPIView, PaymentConfirmAPIView

urlpatterns = [
    path("events/", EventListAPIView.as_view(), name="event-list"),
    path("events/<int:pk>/", EventDetailAPIView.as_view(), name="event-detail"),
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("payments/confirm/", PaymentConfirmAPIView.as_view(), name="payment-confirm"),
]