from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('nuevo/', views.crear_producto, name='crear_producto'),
    path(
    'editar/<int:producto_id>/',
    views.editar_producto,
    name='editar_producto'
    ),

    path(
    'desactivar/<int:producto_id>/',
    views.desactivar_producto,
    name='desactivar_producto'
    ),

    path(
    'reactivar/<int:producto_id>/',
    views.reactivar_producto,
    name='reactivar_producto'
),

path(
    'categorias/',
    views.lista_categorias,
    name='lista_categorias'
),

path(
    'categorias/nueva/',
    views.crear_categoria,
    name='crear_categoria'
),

path(
    'categorias/editar/<int:categoria_id>/',
    views.editar_categoria,
    name='editar_categoria'
),

path(
    'categorias/desactivar/<int:categoria_id>/',
    views.desactivar_categoria,
    name='desactivar_categoria'
),

path(
    'categorias/reactivar/<int:categoria_id>/',
    views.reactivar_categoria,
    name='reactivar_categoria'
),

path(
    'inventario/',
    views.inventario,
    name='inventario'
),

path(
    'inventario/movimiento/<int:producto_id>/',
    views.registrar_movimiento,
    name='registrar_movimiento'
),

path(
    'inventario/historial/',
    views.historial_inventario,
    name='historial_inventario'
),

path(
    'proveedores/',
    views.lista_proveedores,
    name='lista_proveedores'
),

path(
    'proveedores/nuevo/',
    views.crear_proveedor,
    name='crear_proveedor'
),

path(
    'proveedores/editar/<int:proveedor_id>/',
    views.editar_proveedor,
    name='editar_proveedor'
),

path(
    'proveedores/desactivar/<int:proveedor_id>/',
    views.desactivar_proveedor,
    name='desactivar_proveedor'
),

path(
    'proveedores/reactivar/<int:proveedor_id>/',
    views.reactivar_proveedor,
    name='reactivar_proveedor'
),

path(
    'compras/',
    views.lista_compras,
    name='lista_compras'
),

path(
    'compras/nueva/',
    views.crear_compra,
    name='crear_compra'
),

path(
    'compras/<int:compra_id>/',
    views.detalle_compra,
    name='detalle_compra'
),

path(
    'compras/<int:compra_id>/agregar-producto/',
    views.agregar_producto_compra,
    name='agregar_producto_compra'
),

path(
    'compras/detalle/<int:detalle_id>/editar/',
    views.editar_detalle_compra,
    name='editar_detalle_compra'
),

path(
    'compras/detalle/<int:detalle_id>/eliminar/',
    views.eliminar_detalle_compra,
    name='eliminar_detalle_compra'
),

path(
    'compras/<int:compra_id>/confirmar/',
    views.confirmar_compra,
    name='confirmar_compra'
),

path(
    'compras/<int:compra_id>/anular/',
    views.anular_compra,
    name='anular_compra'
),

path(
    'ventas/',
    views.lista_ventas,
    name='lista_ventas'
),

path(
    'ventas/nueva/',
    views.crear_venta,
    name='crear_venta'
),

path(
    'ventas/<int:venta_id>/',
    views.detalle_venta,
    name='detalle_venta'
),

path(
    'ventas/<int:venta_id>/agregar-producto/',
    views.agregar_producto_venta,
    name='agregar_producto_venta'
),

path(
    'ventas/<int:venta_id>/producto/<int:producto_id>/agregar/',
    views.agregar_producto_pos,
    name='agregar_producto_pos'
),

path(
    'ventas/detalle/<int:detalle_id>/aumentar/',
    views.aumentar_producto_venta,
    name='aumentar_producto_venta'
),

path(
    'ventas/detalle/<int:detalle_id>/disminuir/',
    views.disminuir_producto_venta,
    name='disminuir_producto_venta'
),

path(
    'ventas/detalle/<int:detalle_id>/eliminar/',
    views.eliminar_producto_venta,
    name='eliminar_producto_venta'
),
    ]