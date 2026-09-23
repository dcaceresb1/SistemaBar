from django import forms
from django.db.models import Q
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


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'categoria',
            'codigo',
            'nombre',
            'presentacion',
            'descripcion',
            'costo_compra',
            'precio',
            'stock',
            'stock_minimo',
            'activo',
        ]

        widgets = {
            'descripcion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categorias = Categoria.objects.filter(
            activo=True
        ).order_by('nombre')

        # Al editar un producto, también permitimos mostrar
        # su categoría actual aunque esté inactiva.
        if self.instance and self.instance.pk:

            categorias = Categoria.objects.filter(
                Q(activo=True) |
                Q(pk=self.instance.categoria_id)
            ).order_by('nombre')

        self.fields['categoria'].queryset = categorias


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            'nombre',
            'descripcion',
            'activo',
        ]

        widgets = {
            'descripcion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

class MovimientoInventarioForm(forms.ModelForm):

    class Meta:
        model = MovimientoInventario

        fields = [
            'tipo',
            'motivo',
            'cantidad',
            'observacion',
        ]

        widgets = {
            'observacion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor

        fields = [
            'nombre',
            'identificacion',
            'telefono',
            'email',
            'direccion',
            'activo',
        ]

        widgets = {
            'direccion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra

        fields = [
            'proveedor',
            'numero_documento',
            'observacion',
        ]

        widgets = {
            'observacion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['proveedor'].queryset = Proveedor.objects.filter(
            activo=True
        ).order_by('nombre')

class DetalleCompraForm(forms.ModelForm):

     class Meta:
        model = DetalleCompra

        fields = [
            'producto',
            'cantidad',
            'costo_unitario',
        ]

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = Producto.objects.filter(
            activo=True
        ).order_by('nombre')

        self.fields['cantidad'].widget.attrs.update({
            'min': 1
        })

        self.fields['costo_unitario'].widget.attrs.update({
            'min': 0,
            'step': '0.01'
        })

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta

        fields = [
            'observacion',
        ]

        widgets = {
            'observacion': forms.Textarea(
                attrs={'rows': 3}
            ),
        }


class DetalleVentaForm(forms.ModelForm):

    class Meta:
        model = DetalleVenta

        fields = [
            'producto',
            'cantidad',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = Producto.objects.filter(
            activo=True
        ).order_by('nombre')

        self.fields['cantidad'].widget.attrs.update({
            'min': 1
        })
        