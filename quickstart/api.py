from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions, status


from .models import project, Residente, StockMedicamentosResidente, ObservaciónSemanal, Users, StockMedicamentosLocal
from .serializers import ProjectSerializer, ResidenteSerializer, StockMedicamentosResidenteSerializer, ObservacionSemanalSerializer, UsersRegisterSerializer,UsersLoginSerializer, StockMedicamentosLocalSerializer


class UsersRegisterViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsersRegisterSerializer

def create(self, request, *args, **kwargs):
        serializer = UsersRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersLoginViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsersLoginSerializer



    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UsersLoginSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            password = serializer.validated_data['password']
            user = authenticate(request, usuario=usuario, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class ProjectViewSet(viewsets.ModelViewSet):
    queryset = project.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer
    

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