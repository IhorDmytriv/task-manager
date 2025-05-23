from django import template

register = template.Library()


@register.simple_tag
def toggle_sort(request, field_name):
    current_sort = request.GET.get("sort", "")
    return f"-{field_name}" if current_sort == field_name else field_name
