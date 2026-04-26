from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("start_datetime",)
        indexes = [
            models.Index(fields=["start_datetime"]),
            models.Index(fields=["organizer", "start_datetime"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.start_datetime:%Y-%m-%d %H:%M})"


class TicketType(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="ticket_types",
    )
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_total = models.PositiveIntegerField()
    quantity_available = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    sales_start = models.DateTimeField(null=True, blank=True)
    sales_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "name"],
                name="unique_ticket_type_name_per_event",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity_available__lte=models.F("quantity_total")),
                name="available_lte_total",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.event.title} - {self.name}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        CONFIRMED = "confirmed", _("Confirmed")
        CANCELLED = "cancelled", _("Cancelled")
        EXPIRED = "expired", _("Expired")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-booked_at",)
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["ticket_type", "status"]),
            models.Index(fields=["booked_at"]),
        ]

    def __str__(self) -> str:
        return f"Booking #{self.pk} - {self.user} - {self.status}"


class Payment(models.Model):
    class Provider(models.TextChoices):
      STRIPE = "stripe", "Stripe"
      PAYPAL = "paypal", "PayPal"
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    provider = models.CharField(max_length=80, choices=Provider.choices, blank=True)
    provider_payment_id = models.CharField(max_length=128, blank=True, null=True, unique=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["booking", "status"]),
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["provider"]),
        ]

    def __str__(self) -> str:
        return f"Payment #{self.pk} - Booking #{self.booking_id} - {self.status}"