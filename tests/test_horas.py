import pytest
from faker import Faker
from ddf import G
from custom_faker_providers import nombre_tipo_loteria_class 
from LoteriaApp.models import tipo_de_loteria_jugada

#pytest -rP imprime los datos 

fake = Faker()
#ASI AGREGO UN FAKE QUE YO MISMO CREE
fake.add_provider(nombre_tipo_loteria_class)

#este decorador me permite hacer la transaccion con la base de datos
@pytest.mark.django_db
def test_horas_creacion():
    
    hora = tipo_de_loteria_jugada.objects.create(
        nombre_tipo_loteria = "prueba_test_nombre" ,
        codigo_tipo_loteria = "code_cance1"
    )

    """
        In simpler terms, we can say that assertion is the boolean expression that
         checks if the statement is True or False. If the statement is true then it
          does nothing and continues the execution, but if the
         statement is False then it stops the execution of the program and throws an error.
    """

    assert hora.nombre_tipo_loteria =="prueba_test_nombre"




# @pytest.mark.django_db
# def test_horas_error():
#     with pytest.raises(Exception):
#         tipo_de_loteria_jugada.objects.create(
#          nombre_tipo_loteria = "prueba_test_nombre", 
#          codigo_tipo_loteria = "code_cance1"
#      )
    
 
@pytest.fixture
def test_horas_creacion_envio_funcion():
    #crea una instancia 
    return G(tipo_de_loteria_jugada)
 

@pytest.mark.django_db
def test_recibo_function(test_horas_creacion_envio_funcion):
    print(test_horas_creacion_envio_funcion.codigo_tipo_loteria)
   
    assert test_horas_creacion_envio_funcion.nombre_tipo_loteria == "1"

    
