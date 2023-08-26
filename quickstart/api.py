from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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
    
class ObservacionSemanalViewSet(viewsets.ModelViewSet):
    queryset = ObservaciónSemanal.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ObservacionSemanalSerializer


class StockMedicamentosLocalViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamentosLocal.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StockMedicamentosLocalSerializer