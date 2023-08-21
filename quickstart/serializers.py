from rest_framework import serializers
from .models import project, Residente, StockMedicamentosResidente, ObservaciónSemanal, Users, StockMedicamentosLocal

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ('id','title','description','technology','created_at')

class UsersRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id','usuario','password','email','cargo')
        
class UsersLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('usuario','password')
        

class ResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residente
        fields = (
            'id','nombreResidente','apellidoResidente','dniResidente','fechaNacimiento','edad',
            'genero','medicoDeCabecera','grupoSanguineo','numeroDeHabitacion','observacionesResidente',
            'localidadFamiliar','domicilioFamiliar','nombreFamiliar','apellidoFamiliar','numeroTelefonico',
            'dniFamiliar','numeroAfiliado','obraSocial','vinculoConElResidente'
            )

class StockMedicamentosLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosLocal
        fields = (
                'id','genericMedicamento','nombreMedicamento','marcaMedicamento',
                'pesoMedicamento','cantDisponible','medicionMedicamento',
                'fechaIngreso','codMedicamento','observacionesMedicamento','derivacionesMedicamento'
                  )

class ObservacionSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservaciónSemanal
        fields = (
            'residenteS','tensionArterial','glucemia','saturacion','pulso',
            'observacionesSemanales','derivacionesSemanales','fechaConsulta'
        )
        
        
class StockMedicamentosResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosResidente
        fields = (
                'id','residenteM','genericMedicamento','nombreMedicamento','marcaMedicamento',
                'pesoMedicamento','cantDisponible','medicionMedicamento',
                'fechaIngreso','codMedicamento','observacionesMedicamento','derivacionesMedicamento'
                  )