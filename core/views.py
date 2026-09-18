from django.shortcuts import render
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from productos.models import Producto


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

    contexto = {
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'valor_inventario': valor_inventario,
    }

    return render(
        request,
        'core/dashboard.html',
        contexto
    )