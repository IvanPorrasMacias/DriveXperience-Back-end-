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
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    año = models.CharField(max_length=4)
    especificaciones = models.CharField(max_length=200)
    precioLista = models.DecimalField(max_digits=10, decimal_places=2)
    interesAnual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interesMensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fotoLateral = models.ImageField(default='acura.png', upload_to='autosTresCuartos/') 

    def save(self, *args, **kwargs):
        self.interesAnual = (self.precioLista*8)/100
        self.interesMensual = self.interesAnual/12
        super(Vehículo, self).save(*args, **kwargs)

    def __str__(self):
        return self.marca + ' - ' + self.modelo


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