from .models import project, Residente, StockMedicamentosResidente, ObservaciónSemanal
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializer, ResidenteSerializer, StockMedicamentosResidenteSerializer, ObservacionSemanalSerializer

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