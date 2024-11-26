from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet,VehículoViewSet
import django.contrib.auth.urls

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'vehiculos', VehículoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.IndexView, name='indexCar'),
    path('login/', views.LoginView, name='login'),
    path('registro/', views.RegistroView, name='registro'),
    path('cotizador/<int:vehículoId>', views.CotizadorView, name='cotizador'),
    path('catalogo/', views.CatalogoView, name='catalogo'),
    path('accounts/', include(django.contrib.auth.urls)),
    path('logout/', views.exit, name='exit'),
    #path('registro2/',views.Registro2View, name='registro2'),
    path('guardar_cotizacion/', views.guardar_cotizacion, name='guardar_cotizacion'),
    path('borrar-plan/<int:plan_id>/', views.borrar_plan, name='borrar_plan'),
    path('panelUsuario/', views.PanelUsuarioView, name='panelUsuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)