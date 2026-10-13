from django import template

register = template.Library()


@register.filter
def tiene_rol(usuario, nombre_rol):

    if not usuario.is_authenticated:
        return False

    if usuario.is_superuser:
        return True

    return usuario.groups.filter(
        name=nombre_rol
    ).exists()