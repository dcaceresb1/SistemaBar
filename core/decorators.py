from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def roles_permitidos(*roles):

    def decorador(vista):

        @wraps(vista)
        @login_required
        def funcion_protegida(request, *args, **kwargs):

            usuario = request.user

            # El superusuario tiene acceso completo.
            if usuario.is_superuser:
                return vista(request, *args, **kwargs)

            # Comprobar si pertenece a un grupo autorizado.
            autorizado = usuario.groups.filter(
                name__in=roles
            ).exists()

            if not autorizado:
                raise PermissionDenied(
                    'No tienes permisos para acceder a esta función.'
                )

            return vista(request, *args, **kwargs)

        return funcion_protegida

    return decorador