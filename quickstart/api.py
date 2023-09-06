from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics


from .models import  Residente, StockMedicamentosResidente, ObservaciónSemanal, User, StockMedicamentosLocal
from .serializers import  ResidenteSerializer, StockMedicamentosResidenteSerializer, ObservacionSemanalSerializer, StockMedicamentosLocalSerializer
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







class ResidenteViewSet(viewsets.ModelViewSet):
    queryset = Residente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ResidenteSerializer
    

class StockMedicamentosResidenteViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamentosResidente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StockMedicamentosResidenteSerializer


def medicamentos_residente(request, residente_id):
    residente = get_object_or_404(Residente, pk=residente_id)
    medicamentos = residente.medicamentos.all()
    data = [{
        'Generico':med.genericMedicamento,
        'Nombre': med.nombreMedicamento,
        'Marca': med.marcaMedicamento,
        'Peso': med.pesoMedicamento,
        'CantidadDisponible': med.cantDisponible,
        'Medida': med.medicionMedicamento,
        'FechaIngreso': med.fechaIngreso,
        'FechaCaducidad': med.fechaCaducidad,
        'Codigo': med.codMedicamento,
        'Observaciones': med.observacionesMedicamento,
        'Derivaciones': med.derivacionesMedicamento,

            
            } for med in medicamentos]
    return JsonResponse({'medicamentos': data})




    
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











class StockMedicamentosLocalViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamentosLocal.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StockMedicamentosLocalSerializer