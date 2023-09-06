from django.db import models


GENERO = (
    ('0','Masculino'),
    ('1','Femenino'),
    ('2','No responder')
)

VINCULO = (
    ('0','Padre'),
    ('1','Madre'),
    ('2','Hijo'),
    ('3','Hija'),
    ('4','Abuelo'),
    ('5','Abuela'),
    ('6','Tío'),
    ('7','Tía'),
    ('8','Pariente lejano'),
    ('9','Prefiero no responder'),
)

GENERICO = (
    ('Y', 'Si'),
    ('N', 'No'),
)

TIPOMEDICAMENTO = (
    ('0','ml'),
    ('1','g'),
    ('2','píldora/as'),
    ('3','caja/as'),
    ('4','frasco/os'),

)

CARGO = (
     ('0','invitado'),
     ('1','Medico/a'),
     ('2','Enfermero/a'),
     ('3','Empleado diario'),
     ('4','Admin'),
)
  
#DATOS DE CADA USUARIO DEL SISTEMA
class User(models.Model):
    username = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=50, null=False)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=200, default="", null=True)
    cargo = models.CharField(max_length=1, choices=CARGO)


    def __str__(self):
        return "{} -{}".format(self.username, self.email)

   

#DATOS DE CADA RESIDENTE

class Residente (models.Model):
    nombreResidente = models.CharField(max_length=40)
    apellidoResidente = models.CharField(max_length=40)
    dniResidente = models.CharField(null=False, unique=True,max_length=8)
    fechaNacimiento = models.DateField(default=None)
    edad = models.IntegerField(default='Edad del residente')
    genero = models.CharField(max_length=1, choices=GENERO)
    fotoResidente = models.ImageField(upload_to='residentesFoto/', blank='', default='')
    medicoDeCabecera = models.CharField(max_length=40)
    grupoSanguineo = models.CharField(max_length=40, default='Sangre')
    numeroDeHabitacion = models.CharField(max_length=40)
    observacionesResidente = models.TextField(blank=False, default='SOME STRING')
    localidadFamiliar = models.CharField(max_length=60, default='Localidad')
    domicilioFamiliar = models.CharField(max_length=60, default='Domicilio')
    nombreFamiliar = models.CharField(max_length=40)
    apellidoFamiliar = models.CharField(max_length=40)
    numeroTelefonico = models.CharField(max_length=40)
    dniFamiliar = models.CharField(null=False, unique=True,max_length=8, default='Dni familiar')
    numeroAfiliado = models.IntegerField(null=False, unique=True)
    obraSocial = models.CharField(max_length=40)
    vinculoConElResidente = models.CharField(max_length=1 ,choices=VINCULO)

    def __str__(self):
         return self.nombreResidente
    def __repr__(self):
         return f'Model  Residente: (self.nombreResidente)'


class StockMedicamentosResidente (models.Model):
        residenteM = models.ForeignKey(Residente,on_delete=models.CASCADE, related_name='medicamentos')
        genericMedicamento = models.CharField(max_length=1, choices=GENERICO)
        nombreMedicamento = models.CharField(max_length=80)
        marcaMedicamento = models.CharField(max_length=60)
        pesoMedicamento = models.CharField(max_length=35)
        cantDisponible = models.IntegerField()
        medicionMedicamento = models.CharField(max_length=1, choices=TIPOMEDICAMENTO)
        fechaIngreso = models.DateField(default=None)
        fechaCaducidad = models.DateField(default=None)
        codMedicamento = models.CharField(max_length=50)
        observacionesMedicamento = models.TextField(blank=False,default='SOME STRING')
        derivacionesMedicamento = models.TextField(blank=False,default='SOME STRING')

        def __str__(self):
             return f'{self.nombreMedicamento} para {self.residenteM.nombreResidente}'
        
class ObservaciónSemanal (models.Model):
     residenteS = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='signosVitales')
     fechaConsulta = models.DateField(auto_now_add=True)
     tensionArterial = models.CharField(max_length=20)
     glucemia = models.CharField(max_length=20)
     saturacion = models.CharField(max_length=20)
     pulso = models.CharField(max_length=30)
     observacionesSemanales = models.TextField(default='some string')
     derivacionesSemanales = models.TextField(default='some string2')



class StockMedicamentosLocal (models.Model):
        genericMedicamento = models.CharField(max_length=1, choices=GENERICO)
        nombreMedicamento = models.CharField(max_length=80)
        marcaMedicamento = models.CharField(max_length=60)
        pesoMedicamento = models.CharField(max_length=35)
        cantDisponible = models.IntegerField()
        medicionMedicamento = models.CharField(max_length=1, choices=TIPOMEDICAMENTO)
        fechaIngreso = models.DateField(default=None)
        fechaCaducidad = models.DateField(default=None)
        codMedicamento = models.CharField(max_length=50)
        observacionesMedicamento = models.TextField(blank=False,default='SOME STRING')
        derivacionesMedicamento = models.TextField(blank=False,default='SOME STRING')
