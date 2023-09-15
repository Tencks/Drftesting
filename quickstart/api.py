from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics
from datetime import datetime, timedelta
from django.db.models import Sum



from .models import  Residente, StockMedicamentosResidente, ObservaciónSemanal, User, StockMedicamentosLocal, LocalArmonia,CuracionesResidente
from .serializers import  ResidenteSerializer, StockMedicamentosResidenteSerializer, ObservacionSemanalSerializer, StockMedicamentosLocalSerializer, LocalArmoniaSerializer, CuracionesResidentesSerializer,MedicationStatusSerializer, MedicationArmoniaStatusSerializer
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer


class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
   

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
         user = serializer_class.validated_data.get('user')
    
         return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer
   
    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
    return redirect('/api/login')   


class UserDataViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ResidenteViewSet(viewsets.ModelViewSet):
    queryset = Residente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ResidenteSerializer
    

class StockMedicamentosResidenteViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamentosResidente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StockMedicamentosResidenteSerializer


# VISTA DEL MEDICAMENTO
def medicamentos_residente(request, residente_id):
    residente = get_object_or_404(Residente, pk=residente_id)
    medicamentos = residente.medicamentos.all()
    data = [{
        'Generico':med.genericMedicamento,
        'Nombre': med.nombreMedicamento,
        'Marca': med.marcaMedicamento,
        'Peso': med.pesoMedicamento,
        'CantidadTotal': med.cantidadTotal,
        'Medida': med.medicionMedicamento,
        'FechaInicio': med.fechaInicio,
        'cantidadDiaria': med.cantidadDiaria,
        'cantidadDisponible': med.cantidadDisponible,
        'Codigo': med.codMedicamento,
        'Observaciones': med.observacionesMedicamento,
        'Derivaciones': med.derivacionesMedicamento,
        'id': med.id,

            
            } for med in medicamentos]
    return JsonResponse({'medicamentos': data})


# FUNCION QUE SE AL SER CONSULTADA HACE UN FOR A TODOS LOS RESIDENTES
# PARA ANALIZAR SUS MEDICAMENTOS Y DETERMINAR CUAL SE ESTA QUEDANDO CON MENOS
# DEL 10% DEL MISMO O SI LA CANTIDAD RESTANTE ES INFERIOR A LA NECESARIA 
# PARA ABARCAR UNA SEMANA DE MEDICACIÓN

class MedicationStatusView(APIView):
    def get(self, request, *args, **kwargs):
        # Realiza el cálculo del estado de los medicamentos aquí

        # Calcula lowMedication
        residentes = Residente.objects.all()  # Obtener todos los residentes
        resultados = []

        for residente in residentes:
            medicamentos_residentes = StockMedicamentosResidente.objects.filter(residenteM=residente)
            for medicamento_residente in medicamentos_residentes:
                cantidad_total = medicamento_residente.cantidadTotal
                cantidad_disponible = medicamento_residente.cantidadDisponible

                if cantidad_disponible <= (0.1 * cantidad_total):
                    low_medication = True  # Hay pocos medicamentos
                else:
                    low_medication = False  # Suficientes medicamentos

                medicamento = medicamento_residente.nombreMedicamento
                cantidad_consumida_por_dia = medicamento_residente.cantidadDiaria

                dias_restantes = cantidad_disponible / cantidad_consumida_por_dia

                # Calcular la fecha de agotamiento y la fecha actual
                fecha_inicio = medicamento_residente.fechaInicio
                fecha_agotamiento = fecha_inicio + timedelta(days=dias_restantes)
                today = datetime.now().date()

                if dias_restantes < 7:
                    less_than_a_week = True  # Menos de una semana de suministro
                else:
                    less_than_a_week = False  # Suficiente suministro para al menos una semana

                # Crear un diccionario con los resultados para cada medicamento del residente
                resultado = {
                    'residente': residente.nombreResidente,  # Aquí debes ajustar el campo que contiene el nombre del residente
                    'medicamento': medicamento,
                    'lowMedication': low_medication,
                    'lessThanAWeek': less_than_a_week,
                    'fechaAgotamiento': fecha_agotamiento.strftime('%Y-%m-%d'),
                    'today': today.strftime('%Y-%m-%d'),
                    # Otros campos si es necesario
                }

                resultados.append(resultado)

        # Serializar la respuesta y devolver la respuesta JSON
        serializer = MedicationStatusSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






    
class ObservacionSemanalViewSet(viewsets.ModelViewSet):
    queryset = ObservaciónSemanal.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ObservacionSemanalSerializer

def Observacion_residente(request, residente_id):
    residente = get_object_or_404(Residente, pk=residente_id)
    observaciones = residente.signosVitales.all()
    data = [{
        'FechaConsulta':med.fechaConsulta,
        'TensionArterial': med.tensionArterial,
        'Glucemia': med.glucemia,
        'Saturacion': med.saturacion,
        'Pulso': med.pulso,
        'Observaciones': med.observacionesSemanales,
        'Derivaciones': med.derivacionesSemanales,

            
            } for med in observaciones]
    return JsonResponse({'signosVitales': data})

class CuracionesResidenteViewSet(viewsets.ModelViewSet):
    queryset = CuracionesResidente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CuracionesResidentesSerializer

def Curacion_residente(request, residente_id):
    residente = get_object_or_404(Residente, pk=residente_id)
    curaciones = residente.curaciones.all()
    data = [{
        'fechaRealizada':med.fechaRealizada,
        'profesional': med.profesional,
        'MedicacionAplicada': med.medicacionAplicada,
        

            
            } for med in curaciones]
    return JsonResponse({'curaciones': data})







class LocalArmonioViewSet(viewsets.ModelViewSet):
    queryset = LocalArmonia.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LocalArmoniaSerializer



class StockMedicamentosLocalViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamentosLocal.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StockMedicamentosLocalSerializer

def medicamentos_local(request, local_id):
    localA = get_object_or_404(LocalArmonia, pk=local_id)
    localMedicamentos = localA.localMedicamentos.all()
    data = [{
        'Generico':med.genericMedicamento,
        'Nombre': med.nombreMedicamento,
        'Marca': med.marcaMedicamento,
        'Peso': med.pesoMedicamento,
        'CantidadTotal': med.cantidadTotal,
        'Medida': med.medicionMedicamento,
        'FechaInicio': med.fechaInicio,
        'cantidadDisponible': med.cantidadDisponible,
        'CantidadDiaria': med.cantidadDiaria,
        'Codigo': med.codMedicamento,
        'Observaciones': med.observacionesMedicamento,
        'Derivaciones': med.derivacionesMedicamento,
        'id': med.id,

            
            } for med in localMedicamentos]
    return JsonResponse({'localMedicamentos': data})

# LOGICA PARA LA NOTIFICACIÓN DEL MEDICAMENTO AGOTÁNDOSE
class MedicationArmoniaStatusView(APIView):
    def get(self, request, local_id, *args, **kwargs):
        # Realiza el cálculo del estado de los medicamentos aquí

        localA = get_object_or_404(LocalArmonia, pk=local_id)
        medicamentos_armonia = StockMedicamentosLocal.objects.filter(localA=localA)

        resultados = []

        for medicamento_local in medicamentos_armonia:
            cantidad_total = medicamento_local.cantidadTotal
            cantidad_disponible = medicamento_local.cantidadDisponible

            if cantidad_disponible <= (0.1 * cantidad_total):
                low_medication = True  # Hay pocos medicamentos
            else:
                low_medication = False  # Suficientes medicamentos

            medicamento = medicamento_local.nombreMedicamento
            cantidad_consumida_por_dia = medicamento_local.cantidadDiaria

            dias_restantes = cantidad_disponible / cantidad_consumida_por_dia

            # Calcular la fecha de agotamiento y la fecha actual
            fecha_inicio = medicamento_local.fechaInicio
            fecha_agotamiento = fecha_inicio + timedelta(days=dias_restantes)
            today = datetime.now().date()

            if dias_restantes < 7:
                less_than_a_week = True  # Menos de una semana de suministro
            else:
                less_than_a_week = False  # Suficiente suministro para al menos una semana

            # Crear un diccionario con los resultados para cada medicamento del residente
            resultado = {
                'local': localA.nombre,  # Aquí debes ajustar el campo que contiene el nombre del local
                'medicamento': medicamento,
                'lowMedication': low_medication,
                'lessThanAWeek': less_than_a_week,
                'fechaAgotamiento': fecha_agotamiento.strftime('%Y-%m-%d'),
                'today': today.strftime('%Y-%m-%d'),
                # Otros campos si es necesario
            }

            resultados.append(resultado)

        # Serializar la respuesta y devolver la respuesta JSON
        serializer = MedicationArmoniaStatusSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)