from rest_framework import serializers
from .models import Residente, StockMedicamentosResidente, ObservaciónSemanal, User, StockMedicamentosLocal

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
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'cargo'
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

        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token',
            'cargo'
        )

        read_only_fields = (
            'token',
            'cargo'
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
            'dniFamiliar','numeroAfiliado','obraSocial','vinculoConElResidente','fotoResidente'
            )

class StockMedicamentosLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMedicamentosLocal
        fields = (
                'id','genericMedicamento','nombreMedicamento','marcaMedicamento',
                'pesoMedicamento','cantDisponible','medicionMedicamento',
                'fechaIngreso','fechaCaducidad','codMedicamento','observacionesMedicamento','derivacionesMedicamento'
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
                'fechaIngreso','fechaCaducidad','codMedicamento','observacionesMedicamento','derivacionesMedicamento'
                  )