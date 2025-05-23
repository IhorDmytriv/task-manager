from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def time_until(deadline: datetime) -> str:

    delta = (deadline - timezone.now().date()).days

    if delta < 0:
        return f"Overdue by {-delta} {'day' if delta == -1 else 'days'}"
    elif delta == 0:
        return "Today"
    return f"{delta} {'day' if delta == 1 else 'days'} left"
