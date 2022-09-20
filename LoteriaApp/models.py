from django.db import models

# Create your models here.



class Animalito(models.Model):
    nombre_animalito = models.CharField(max_length=250 , null=False, blank= False )
    codigo_animalito = models.CharField(max_length=250 , null=False, blank= False )

    def __str__(self):
        return self.nombre_animalito



class tipo_de_loteria_jugada(models.Model):

    nombre_tipo_loteria = models.CharField(max_length=150, null=False , blank=False)
    codigo_tipo_loteria= models.CharField(max_length=250 , null=False, blank= False )
    def __str__(self):
        return self.nombre_tipo_loteria


class Loteria(models.Model):



    hora_jugada = models.TimeField(null=False, blank=False )
    monto_jugada = models.DecimalField(max_digits=12 , decimal_places=2 , null=False, blank= False)
    codigo_jugada = models.CharField(max_length=250 , null=False, blank= False )
    creado = models.DateField(auto_now=True)
    relacion_animalito = models.ManyToManyField(Animalito)
    tipo_loteria_relacion = models.ForeignKey(tipo_de_loteria_jugada(),  blank=False, null=False, on_delete=models.CASCADE)





