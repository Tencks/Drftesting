
from rest_framework import routers
from .api import ProjectViewSet, ResidenteViewSet, StockMedicamentosResidenteViewSet, ObservacionSemanalViewSet,UsersRegisterViewSet,UsersLoginViewSet,StockMedicamentosLocalViewSet

router = routers.DefaultRouter()

router.register('api/register', UsersRegisterViewSet, 'register')
router.register('api/login', UsersLoginViewSet, 'login')
router.register('api/project', ProjectViewSet, 'project')
router.register('api/residentes', ResidenteViewSet, 'residentes')
router.register('api/medicamentosresidente', StockMedicamentosResidenteViewSet, 'stockMedicamentosResidente')
router.register('api/observacionessemanales', ObservacionSemanalViewSet, 'Observaciones Semanales')
router.register('api/medicamentoslocales', StockMedicamentosLocalViewSet, 'MedicamentosLocales')

urlpatterns  = router.urls