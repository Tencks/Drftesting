from rest_framework import serializers
from .models import Residente, StockMedicamentosResidente, ObservaciónSemanal, User, StockMedicamentosLocal, LocalArmonia, CuracionesResidente

from django.db.models import Q # for queries
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
from drf_extra_fields.fields import Base64ImageField




#EL MAQUINADO DE USERS
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=50)

    fotoUser = Base64ImageField(required=False)
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'cargo',
            'fotoUser',
            'descriptionUser',
            'numCelular',
            'direccion',
            'birthday',
            'id'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = User.objects.filter(
                Q(email=user_id) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=user_id)
        else:
            user = User.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=user_id)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()

        data['cargo'] = user.cargo
        user.cargo = data['cargo']
        user.save()

        data['id'] = user.id
        user.id = data['id']
        user.save()
       

        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token',
            'cargo',
            'id'
        )

        read_only_fields = (
            'token',
            'cargo',
            'id'
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )



#RESIDENTES

class ResidenteSerializer(serializers.ModelSerializer):
    fotoResidente = Base64ImageField(required=False)
    class Meta:
        model = Residente
        fields = (
            'id','nombreResidente','apellidoResidente','dniResidente','fechaNacimiento','edad',
            'genero','medicoDeCabecera','grupoSanguineo','numeroDeHabitacion','observacionesResidente',
            'localidadFamiliar','domicilioFamiliar','nombreFamiliar','apellidoFamiliar','numeroTelefonico',
            'dniFamiliar','numeroAfiliado','obraSocial','vinculoConElResidente','fotoResidente','egresado'
            )


class ObservacionSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservaciónSemanal
        fields = (
            'residenteS','tensionArterial','glucemia','saturacion','pulso',
            'observacionesSemanales','fechaConsulta'
        )
        
        
class StockMedicamentosResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosResidente
        fields = (
                'id','residenteM','genericMedicamento','nombreMedicamento','marcaMedicamento',
                'pesoMedicamento','medicionMedicamento',
                'codMedicamento','observacionesMedicamento',
                'fechaInicio','cantidadTotal','cantidadDiaria','cantidadDisponible'
                  )
        

class MedicationStatusSerializer(serializers.Serializer):
    lowMedication = serializers.BooleanField()
    lessThanAWeek = serializers.BooleanField()
    medicamento = serializers.CharField()
    residente = serializers.CharField()
    fechaAgotamiento = serializers.DateField()
    today = serializers.DateField()

    class Meta:
        fields = (
            'lowMedication', 'lessThanAWeek','medicamento','residente','fechaAgotamiento','today'
                  
                  )  # Lista de campos a incluir en la respuesta
    
        

class CuracionesResidentesSerializer(serializers.ModelSerializer):  
    class Meta:
        model=CuracionesResidente
        fields = (
            'residenteC','fechaRealizada','profesional','practicaAplicada'
        )




class LocalArmoniaSerializer(serializers.ModelSerializer):
    foto = Base64ImageField(required=False)
    class Meta:
        model = LocalArmonia
        fields = (
            'nombre','foto','localidad','domicilio',
            'habilitacionProvincial','habilitacionMunicipal','numeroTelefonico','id'
        )




class StockMedicamentosLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosLocal
        fields = (
                'id','localA','genericMedicamento','nombreMedicamento','marcaMedicamento',
                'pesoMedicamento','medicionMedicamento',
                'codMedicamento','observacionesMedicamento',
                'fechaInicio','cantidadTotal','cantidadDiaria','cantidadDisponible'
                  )
        
class MedicationArmoniaStatusSerializer(serializers.Serializer):
    lowMedication = serializers.BooleanField()
    lessThanAWeek = serializers.BooleanField()
    medicamento = serializers.CharField()
    local = serializers.CharField()
    fechaAgotamiento = serializers.DateField()
    today = serializers.DateField()

    class Meta:
        fields = (
            'lowMedication', 'lessThanAWeek','medicamento','local','fechaAgotamiento','today'
                  
                  )  # Lista de campos a incluir en la respuesta
 
