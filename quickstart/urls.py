from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from rest_framework import routers
from . import api
from .api import  ResidenteViewSet, StockMedicamentosResidenteViewSet, ObservacionSemanalViewSet,StockMedicamentosLocalViewSet,Record, Login, Logout

# Configuración de las URLs para las vistas Record, Login y Logout
urlpatterns = [
    path('api/addUser/', Record.as_view(), name="register"),
    path('api/login/', Login.as_view(), name="login"),
    path('api/logout/', Logout.as_view(), name="logout"),
    path('api/residentes/<int:residente_id>/medicamentos/', api.medicamentos_residente, name='medicamentos_residente'),
    path('api/residentes/<int:residente_id>/signosVitales/', api.Observacion_residente, name='Observacion_residente'),

    
]


# Configuración de las URLs utilizando DefaultRouter() para las otras vistas basadas en conjuntos

router = routers.DefaultRouter()

router.register('api/residentes', ResidenteViewSet, 'residentes')
router.register('api/medicamentosresidente', StockMedicamentosResidenteViewSet, 'stockMedicamentosResidente')
router.register('api/observacionessemanales', ObservacionSemanalViewSet, 'Observaciones Semanales')
router.register('api/medicamentoslocales', StockMedicamentosLocalViewSet, 'MedicamentosLocales')


# asi era antes la línea : urlpatterns  = router.urls
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)