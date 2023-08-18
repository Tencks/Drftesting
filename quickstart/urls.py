from rest_framework import routers
from .api import ProjectViewSet, ResidenteViewSet, StockMedicamentosResidenteViewSet, ObservacionSemanalViewSet

router = routers.DefaultRouter()

router.register('api/project', ProjectViewSet, 'project')
router.register('api/residentes', ResidenteViewSet, 'residentes')
router.register('api/medicamentosresidente', StockMedicamentosResidenteViewSet, 'stockMedicamentosResidente')
router.register('api/observacionessemanales', ObservacionSemanalViewSet, 'Observaciones Semanales')

urlpatterns  = router.urls