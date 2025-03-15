from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def time_until(deadline: datetime) -> str:
    if not deadline:
        return "No deadline"

    delta = (deadline - timezone.now().date()).days

    if delta < 0:
        return f"Overdue by {-delta} {'day' if delta == -1 else 'days'}"
    elif delta == 0:
        return "Today"
    else:
        return f"{delta} {'day' if delta == 1 else 'days'} left"
