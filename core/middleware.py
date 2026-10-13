from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        login_url = reverse('login')

        rutas_publicas = [
            login_url,
        ]

        ruta_actual = request.path_info

        # Permitir acceso a archivos estáticos y multimedia
        rutas_excluidas = [
            settings.STATIC_URL,
            settings.MEDIA_URL,
        ]

        # Permitir acceso a la pantalla de inicio de sesión
        if ruta_actual in rutas_publicas:
            return self.get_response(request)

        # Permitir archivos CSS, imágenes y otros recursos
        if any(
            ruta_actual.startswith(ruta)
            for ruta in rutas_excluidas
            if ruta
        ):
            return self.get_response(request)

        # Permitir acceso al administrador de Django
        # Django Admin ya tiene su propia autenticación
        if ruta_actual.startswith('/admin/'):
            return self.get_response(request)

        # Comprobar si el usuario inició sesión
        if not request.user.is_authenticated:

            return redirect(
                f'{login_url}?next={request.get_full_path()}'
            )

        return self.get_response(request)