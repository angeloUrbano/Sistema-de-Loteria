from django.db import models

# Create your models here.



class Animalito(models.Model):
    nombre_animalito = models.CharField(max_length=250 , null=False, blank= False )
    codigo_animalito = models.CharField(max_length=250 , null=False, blank= False )

    def __str__(self):
        return self.nombre_animalito



class tipo_de_loteria_jugada(models.Model):

    nombre_tipo_loteria = models.CharField(max_length=150, null=False , blank=False)
    codigo_tipo_loteria= models.CharField(max_length=250 , null=False, blank= False , unique=True )
    def __str__(self):
        return self.nombre_tipo_loteria

class hora_jugada_model(models.Model):

    hora_en_nombre = models.CharField(max_length=150, null=False , blank=False)

    def __str__(self):
        return self.hora_en_nombre



class Loteria(models.Model):

    monto_jugada = models.DecimalField(max_digits=12 , decimal_places=2 , null=False, blank= False)
    creado = models.DateField(auto_now_add=True)
    procesado = models.BooleanField(default=False)
    relacion_animalito = models.ManyToManyField(Animalito)
    tipo_loteria_relacion =  models.ManyToManyField(tipo_de_loteria_jugada )
    hora_relacion = models.ManyToManyField(hora_jugada_model)
   



class venta_procesada(models.Model):

    relacion_model_loteria = models.ManyToManyField(Loteria)
    codigo_jugada = models.CharField(max_length=250 , null=False, blank= False )
    creado = models.DateField(auto_now_add=True)
    monto_final_jugadas= models.DecimalField(max_digits=12 , decimal_places=2 , null=False, blank= False)
    pago_realizado = models.BooleanField(default=True) 
    hora = models.CharField(max_length=250 , null=False, blank= False )



class monto_divisa(models.Model):

    monto_en_dolares =  models.DecimalField(max_digits=12 , decimal_places=2 , null=False, blank= False)

    def __str__(self):
        return str(self.monto_en_dolares)






