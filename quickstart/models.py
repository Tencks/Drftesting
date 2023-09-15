from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


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

GRUPOSANGUINEO = (
  ('0', 'A+'),
  ('1', 'O+'),
  ('2', 'B+'),
  ('3', 'AB+'),
  ('4', 'A-'),
  ('5', 'O-'),
  ('6', 'B-'),
  ('7', 'AB-'),
)


CARGO = (
     ('0','invitado'),
     ('1','Empleado diario'),
     ('2','Enfermero/a'),
     ('3','Medico/a'),
     ('4','Admin'),
)


  
#DATOS DE CADA USUARIO DEL SISTEMA
class User(models.Model):
    id =  models.BigAutoField(auto_created=True, primary_key=True,  verbose_name='ID')
    username = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=50, null=False)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=200, default="", null=True)
    cargo = models.CharField(max_length=1, choices=CARGO)

    fotoUser = models.ImageField(upload_to='usersFoto/', blank=True, default='')
    descriptionUser = models.TextField(max_length=400, blank=True, default='',null=True)
    numCelular = models.CharField(max_length=40,null=True,blank=True,default='')
    direccion = models.CharField(max_length=100, null=True,blank=True)
    birthday = models.DateField(default=None,null=True)


    def __str__(self):
        return "{} -{}".format(self.username, self.email)

   
#TABLA PARA LAS NOTIFICACIONES DE MEDICAMENTOS
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario al que se enviará la notificación
    mensaje = models.CharField(max_length=255)  # Mensaje de la notificación
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la notificación
    leida = models.BooleanField(default=False)  # Indica si la notificación ha sido leída o no

    def __str__(self):
        return self.mensaje



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
    grupoSanguineo = models.CharField(max_length=1 ,choices=GRUPOSANGUINEO)
    numeroDeHabitacion = models.CharField(max_length=40)
    observacionesResidente = models.TextField( default='SOME STRING', blank=True, null=True)
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
        medicionMedicamento = models.CharField(max_length=1, choices=TIPOMEDICAMENTO)
        
        codMedicamento = models.CharField(max_length=50)
        observacionesMedicamento = models.TextField(blank=True, null=True,default='SOME STRING')
        derivacionesMedicamento = models.TextField(blank=True, null=True,default='SOME STRING')
        
        fechaInicio = models.DateField()
        cantidadTotal = models.IntegerField()
        cantidadDiaria = models.IntegerField()
        cantidadDisponible = models.IntegerField(blank=True,null=True)

    # METODO USADO PARA EL CALUCULO AUTOMATICO DE LAS UNIDADES RESTANTES

        def calcular_cantidad_disponible(self):
                # Calcular la cantidad disponible en función de la cantidad total y la cantidad diaria
                dias_pasados = (datetime.now().date() - self.fechaInicio).days
                if dias_pasados >= 0:
                    cantidad_disponible = self.cantidadTotal - (dias_pasados * self.cantidadDiaria)
                    if cantidad_disponible < 0:
                        cantidad_disponible = 0
                else:
                    # Si la fecha de inicio es en el futuro, no se ha consumido nada todavía
                    cantidad_disponible = self.cantidadTotal

                return cantidad_disponible

        def save(self, *args, **kwargs):
                # Antes de guardar, calcular la cantidad disponible
                self.cantidadDisponible = self.calcular_cantidad_disponible()
                super().save(*args, **kwargs)







        def __str__(self):
             return f'{self.nombreMedicamento} para {self.residenteM.nombreResidente}'
        
class ObservaciónSemanal (models.Model):
     residenteS = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='signosVitales')
     fechaConsulta = models.DateField(auto_now_add=True)
     tensionArterial = models.CharField(max_length=20)
     glucemia = models.CharField(max_length=20)
     saturacion = models.CharField(max_length=20)
     pulso = models.CharField(max_length=30)
     observacionesSemanales = models.TextField(default='some string', blank=True, null=True)
     derivacionesSemanales = models.TextField(default='some string2', blank=True, null=True)


class CuracionesResidente (models.Model):
     residenteC = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='curaciones')
     fechaRealizada = models.DateField(auto_now_add=True)
     medicacionAplicada = models.CharField(max_length=60)
     profesional = models.CharField(max_length=40)






class LocalArmonia (models.Model):
    nombre = models.CharField(max_length=40)
    foto = models.ImageField(upload_to='localFoto/', blank='', default='')
    localidad = models.CharField(max_length=60,null=True )
    domicilio = models.CharField(max_length=60,null=True )
    cuil = models.CharField(null=True, unique=True,max_length=40)
    fechaCreacion = models.DateField(default=None, blank='',null=True)
    numeroTelefonico = models.CharField(max_length=40,null=True)
    
    

    def __str__(self):
         return self.nombre
    def __repr__(self):
         return f'Model  LocalArmonia: (self.nombre)'





class StockMedicamentosLocal (models.Model):
        localA = models.ForeignKey(LocalArmonia,on_delete=models.CASCADE, related_name='localMedicamentos')
        genericMedicamento = models.CharField(max_length=1, choices=GENERICO)
        nombreMedicamento = models.CharField(max_length=80)
        marcaMedicamento = models.CharField(max_length=60)
        pesoMedicamento = models.CharField(max_length=35)
       
        medicionMedicamento = models.CharField(max_length=1, choices=TIPOMEDICAMENTO)
       
       
        codMedicamento = models.CharField(max_length=50)
        observacionesMedicamento = models.TextField(default='SOME STRING', blank=True, null=True)
        derivacionesMedicamento = models.TextField(default='SOME STRING', blank=True, null=True)

        fechaInicio = models.DateField()
        cantidadTotal = models.IntegerField()
        cantidadDiaria = models.IntegerField()
        cantidadDisponible = models.IntegerField(blank=True,null=True)

    # METODO USADO PARA EL CALUCULO AUTOMATICO DE LAS UNIDADES RESTANTES

        def calcular_cantidad_disponible(self):
                # Calcular la cantidad disponible en función de la cantidad total y la cantidad diaria
                dias_pasados = (datetime.now().date() - self.fechaInicio).days
                if dias_pasados >= 0:
                    cantidad_disponible = self.cantidadTotal - (dias_pasados * self.cantidadDiaria)
                    if cantidad_disponible < 0:
                        cantidad_disponible = 0
                else:
                    # Si la fecha de inicio es en el futuro, no se ha consumido nada todavía
                    cantidad_disponible = self.cantidadTotal

                return cantidad_disponible

        def save(self, *args, **kwargs):
                # Antes de guardar, calcular la cantidad disponible
                self.cantidadDisponible = self.calcular_cantidad_disponible()
                super().save(*args, **kwargs)




