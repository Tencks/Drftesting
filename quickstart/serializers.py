from rest_framework import serializers
from .models import project, Residente, StockMedicamentosResidente, ObservaciónSemanal

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ('id','title','description','technology','created_at')
        

class ResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residente
        fields = (
            'id','nombreResidente','apellidoResidente','dniResidente','fechaNacimiento','edad',
            'genero','medicoDeCabecera','grupoSanguineo','numeroDeHabitacion','observacionesResidente',
            'localidadFamiliar','domicilioFamiliar','nombreFamiliar','apellidoFamiliar','numeroTelefonico',
            'dniFamiliar','numeroAfiliado','obraSocial','vinculoConElResidente'
            )

class StockMedicamentosResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosResidente
        fields = (
                'id','residenteM','genericMedicamento','nombreMedicamento','marcaMedicamento',
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