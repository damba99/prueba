# templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(value, arg):
    """
    Retorna el objeto Asistencia correspondiente al alumno con id `arg`
    """
    for asistencia in value:
        if asistencia.id_alumno == int(arg):
            return asistencia
    return None
