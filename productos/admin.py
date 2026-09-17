from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo', 'fecha_creacion')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'codigo',
        'nombre',
        'presentacion',
        'categoria',
        'costo_compra',
        'precio',
        'stock',
        'stock_minimo',
        'activo'
    )

    search_fields = (
        'codigo',
        'nombre',
        'presentacion',
    )

    list_filter = (
        'categoria',
        'activo',
    )