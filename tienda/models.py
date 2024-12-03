from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    direccion = models.CharField(max_length=100)
    teléfono = models.CharField(max_length=20)
    RFC = models.CharField(max_length=13)

    def save(self, *args, **kwargs):
        self.username = (self.first_name[:3] + self.last_name[:3] + self.teléfono[-3:]).lower()
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    pass

class Vehículo(models.Model):
    marca = models.CharField(max_length=30, null=False)
    modelo = models.CharField(max_length=30, null=False)
    año = models.CharField(max_length=4, null=False)
    tipoTransmision = (
        ('a','Automático'),
        ('m','Manual'),
        ('','Sin definir')
    )
    transmision = models.CharField(max_length=1, null=True, blank=True, choices=tipoTransmision, default='')
    tipoCombustible = (
        ('gas','Gasolina'),
        ('diesel','Diesel'),
        ('electricity','Eléctrico'),
        ('','Sin definir')
    )
    combustible = models.CharField(max_length=11, null=True, blank=True, choices=tipoCombustible, default='')
    tipoTraccion = (
        ('fwd','Delantera'),
        ('rwd','Trasera'),
        ('4wd','4x4'),
        ('','Sin definir')
    )
    traccion = models.CharField(max_length=3, null=True, blank=True, choices=tipoTraccion, default='')
    cilindros = models.IntegerField(null=True, blank=True)
    precioLista = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    interesAnual = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    interesMensual = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    fotoLateral = models.ImageField(default='acura.png', upload_to='autosTresCuartos/')


class Plan(models.Model):
    mensualidades = models.DecimalField(max_digits=10, decimal_places=2)
    plazo = models.IntegerField()
    montoAFinanciar = models.DecimalField(max_digits=10, decimal_places=2)
    pagoInicial = models.DecimalField(max_digits=10, decimal_places=2)
    seguroContado = models.DecimalField(max_digits=10, decimal_places=2)
    tazaInteres = models.DecimalField(max_digits=5,decimal_places=2,default=8.00)
    comisionApertura = models.DecimalField(max_digits=10,decimal_places=2,default=15000.00)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehículo = models.ForeignKey(Vehículo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.usuario.first_name} - {self.vehículo.marca} {self.vehículo.modelo}"

class Promociones(models.Model):
    descuento = models.IntegerField()
    vehículo = models.ForeignKey(Vehículo, on_delete=models.CASCADE)