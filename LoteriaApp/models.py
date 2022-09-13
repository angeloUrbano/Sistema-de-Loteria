from django.db import models

# Create your models here.



class Animalito(models.Model):
    nombre_animalito = models.CharField(max_length=250 , null=False, blank= False )
    codigo_animalito = models.CharField(max_length=250 , null=False, blank= False )

    def __str__(self):
        return self.nombre_animalito


class Loteria(models.Model):



    hora_jugada = models.TimeField(null=False, blank=False )
    monto_jugada = models.DecimalField(default=0.00 , max_digits=12 , decimal_places=3 , null=False, blank= False )
    codigo_jugada = models.CharField(max_length=250 , null=False, blank= False )
    relacion_animalito = models.ManyToManyField(Animalito)
