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
    Cliente,
    PagoVenta,
    ConfiguracionNegocio,
    CajaSesion,
    MovimientoCaja,
    
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
    ClienteForm,
    ConfiguracionNegocioForm,

)

from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from decimal import Decimal, InvalidOperation
from core.decorators import roles_permitidos
from django.db.models import Sum
from django.utils import timezone

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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


@roles_permitidos('Administrador', 'Inventario')
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


@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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


@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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


@roles_permitidos('Administrador', 'Inventario')
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


@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Inventario')
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

@roles_permitidos('Administrador', 'Cajero')
def lista_ventas(request):

    ventas = Venta.objects.prefetch_related(
        'detalles'
    ).order_by('-fecha')

    for venta in ventas:
        venta.total_calculado = sum(
            detalle.subtotal
            for detalle in venta.detalles.all()
        )

        venta.cantidad_productos = sum(
            detalle.cantidad
            for detalle in venta.detalles.all()
        )

    contexto = {
        'ventas': ventas,
    }

    return render(
        request,
        'productos/lista_ventas.html',
        contexto
    )
###############################################################################

@roles_permitidos('Administrador', 'Cajero')
def crear_venta(request):

    # Buscar una caja abierta
    caja_abierta = CajaSesion.objects.filter(
        estado='ABIERTA'
    ).first()

    # No permitir ventas si no existe una caja abierta
    if not caja_abierta:
        return redirect('abrir_caja')

    # Obtener o crear Consumidor Final
    consumidor_final, creado = Cliente.objects.get_or_create(
        identificacion='9999999999999',
        defaults={
            'tipo_identificacion': 'CONSUMIDOR_FINAL',
            'nombre': 'CONSUMIDOR FINAL',
            'activo': True,
        }
    )

    # Crear la venta vinculada al usuario y a la caja
    venta = Venta.objects.create(
        estado='BORRADOR',
        cliente=consumidor_final,
        usuario=request.user,
        caja=caja_abierta
    )

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

###################################################################################

@roles_permitidos('Administrador', 'Cajero')
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    detalles = venta.detalles.select_related('producto').all()

    # Valores recibidos desde los filtros del POS
    busqueda = request.GET.get('buscar', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    cliente_no_encontrado = request.GET.get(
    'cliente_no_encontrado',
    ''
    ).strip()

    productos = Producto.objects.filter(
        activo=True
    ).select_related('categoria')

    # Buscar por nombre o código
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda)
        )

    # Filtrar por categoría
    if categoria_id:
        productos = productos.filter(
            categoria_id=categoria_id
        )

    productos = productos.order_by(
        'categoria__nombre',
        'nombre'
    )

    categorias = Categoria.objects.filter(
        activo=True
    ).order_by('nombre')

    total = sum(detalle.subtotal for detalle in detalles)
    pago = venta.pagos.order_by('-fecha').first()

    contexto = {
        'venta': venta,
        'detalles': detalles,
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_id,
        'cliente_no_encontrado': cliente_no_encontrado,
        'total': total,
        'pago': pago,
    }

    return render(
        request,
        'productos/detalle_venta.html',
        contexto
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
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

################################################################################

@roles_permitidos('Administrador', 'Cajero')
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

################################################################################

@roles_permitidos('Administrador', 'Cajero')
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

################################################################################

@roles_permitidos('Administrador', 'Cajero')
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

################################################################################

@roles_permitidos('Administrador', 'Cajero')
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

############## ANULAR VENTA #####################################

@roles_permitidos('Administrador')
@transaction.atomic
def anular_venta(request, venta_id):

    venta = get_object_or_404(
        Venta.objects.select_for_update(),
        id=venta_id,
        estado='CONFIRMADA'
        )

    # La anulación solamente puede realizarse mediante POST
    if request.method != 'POST':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    # Una venta perteneciente a una caja cerrada
    # no puede modificarse retroactivamente.
    if venta.caja and venta.caja.estado == 'CERRADA':
        return render(
            request,
            'productos/venta_no_anulable.html',
            {
                'venta': venta,
                'mensaje': (
                    'No se puede anular esta venta porque '
                    'pertenece a una caja que ya fue cerrada.'
                ),
            }
        )

    detalles = list(
        venta.detalles.all()
    )

    # Obtenemos los productos involucrados
    productos_ids = sorted(
        detalle.producto_id
        for detalle in detalles
    )

    # Bloqueamos los productos mientras actualizamos inventario
    productos_bloqueados = (
        Producto.objects
        .select_for_update()
        .filter(id__in=productos_ids)
        .order_by('id')
    )

    productos = {
        producto.id: producto
        for producto in productos_bloqueados
    }

    # Devolver al inventario los productos vendidos
    for detalle in detalles:

        producto = productos[detalle.producto_id]

        stock_anterior = producto.stock
        stock_nuevo = (
            stock_anterior
            + detalle.cantidad
        )

        producto.stock = stock_nuevo

        producto.save(
            update_fields=['stock']
        )

        MovimientoInventario.objects.create(
            producto=producto,
            tipo='ENTRADA',
            motivo='DEVOLUCION',
            cantidad=detalle.cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            observacion=(
                f'Anulación de venta #{venta.id}'
            )
        )

    # Los pagos no se eliminan.
    # Se conservan como parte del historial,
    # pero quedan marcados como anulados.
    venta.pagos.filter(
        estado='REGISTRADO'
    ).update(
        estado='ANULADO'
    )

    # Finalmente anulamos la venta
    venta.estado = 'ANULADA'

    venta.save(
        update_fields=['estado']
    )

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def cancelar_venta_borrador(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    if request.method != 'POST':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    venta.estado = 'ANULADA'
    venta.save(update_fields=['estado'])

    return redirect('lista_ventas')

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def lista_clientes(request):

    busqueda = request.GET.get('buscar', '').strip()

    clientes = Cliente.objects.all().order_by('nombre')

    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(identificacion__icontains=busqueda)
        )

    contexto = {
        'clientes': clientes,
        'busqueda': busqueda,
    }

    return render(
        request,
        'productos/lista_clientes.html',
        contexto
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def crear_cliente(request):

    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('lista_clientes')

    else:
        form = ClienteForm()

    contexto = {
        'form': form,
    }

    return render(
        request,
        'productos/crear_cliente.html',
        contexto
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def asignar_cliente_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    if request.method != 'POST':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    identificacion = request.POST.get(
        'identificacion',
        ''
    ).strip()

    if not identificacion:
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    cliente = Cliente.objects.filter(
        identificacion=identificacion,
        activo=True
    ).first()

    if cliente:

        venta.cliente = cliente
        venta.save(update_fields=['cliente'])

        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    # Cliente no encontrado
    return redirect(
        f'/productos/ventas/{venta.id}/?cliente_no_encontrado={identificacion}'
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def quitar_cliente_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    if request.method != 'POST':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    venta.cliente = None
    venta.save(update_fields=['cliente'])

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def crear_cliente_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    identificacion = request.GET.get(
        'identificacion',
        ''
    ).strip()

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():

            cliente = form.save()

            venta.cliente = cliente
            venta.save(update_fields=['cliente'])

            return redirect(
                'detalle_venta',
                venta_id=venta.id
            )

    else:

        form = ClienteForm(
            initial={
                'identificacion': identificacion
            }
        )

    contexto = {
        'form': form,
        'venta': venta,
    }

    return render(
        request,
        'productos/crear_cliente_venta.html',
        contexto
    )

################################################################################

@roles_permitidos('Administrador', 'Cajero')
def asignar_consumidor_final(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='BORRADOR'
    )

    if request.method != 'POST':
        return redirect(
            'detalle_venta',
            venta_id=venta.id
        )

    consumidor_final, creado = Cliente.objects.get_or_create(
        identificacion='9999999999999',
        defaults={
            'tipo_identificacion': 'CONSUMIDOR_FINAL',
            'nombre': 'CONSUMIDOR FINAL',
            'activo': True,
        }
    )

    venta.cliente = consumidor_final
    venta.save(update_fields=['cliente'])

    return redirect(
        'detalle_venta',
        venta_id=venta.id
    )

################################################################################

@transaction.atomic
@roles_permitidos('Administrador', 'Cajero')
def cobrar_venta(request, venta_id):

    venta = get_object_or_404(
        Venta.objects.select_for_update(),
        id=venta_id,
        estado='BORRADOR'
    )

    # ==========================================
    # VALIDAR CAJA DE LA VENTA
    # ==========================================

    if not venta.caja_id:
        return render(
            request,
            'productos/venta_no_cobrable.html',
            {
                'venta': venta,
                'mensaje': (
                    'No se puede cobrar esta venta porque '
                    'no está asociada a una caja.'
                ),
            }
        )

    caja = CajaSesion.objects.select_for_update().get(
        id=venta.caja_id
    )

    if caja.estado != 'ABIERTA':
        return render(
            request,
            'productos/venta_no_cobrable.html',
            {
                'venta': venta,
                'mensaje': (
                    'No se puede cobrar esta venta porque '
                    'la caja asociada ya está cerrada.'
                ),
            }
        )

    detalles = list(
            venta.detalles.select_related(
                'producto'
            ).all()
        )

    if not detalles:
            return redirect(
                'detalle_venta',
                venta_id=venta.id
            )

    total = sum(
            detalle.subtotal
            for detalle in detalles

        )

    error = None

    # ==========================================
    # PROCESAR PAGO
    # ==========================================

    if request.method == 'POST':

        metodo_pago = request.POST.get(
            'metodo_pago',
            ''
        )

        monto_recibido_texto = request.POST.get(
            'monto_recibido',
            ''
        ).strip()

        referencia = request.POST.get(
            'referencia',
            ''
        ).strip()

        metodos_validos = [
            'EFECTIVO',
            'TRANSFERENCIA',
            'TARJETA',
        ]

        if metodo_pago not in metodos_validos:

            error = 'Selecciona un método de pago válido.'

        # ======================================
        # VALIDAR EFECTIVO
        # ======================================

        elif metodo_pago == 'EFECTIVO':

            try:

                monto_recibido = Decimal(
                    monto_recibido_texto
                )

                if monto_recibido < total:

                    error = (
                        'El monto recibido es menor '
                        'al total de la venta.'
                    )

            except (InvalidOperation, ValueError):

                error = (
                    'Ingresa un monto recibido válido.'
                )

        else:

            monto_recibido = None

        # ======================================
        # SI NO HAY ERRORES
        # ======================================

        if not error:

            # ----------------------------------
            # BLOQUEAR PRODUCTOS
            # ----------------------------------

            productos_ids = sorted(
                detalle.producto_id
                for detalle in detalles
            )

            productos_bloqueados = (
                Producto.objects
                .select_for_update()
                .filter(id__in=productos_ids)
                .order_by('id')
            )

            productos = {
                producto.id: producto
                for producto in productos_bloqueados
            }

            # ----------------------------------
            # VALIDAR STOCK
            # ----------------------------------

            for detalle in detalles:

                producto = productos[
                    detalle.producto_id
                ]

                if producto.stock < detalle.cantidad:

                    error = (
                        f'Stock insuficiente para '
                        f'{producto.nombre}.'
                    )

                    break

            # ----------------------------------
            # PROCESAR VENTA
            # ----------------------------------

            if not error:

                for detalle in detalles:

                    producto = productos[
                        detalle.producto_id
                    ]

                    stock_anterior = producto.stock

                    stock_nuevo = (
                        stock_anterior -
                        detalle.cantidad
                    )

                    producto.stock = stock_nuevo

                    producto.save(
                        update_fields=['stock']
                    )

                    MovimientoInventario.objects.create(
                        producto=producto,
                        tipo='SALIDA',
                        motivo='VENTA',
                        cantidad=detalle.cantidad,
                        stock_anterior=stock_anterior,
                        stock_nuevo=stock_nuevo,
                        observacion=f'Venta #{venta.id}'
                    )

                # --------------------------------
                # CALCULAR CAMBIO
                # --------------------------------

                if metodo_pago == 'EFECTIVO':

                    cambio = (
                        monto_recibido - total
                    )

                else:

                    cambio = Decimal('0.00')

                # --------------------------------
                # REGISTRAR PAGO
                # --------------------------------

                PagoVenta.objects.create(
                    venta=venta,
                    metodo=metodo_pago,
                    monto=total,
                    monto_recibido=monto_recibido,
                    cambio=cambio,
                    referencia=referencia or None
                )

                # --------------------------------
                # CONFIRMAR VENTA
                # --------------------------------

                venta.estado = 'CONFIRMADA'

                venta.save(
                    update_fields=['estado']
                )

                return redirect(
                    'detalle_venta',
                    venta_id=venta.id
                )

    contexto = {
        'venta': venta,
        'detalles': detalles,
        'total': total,
        'error': error,
    }

    return render(
        request,
        'productos/cobrar_venta.html',
        contexto
    )

# --------------------------------
# COMPROBNANTE DE VENTA
# --------------------------------

@roles_permitidos('Administrador', 'Cajero')
def comprobante_venta(request, venta_id):

    venta = get_object_or_404(
        Venta,
        id=venta_id,
        estado='CONFIRMADA'
    )

    detalles = venta.detalles.select_related(
        'producto'
    ).all()

    pago = venta.pagos.order_by(
        '-fecha'
    ).first()

    total = sum(
        detalle.subtotal
        for detalle in detalles
    )

    configuracion = ConfiguracionNegocio.objects.first()

    contexto = {
        'venta': venta,
        'detalles': detalles,
        'pago': pago,
        'total': total,
        'configuracion': configuracion,
    }

    return render(
        request,
        'productos/comprobante_venta.html',
        contexto
    )

# --------------------------------
# CONFIGURACIÓN DE DATOS DEL NEGOCIO
# --------------------------------

@roles_permitidos('Administrador')
def configuracion_negocio(request):

    configuracion = ConfiguracionNegocio.objects.first()

    if request.method == 'POST':

        form = ConfiguracionNegocioForm(
             request.POST,
            request.FILES,
            instance=configuracion
        )

        if form.is_valid():

            form.save()

            return redirect(
                'configuracion_negocio'
            )

    else:

        form = ConfiguracionNegocioForm(
            instance=configuracion
        )

    contexto = {
        'form': form,
        'configuracion': configuracion,
    }

    return render(
        request,
        'productos/configuracion_negocio.html',
        contexto
    )

# --------------------------------
# CAJA SESION
# --------------------------------

@roles_permitidos('Administrador', 'Cajero')
def abrir_caja(request):

    caja_abierta = CajaSesion.objects.filter(
        estado='ABIERTA'
    ).first()

    # ==========================================
    # SI EXISTE UNA CAJA ABIERTA
    # ==========================================

    if caja_abierta:

        pagos = PagoVenta.objects.filter(
            venta__caja=caja_abierta,
            venta__estado='CONFIRMADA'
        )

        ventas_efectivo = pagos.filter(
            metodo='EFECTIVO'
        ).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')

        ventas_transferencia = pagos.filter(
            metodo='TRANSFERENCIA'
        ).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')

        ventas_tarjeta = pagos.filter(
            metodo='TARJETA'
        ).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')

        total_vendido = (
            ventas_efectivo
            + ventas_transferencia
            + ventas_tarjeta
        )

        ingresos = caja_abierta.movimientos.filter(
            tipo='INGRESO'
        ).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')

        egresos = caja_abierta.movimientos.filter(
            tipo='EGRESO'
        ).aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')

        efectivo_esperado = (
            caja_abierta.saldo_inicial
            + ventas_efectivo
            + ingresos
            - egresos
        )

        return render(
            request,
            'productos/caja_abrir.html',
            {
                'caja_abierta': caja_abierta,
                'ventas_efectivo': ventas_efectivo,
                'ventas_transferencia': ventas_transferencia,
                'ventas_tarjeta': ventas_tarjeta,
                'total_vendido': total_vendido,
                'ingresos': ingresos,
                'egresos': egresos,
                'efectivo_esperado': efectivo_esperado,
            }
        )

    # ==========================================
    # ABRIR UNA NUEVA CAJA
    # ==========================================

    error = None

    if request.method == 'POST':

        saldo_inicial_texto = request.POST.get(
            'saldo_inicial',
            ''
        ).strip()

        observacion = request.POST.get(
            'observacion',
            ''
        ).strip()

        try:
            saldo_inicial = Decimal(
                saldo_inicial_texto
            )

            if saldo_inicial < 0:
                error = (
                    'El saldo inicial no puede ser negativo.'
                )

        except (InvalidOperation, ValueError):
            error = (
                'Ingresa un saldo inicial válido.'
            )

        if not error:

            CajaSesion.objects.create(
                saldo_inicial=saldo_inicial,
                abierta_por=request.user,
                observacion=observacion or None
            )

            return redirect('abrir_caja')

    return render(
        request,
        'productos/caja_abrir.html',
        {
            'error': error,
        }
    )

# ==========================================
# REGISTRAR MOVIMIENTO DE CAJA
# ==========================================


@roles_permitidos('Administrador', 'Cajero')
def registrar_movimiento_caja(request):

    caja_abierta = CajaSesion.objects.filter(
        estado='ABIERTA'
    ).first()

    if not caja_abierta:
        return redirect('abrir_caja')

    error = None

    if request.method == 'POST':

        tipo = request.POST.get(
            'tipo',
            ''
        )

        concepto = request.POST.get(
            'concepto',
            ''
        )

        monto_texto = request.POST.get(
            'monto',
            ''
        ).strip()

        observacion = request.POST.get(
            'observacion',
            ''
        ).strip()

        tipos_validos = [
            'INGRESO',
            'EGRESO',
        ]

        conceptos_validos = [
            'INGRESO_MANUAL',
            'RETIRO',
            'GASTO',
            'OTRO',
        ]

        if tipo not in tipos_validos:

            error = (
                'Selecciona un tipo de movimiento válido.'
            )

        elif concepto not in conceptos_validos:

            error = (
                'Selecciona un concepto válido.'
            )

        elif (
            tipo == 'INGRESO'
            and concepto in ['RETIRO', 'GASTO']
        ):

            error = (
                'ERROR: Un retiro o gasto debe registrarse '
                'como egreso.'
            )

        elif (
            tipo == 'EGRESO'
            and concepto == 'INGRESO_MANUAL'
        ):

            error = (
                'ERROR: Un ingreso manual debe registrarse '
                'como ingreso.'
            )

        else:

            try:

                monto = Decimal(
                    monto_texto
                )

                if monto <= 0:

                    error = (
                        'El monto debe ser mayor que cero.'
                    )

            except (InvalidOperation, ValueError):

                error = (
                    'Ingresa un monto válido.'
                )

        if not error:

            MovimientoCaja.objects.create(
                caja=caja_abierta,
                tipo=tipo,
                concepto=concepto,
                monto=monto,
                usuario=request.user,
                observacion=observacion or None
            )

            return redirect('abrir_caja')

    return render(
        request,
        'productos/caja_movimiento.html',
        {
            'caja_abierta': caja_abierta,
            'error': error,
        }
    )

# ==========================================
# CERRAR CAJA
# ==========================================

@roles_permitidos('Administrador', 'Cajero')
@transaction.atomic
def cerrar_caja(request):

    caja = CajaSesion.objects.select_for_update().filter(
        estado='ABIERTA'
    ).first()

    if not caja:
        return redirect('abrir_caja')

    # ==========================================
    # VENTAS PENDIENTES
    # ==========================================

    ventas_pendientes = caja.ventas.filter(
        estado='BORRADOR'
    ).count()

    # ==========================================
    # VENTAS DE LA CAJA
    # ==========================================

    pagos = PagoVenta.objects.filter(
        venta__caja=caja,
        venta__estado='CONFIRMADA',
        estado='REGISTRADO'
    )

    ventas_efectivo = pagos.filter(
        metodo='EFECTIVO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    ventas_transferencia = pagos.filter(
        metodo='TRANSFERENCIA'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    ventas_tarjeta = pagos.filter(
        metodo='TARJETA'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    total_vendido = (
        ventas_efectivo
        + ventas_transferencia
        + ventas_tarjeta
    )

    # ==========================================
    # MOVIMIENTOS MANUALES
    # ==========================================

    ingresos = caja.movimientos.filter(
        tipo='INGRESO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    egresos = caja.movimientos.filter(
        tipo='EGRESO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    # ==========================================
    # EFECTIVO ESPERADO
    # ==========================================

    efectivo_esperado = (
        caja.saldo_inicial
        + ventas_efectivo
        + ingresos
        - egresos
    )

    error = None

    # ==========================================
    # PROCESAR CIERRE
    # ==========================================

    if request.method == 'POST':

        # No permitir cerrar con ventas pendientes
        if ventas_pendientes > 0:

            error = (
                f'No se puede cerrar la caja porque existen '
                f'{ventas_pendientes} venta(s) en borrador. '
                f'Debes cobrarlas o cancelarlas antes de cerrar.'
            )

        else:

            efectivo_contado_texto = request.POST.get(
                'efectivo_contado',
                ''
            ).strip()

            try:

                efectivo_contado = Decimal(
                    efectivo_contado_texto
                )

                if efectivo_contado < 0:

                    error = (
                        'El efectivo contado no puede ser negativo.'
                    )

            except (InvalidOperation, ValueError):

                error = (
                    'Ingresa un valor válido para el efectivo contado.'
                )

            # ==================================
            # GUARDAR CIERRE
            # ==================================

            if not error:

                diferencia = (
                    efectivo_contado
                    - efectivo_esperado
                )

                caja.efectivo_esperado = efectivo_esperado
                caja.efectivo_contado = efectivo_contado
                caja.diferencia = diferencia
                caja.fecha_cierre = timezone.now()
                caja.cerrada_por = request.user
                caja.estado = 'CERRADA'

                caja.save(
                    update_fields=[
                        'efectivo_esperado',
                        'efectivo_contado',
                        'diferencia',
                        'fecha_cierre',
                        'cerrada_por',
                        'estado',
                    ]
                )

                return redirect('abrir_caja')

    # ==========================================
    # MOSTRAR PANTALLA
    # ==========================================

    return render(
        request,
        'productos/caja_cerrar.html',
        {
            'caja': caja,
            'ventas_efectivo': ventas_efectivo,
            'ventas_transferencia': ventas_transferencia,
            'ventas_tarjeta': ventas_tarjeta,
            'total_vendido': total_vendido,
            'ingresos': ingresos,
            'egresos': egresos,
            'efectivo_esperado': efectivo_esperado,
            'ventas_pendientes': ventas_pendientes,
            'error': error,
        }
    )

    # ==========================================
    # HISTORIAL CAJAS
    # ==========================================

@roles_permitidos('Administrador', 'Cajero')
def historial_cajas(request):

    cajas = CajaSesion.objects.select_related(
        'abierta_por',
        'cerrada_por'
    ).order_by('-fecha_apertura')

    return render(
        request,
        'productos/caja_historial.html',
        {
            'cajas': cajas,
        }
    )

    # ==========================================
    # DETALLE CAJA
    # ==========================================

@roles_permitidos('Administrador', 'Cajero')
def detalle_caja(request, caja_id):

    caja = get_object_or_404(
        CajaSesion.objects.select_related(
            'abierta_por',
            'cerrada_por'
        ),
        id=caja_id
    )

    pagos = PagoVenta.objects.filter(
        venta__caja=caja,
        venta__estado='CONFIRMADA'
    ).select_related(
        'venta',
        'venta__usuario'
    ).order_by('fecha')

    ventas_efectivo = pagos.filter(
        metodo='EFECTIVO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    ventas_transferencia = pagos.filter(
        metodo='TRANSFERENCIA'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    ventas_tarjeta = pagos.filter(
        metodo='TARJETA'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    total_vendido = (
        ventas_efectivo
        + ventas_transferencia
        + ventas_tarjeta
    )

    movimientos = caja.movimientos.select_related(
        'usuario'
    ).order_by('fecha')

    ingresos = movimientos.filter(
        tipo='INGRESO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    egresos = movimientos.filter(
        tipo='EGRESO'
    ).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')

    efectivo_calculado = (
        caja.saldo_inicial
        + ventas_efectivo
        + ingresos
        - egresos
    )

    return render(
        request,
        'productos/caja_detalle.html',
        {
            'caja': caja,
            'pagos': pagos,
            'movimientos': movimientos,
            'ventas_efectivo': ventas_efectivo,
            'ventas_transferencia': ventas_transferencia,
            'ventas_tarjeta': ventas_tarjeta,
            'total_vendido': total_vendido,
            'ingresos': ingresos,
            'egresos': egresos,
            'efectivo_calculado': efectivo_calculado,
        }
    )