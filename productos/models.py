from django.db import models
from django.conf import settings

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

"""class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre"""

class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )

    codigo = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    nombre = models.CharField(max_length=150)

    presentacion = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    costo_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    stock_minimo = models.PositiveIntegerField(default=5)

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class MovimientoInventario(models.Model):

    TIPOS_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    MOTIVOS = [
        ('COMPRA', 'Compra'),
        ('VENTA', 'Venta'),
        ('AJUSTE', 'Ajuste de inventario'),
        ('MERMA', 'Merma / Pérdida'),
        ('DEVOLUCION', 'Devolución'),
        ('OTRO', 'Otro'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_MOVIMIENTO
    )

    motivo = models.CharField(
        max_length=20,
        choices=MOTIVOS
    )

    cantidad = models.PositiveIntegerField()

    stock_anterior = models.PositiveIntegerField()

    stock_nuevo = models.PositiveIntegerField()

    observacion = models.TextField(
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.producto.nombre} - {self.tipo} - {self.cantidad}' 

class Proveedor(models.Model):

     nombre = models.CharField(
        max_length=150
    )

     identificacion = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

     telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

     email = models.EmailField(
        blank=True,
        null=True
    )

     direccion = models.TextField(
        blank=True,
        null=True
    )

     activo = models.BooleanField(
        default=True 
    )

     fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

     def __str__(self):
        return self.nombre

class Compra(models.Model):

    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADA', 'Confirmada'),
        ('ANULADA', 'Anulada'),
    ]

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='compras'
    )

    numero_documento = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='BORRADOR'
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Compra #{self.id} - {self.proveedor.nombre}'

class DetalleCompra(models.Model):

    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_compra'
    )

    cantidad = models.PositiveIntegerField()

    costo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.compra_id} - {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.costo_unitario

###############################################################################

class Venta(models.Model):

    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADA', 'Confirmada'),
        ('ANULADA', 'Anulada'),
    ]

    cliente = models.ForeignKey(
    'Cliente',
    on_delete=models.PROTECT,
    related_name='ventas',
    blank=True,
    null=True
    )

    usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='ventas_realizadas',
    blank=True,
    null=True
    )

    caja = models.ForeignKey(
    'CajaSesion',
    on_delete=models.PROTECT,
    related_name='ventas',
    blank=True,
    null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='BORRADOR'
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Venta #{self.id}'

##############################################################################

class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_venta'
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.venta_id} - {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

##############################################################################

class Cliente(models.Model):

    TIPOS_IDENTIFICACION = [
        ('CEDULA', 'Cédula'),
        ('RUC', 'RUC'),
        ('PASAPORTE', 'Pasaporte'),
        ('CONSUMIDOR_FINAL', 'Consumidor final'),
    ]

    tipo_identificacion = models.CharField(
        max_length=20,
        choices=TIPOS_IDENTIFICACION,
        default='CEDULA'
    )

    identificacion = models.CharField(
        max_length=20,
        unique=True
    )

    nombre = models.CharField(
        max_length=200
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    direccion = models.TextField(
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.identificacion} - {self.nombre}'



# PAGO VENTA

class PagoVenta(models.Model):

    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
    ]

    ESTADOS = [
        ('REGISTRADO', 'Registrado'),
        ('ANULADO', 'Anulado'),
]

    venta = models.ForeignKey(
        Venta,
        on_delete=models.PROTECT,
        related_name='pagos'
    )

    metodo = models.CharField(
        max_length=20,
        choices=METODOS_PAGO
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    monto_recibido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    cambio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    estado = models.CharField(
    max_length=15,
    choices=ESTADOS,
    default='REGISTRADO'
)

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Pago venta #{self.venta_id} - {self.metodo} - ${self.monto}'

# DATOS DEL NEGOCIO

class ConfiguracionNegocio(models.Model):

    nombre_comercial = models.CharField(
        max_length=200
    )

    razon_social = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    ruc = models.CharField(
        max_length=13,
        blank=True,
        null=True
    )

    direccion = models.TextField(
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    logo = models.ImageField(
    upload_to='negocio/',
    blank=True,
    null=True
)

    mensaje_comprobante = models.CharField(
        max_length=250,
        default='¡Gracias por su compra!'
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nombre_comercial

    ######################CAJA SESION#####################################

class CajaSesion(models.Model):

    ESTADOS = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
    ]

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='ABIERTA'
    )

    fecha_apertura = models.DateTimeField(
        auto_now_add=True
    )

    saldo_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    abierta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cajas_abiertas'
    )

    fecha_cierre = models.DateTimeField(
        blank=True,
        null=True
    )

    cerrada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cajas_cerradas',
        blank=True,
        null=True
    )

    efectivo_esperado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    efectivo_contado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    diferencia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return (
            f'Caja #{self.id} - '
            f'{self.get_estado_display()}'
        )

###########################MOVIMIENTO CAJA###############################

class MovimientoCaja(models.Model):

    TIPOS = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    CONCEPTOS = [
        ('INGRESO_MANUAL', 'Ingreso manual'),
        ('RETIRO', 'Retiro de efectivo'),
        ('GASTO', 'Gasto'),
        ('OTRO', 'Otro'),
    ]

    caja = models.ForeignKey(
        CajaSesion,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    concepto = models.CharField(
        max_length=20,
        choices=CONCEPTOS
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos_caja'
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'Caja #{self.caja_id} - '
            f'{self.get_tipo_display()} - '
            f'${self.monto}'
        )