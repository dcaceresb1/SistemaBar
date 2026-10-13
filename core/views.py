from django.shortcuts import render
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.utils import timezone
from productos.models import Producto, DetalleVenta
from core.decorators import roles_permitidos


@roles_permitidos(
    'Administrador',
    'Cajero',
    'Inventario'
)
def dashboard(request):

    total_productos = Producto.objects.filter(
        activo=True
    ).count()

    productos_stock_bajo = Producto.objects.filter(
        activo=True,
        stock__lte=F('stock_minimo')
    ).count()

    valor_inventario = Producto.objects.filter(
        activo=True
    ).aggregate(
        total=Sum(
            ExpressionWrapper(
                F('costo_compra') * F('stock'),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2
                )
            )
        )
    )['total'] or 0

    # =========================
    # VENTAS DEL DÍA
    # =========================

    hoy = timezone.localdate()

    ventas_dia = DetalleVenta.objects.filter(
        venta__estado='CONFIRMADA',
        venta__fecha__date=hoy
    ).aggregate(
        total=Sum(
            ExpressionWrapper(
                F('cantidad') * F('precio_unitario'),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2
                )
            )
        )
    )['total'] or 0

    contexto = {
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'valor_inventario': valor_inventario,
        'ventas_dia': ventas_dia,
    }

    return render(
        request,
        'core/dashboard.html',
        contexto
    )