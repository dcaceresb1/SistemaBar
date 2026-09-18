from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

def lista_productos(request):

    productos = Producto.objects.select_related(
        'categoria'
    ).order_by('nombre')

    contexto = {
        'productos': productos,
    }

    return render(
        request,
        'productos/lista_productos.html',
        contexto
    )
def crear_producto(request):

    if request.method == 'POST':

        formulario = ProductoForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            return redirect('lista_productos')

    else:
        formulario = ProductoForm()

    contexto = {
        'formulario': formulario,
    }

    return render(
        request,
        'productos/crear_producto.html',
        contexto
    )