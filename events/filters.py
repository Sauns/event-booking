import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    start_after = django_filters.DateTimeFilter(
        field_name="start_datetime",
        lookup_expr="gte",
    )
    start_before = django_filters.DateTimeFilter(
        field_name="start_datetime",
        lookup_expr="lte",
    )

    class Meta:
        model = Event
        fields = ["is_active", "organizer"]
