from django import forms
from .models import Producto


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