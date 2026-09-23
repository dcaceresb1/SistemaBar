from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Producto,
    Categoria,
    MovimientoInventario,
    Proveedor,
    Compra,
    DetalleCompra,
    Venta,
    DetalleVenta,
    
)
from .forms import (
    ProductoForm,
    CategoriaForm,
    MovimientoInventarioForm,
    ProveedorForm,
    CompraForm,
    DetalleCompraForm,
    VentaForm,
    DetalleVentaForm,
)

from django.db.models import Q
from django.contrib import messages
from django.db import transaction


def lista_productos(request): #LISTAR PRODUCTOS#

    busqueda = request.GET.get('buscar', '')
    categoria_id = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')

    productos = Producto.objects.select_related(
        'categoria'
    ).order_by('nombre')

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda)
        )

    if categoria_id:
        productos = productos.filter(
            categoria_id=categoria_id
        )

    if estado == 'activo':
        productos = productos.filter(
            activo=True
        )

    elif estado == 'inactivo':
        productos = productos.filter(
            activo=False
        )

    categorias = Categoria.objects.filter(
        activo=True
    ).order_by('nombre')

    contexto = {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_id,
        'estado_seleccionado': estado,
    }

    return render(
        request,
        'productos/lista_productos.html',
        contexto
    )

def crear_producto(request):  #CREAR PRODUCTO#

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

def editar_producto(request, producto_id): #EDITAR PRODUCTO#

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':

        formulario = ProductoForm(
            request.POST,
            instance=producto
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_productos')

    else:
        formulario = ProductoForm(
            instance=producto
        )

    contexto = {
        'formulario': formulario,
        'producto': producto,
    }

    return render(
        request,
        'productos/editar_producto.html',
        contexto
    )

def desactivar_producto(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        producto.activo = False #si queremos borrar el registro de la base de datos, podemos usar producto.delete() en lugar de producto.activo = False#
        producto.save()

        return redirect('lista_productos')

    contexto = {
        'producto': producto,
    }

    return render(
        request,
        'productos/desactivar_producto.html',
        contexto
    )

def reactivar_producto(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    if request.method == 'POST':
        producto.activo = True
        producto.save()

        return redirect('lista_productos')

    contexto = {
        'producto': producto,
    }

    return render(
        request,
        'productos/reactivar_producto.html',
        contexto
    )

def lista_categorias(request):

    categorias = Categoria.objects.order_by('nombre')

    contexto = {
        'categorias': categorias,
    }

    return render(
        request,
        'productos/lista_categorias.html',
        contexto
    )

def crear_categoria(request):

    if request.method == 'POST':

        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            return redirect('lista_categorias')

    else:
        formulario = CategoriaForm()

    contexto = {
        'formulario': formulario,
    }

    return render(
        request,
        'productos/crear_categoria.html',
        contexto
    )

def editar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    if request.method == 'POST':

        formulario = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if formulario.is_valid():
            formulario.save()

            return redirect('lista_categorias')

    else:

        formulario = CategoriaForm(
            instance=categoria
        )

    contexto = {
        'formulario': formulario,
        'categoria': categoria,
    }

    return render(
        request,
        'productos/editar_categoria.html',
        contexto
    )

def desactivar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    if request.method == 'POST':
        categoria.activo = False
        categoria.save()

        return redirect('lista_categorias')

    contexto = {
        'categoria': categoria,
    }

    return render(
        request,
        'productos/desactivar_categoria.html',
        contexto
    )


def reactivar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    if request.method == 'POST':
        categoria.activo = True
        categoria.save()

        return redirect('lista_categorias')

    contexto = {
        'categoria': categoria,
    }

    return render(
        request,
        'productos/reactivar_categoria.html',
        contexto
    )

def inventario(request):

    productos = Producto.objects.filter(
        activo=True
    ).select_related(
        'categoria'
    ).order_by('nombre')

    contexto = {
        'productos': productos,
    }

    return render(
        request,
        'productos/inventario.html',
        contexto
    )

def registrar_movimiento(request, producto_id):

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        activo=True
    )

    if request.method == 'POST':

        formulario = MovimientoInventarioForm(
            request.POST
        )

        if formulario.is_valid():

            tipo = formulario.cleaned_data['tipo']
            cantidad = formulario.cleaned_data['cantidad']

            if cantidad <= 0:
                formulario.add_error(
                    'cantidad',
                    'La cantidad debe ser mayor que cero.'
                )

            elif tipo == 'SALIDA' and cantidad > producto.stock:
                formulario.add_error(
                    'cantidad',
                    'No existe suficiente stock para realizar esta salida.'
                )

            else:

                with transaction.atomic():

                    stock_anterior = producto.stock

                    if tipo == 'ENTRADA':
                        producto.stock += cantidad

                    else:
                        producto.stock -= cantidad

                    producto.save(
                        update_fields=['stock']
                    )

                    movimiento = formulario.save(
                        commit=False
                    )

                    movimiento.producto = producto
                    movimiento.stock_anterior = stock_anterior
                    movimiento.stock_nuevo = producto.stock

                    movimiento.save()

                messages.success(
                    request,
                    'Movimiento registrado correctamente.'
                )

                return redirect('inventario')

    else:

        formulario = MovimientoInventarioForm()

    contexto = {
        'producto': producto,
        'formulario': formulario,
    }

    return render(
        request,
        'productos/registrar_movimiento.html',
        contexto
    )

def historial_inventario(request):

    producto_id = request.GET.get('producto', '')
    tipo = request.GET.get('tipo', '')
    motivo = request.GET.get('motivo', '')

    movimientos = MovimientoInventario.objects.select_related(
        'producto'
    ).order_by('-fecha')

    if producto_id:
        movimientos = movimientos.filter(
            producto_id=producto_id
        )

    if tipo:
        movimientos = movimientos.filter(
            tipo=tipo
        )

    if motivo:
        movimientos = movimientos.filter(
            motivo=motivo
        )

    productos = Producto.objects.order_by('nombre')

    contexto = {
        'movimientos': movimientos,
        'productos': productos,
        'tipos_movimiento': MovimientoInventario.TIPOS_MOVIMIENTO,
        'motivos': MovimientoInventario.MOTIVOS,
        'producto_seleccionado': producto_id,
        'tipo_seleccionado': tipo,
        'motivo_seleccionado': motivo,
    }

    return render(
        request,
        'productos/historial_inventario.html',
        contexto
    )

def lista_proveedores(request):

    proveedores = Proveedor.objects.order_by('nombre')

    contexto = {
        'proveedores': proveedores,
    }

    return render(
        request,
        'productos/lista_proveedores.html',
        contexto
    )


def crear_proveedor(request):

    if request.method == 'POST':
        formulario = ProveedorForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_proveedores')

    else:
        formulario = ProveedorForm()

    contexto = {
        'formulario': formulario,
    }

    return render(
        request,
        'productos/crear_proveedor.html',
        contexto
    )


def editar_proveedor(request, proveedor_id):

    proveedor = get_object_or_404(
        Proveedor,
        id=proveedor_id
    )

    if request.method == 'POST':

        formulario = ProveedorForm(
            request.POST,
            instance=proveedor
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_proveedores')

    else:

        formulario = ProveedorForm(
            instance=proveedor
        )

    contexto = {
        'formulario': formulario,
        'proveedor': proveedor,
    }

    return render(
        request,
        'productos/editar_proveedor.html',
        contexto
    )


def desactivar_proveedor(request, proveedor_id):

    proveedor = get_object_or_404(
        Proveedor,
        id=proveedor_id
    )

    if request.method == 'POST':
        proveedor.activo = False
        proveedor.save(
            update_fields=['activo']
        )

        return redirect('lista_proveedores')

    contexto = {
        'proveedor': proveedor,
    }

    return render(
        request,
        'productos/desactivar_proveedor.html',
        contexto
    )


def reactivar_proveedor(request, proveedor_id):

    proveedor = get_object_or_404(
        Proveedor,
        id=proveedor_id
    )

    if request.method == 'POST':
        proveedor.activo = True
        proveedor.save(
            update_fields=['activo']
        )

        return redirect('lista_proveedores')

    contexto = {
        'proveedor': proveedor,
    }

    return render(
        request,
        'productos/reactivar_proveedor.html',
        contexto
    )


def lista_compras(request):

    compras = Compra.objects.select_related(
        'proveedor'
    ).order_by('-fecha')

    contexto = {
        'compras': compras,
    }

    return render(
        request,
        'productos/lista_compras.html',
        contexto
    )


def crear_compra(request):

    if request.method == 'POST':

        formulario = CompraForm(
            request.POST
        )

        if formulario.is_valid():

            compra = formulario.save(
                commit=False
            )

            compra.estado = 'BORRADOR'
            compra.save()

            return redirect(
                'detalle_compra',
                compra_id=compra.id
            )

    else:

        formulario = CompraForm()

    contexto = {
        'formulario': formulario,
    }

    return render(
        request,
        'productos/crear_compra.html',
        contexto
    )


def detalle_compra(request, compra_id):

    compra = get_object_or_404(
        Compra.objects.select_related('proveedor'),
        id=compra_id
    )

    detalles = compra.detalles.select_related(
        'producto'
    ).all()

    total = sum(
        detalle.subtotal
        for detalle in detalles
    )

    contexto = {
        'compra': compra,
        'detalles': detalles,
        'total': total,
    }

    return render(
        request,
        'productos/detalle_compra.html',
        contexto
    )

def agregar_producto_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    if compra.estado != 'BORRADOR':
        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    if request.method == 'POST':

        formulario = DetalleCompraForm(
            request.POST
        )

        if formulario.is_valid():

            detalle = formulario.save(
                commit=False
            )

            detalle.compra = compra
            detalle.save()

            return redirect(
                'detalle_compra',
                compra_id=compra.id
            )

    else:

        formulario = DetalleCompraForm()

    contexto = {
        'compra': compra,
        'formulario': formulario,
    }

    return render(
        request,
        'productos/agregar_producto_compra.html',
        contexto
    )

def editar_detalle_compra(request, detalle_id):

    detalle = get_object_or_404(
        DetalleCompra.objects.select_related(
            'compra',
            'producto'
        ),
        id=detalle_id
    )

    compra = detalle.compra

    if compra.estado != 'BORRADOR':
        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    if request.method == 'POST':

        formulario = DetalleCompraForm(
            request.POST,
            instance=detalle
        )

        if formulario.is_valid():
            formulario.save()

            return redirect(
                'detalle_compra',
                compra_id=compra.id
            )

    else:

        formulario = DetalleCompraForm(
            instance=detalle
        )

    contexto = {
        'compra': compra,
        'detalle': detalle,
        'formulario': formulario,
    }

    return render(
        request,
        'productos/editar_detalle_compra.html',
        contexto
    )

def eliminar_detalle_compra(request, detalle_id):

    detalle = get_object_or_404(
        DetalleCompra.objects.select_related(
            'compra',
            'producto'
        ),
        id=detalle_id
    )

    compra = detalle.compra

    if compra.estado != 'BORRADOR':
        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    if request.method == 'POST':

        detalle.delete()

        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    contexto = {
        'compra': compra,
        'detalle': detalle,
    }

    return render(
        request,
        'productos/eliminar_detalle_compra.html',
        contexto
    )

def confirmar_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    if compra.estado != 'BORRADOR':
        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    if request.method == 'POST':

        with transaction.atomic():

            compra = Compra.objects.select_for_update().get(
                id=compra_id
            )

            if compra.estado != 'BORRADOR':
                return redirect(
                    'detalle_compra',
                    compra_id=compra.id
                )

            detalles = compra.detalles.select_related(
                'producto'
            ).all()

            if not detalles.exists():
                return redirect(
                    'detalle_compra',
                    compra_id=compra.id
                )

            for detalle in detalles:

                producto = Producto.objects.select_for_update().get(
                    id=detalle.producto_id
                )

                stock_anterior = producto.stock

                producto.stock += detalle.cantidad

                producto.costo_compra = detalle.costo_unitario

                producto.save(
                    update_fields=[
                        'stock',
                        'costo_compra',
                        'fecha_actualizacion',
                    ]
                )

                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='ENTRADA',
                    motivo='COMPRA',
                    cantidad=detalle.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock,
                    observacion=f'Compra #{compra.id}'
                )

            compra.estado = 'CONFIRMADA'

            compra.save(
                update_fields=['estado']
            )

        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    contexto = {
        'compra': compra,
        'detalles': compra.detalles.select_related(
            'producto'
        ).all(),
    }

    return render(
        request,
        'productos/confirmar_compra.html',
        contexto
    )

def anular_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    if compra.estado != 'CONFIRMADA':
        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    if request.method == 'POST':

        with transaction.atomic():

            compra = Compra.objects.select_for_update().get(
                id=compra_id
            )

            if compra.estado != 'CONFIRMADA':
                return redirect(
                    'detalle_compra',
                    compra_id=compra.id
                )

            detalles = compra.detalles.select_related(
                'producto'
            ).all()

            # Primero comprobamos que todos los productos
            # tengan stock suficiente para revertir la compra.
            for detalle in detalles:

                producto = Producto.objects.select_for_update().get(
                    id=detalle.producto_id
                )

                if producto.stock < detalle.cantidad:

                    contexto = {
                        'compra': compra,
                        'detalles': detalles,
                        'error': (
                            f'No se puede anular la compra porque '
                            f'{producto.nombre} tiene solamente '
                            f'{producto.stock} unidades disponibles.'
                        ),
                    }

                    return render(
                        request,
                        'productos/anular_compra.html',
                        contexto
                    )

            # Si todo está correcto, revertimos el inventario.
            for detalle in detalles:

                producto = Producto.objects.select_for_update().get(
                    id=detalle.producto_id
                )

                stock_anterior = producto.stock

                producto.stock -= detalle.cantidad

                producto.save(
                    update_fields=[
                        'stock',
                        'fecha_actualizacion',
                    ]
                )

                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='SALIDA',
                    motivo='AJUSTE',
                    cantidad=detalle.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock,
                    observacion=(
                        f'Anulación de compra #{compra.id}'
                    )
                )

            compra.estado = 'ANULADA'

            compra.save(
                update_fields=['estado']
            )

        return redirect(
            'detalle_compra',
            compra_id=compra.id
        )

    contexto = {
        'compra': compra,
        'detalles': compra.detalles.select_related(
            'producto'
        ).all(),
    }

    return render(
        request,
        'productos/anular_compra.html',
        contexto
    )

def lista_ventas(request):

    ventas = Venta.objects.order_by(
        '-fecha'
    )

    contexto = {
        'ventas': ventas,
    }

    return render(
        request,
        'productos/lista_ventas.html',
        contexto
    )

def crear_venta(request):

    venta = Venta.objects.create(
        estado='BORRADOR'
    )

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

def detalle_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id
    )

    detalles = venta.detalles.select_related(
        'producto'
    ).all()

    productos = Producto.objects.filter(
        activo=True
    ).select_related(
        'categoria'
    ).order_by(
        'categoria__nombre',
        'nombre'
    )

    total = sum(
        detalle.subtotal
        for detalle in detalles
    )

    contexto = {
        'venta': venta,
        'detalles': detalles,
        'productos': productos,
        'total': total,
    }

    return render(
        request,
        'productos/detalle_venta.html',
        contexto
    )

def agregar_producto_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id
    )

    if venta.estado != 'BORRADOR':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    if request.method == 'POST':

        formulario = DetalleVentaForm(
            request.POST
        )

        if formulario.is_valid():

            detalle = formulario.save(
                commit=False
            )

            detalle.venta = venta

            detalle.precio_unitario = (
                detalle.producto.precio
            )

            detalle.save()

            return redirect(
                'detalle_venta',
                venta_id=venta.id
            )

    else:

        formulario = DetalleVentaForm()

    contexto = {
        'venta': venta,
        'formulario': formulario,
    }

    return render(
        request,
        'productos/agregar_producto_venta.html',
        contexto
    )

def agregar_producto_pos(request, venta_id, producto_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    producto = get_object_or_404(
        Producto,
        id=producto_id,
        activo=True
    )

    detalle = DetalleVenta.objects.filter(
        venta=venta,
        producto=producto
    ).first()

    if detalle:

        if detalle.cantidad < producto.stock:

            detalle.cantidad += 1
            detalle.save(
                update_fields=['cantidad']
            )

    else:

        if producto.stock > 0:

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=1,
                precio_unitario=producto.precio
            )

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

def aumentar_producto_venta(request, detalle_id):

    detalle = get_object_or_404(
        DetalleVenta.objects.select_related(
            'venta',
            'producto'
        ),
        id=detalle_id
    )

    if detalle.venta.estado != 'BORRADOR':
        return redirect(
            'detalle_venta',
            venta_id=detalle.venta.id
        )

    if detalle.cantidad < detalle.producto.stock:
        detalle.cantidad += 1
        detalle.save(update_fields=['cantidad'])

    return redirect(
        'detalle_venta',
        venta_id=detalle.venta.id
    )


def disminuir_producto_venta(request, detalle_id):

    detalle = get_object_or_404(
        DetalleVenta.objects.select_related('venta'),
        id=detalle_id
    )

    if detalle.venta.estado != 'BORRADOR':
        return redirect(
            'detalle_venta',
            venta_id=detalle.venta.id
        )

    if detalle.cantidad > 1:

        detalle.cantidad -= 1
        detalle.save(update_fields=['cantidad'])

    else:

        detalle.delete()

    return redirect(
        'detalle_venta',
        venta_id=detalle.venta.id
    )


def eliminar_producto_venta(request, detalle_id):

    detalle = get_object_or_404(
        DetalleVenta.objects.select_related('venta'),
        id=detalle_id
    )

    venta_id = detalle.venta.id

    if detalle.venta.estado == 'BORRADOR':
        detalle.delete()

    return redirect(
        'detalle_venta',
        venta_id=venta_id
    )