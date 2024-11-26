import json
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .models import Plan, Usuario, Vehículo
from .serializers import UsuarioSerializer,VehículoSerializer
from .forms import CustomUserAuthenticationForm, CustomUserRegistrationForm

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class VehículoViewSet(viewsets.ModelViewSet):
    queryset = Vehículo.objects.all()
    serializer_class = VehículoSerializer

def IndexView(request):
    return render(request,'indexCar.html')

def LoginView(request):
    return render(request,'login.html')

def RegistroView(request):
    data = {
        'form': CustomUserRegistrationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserRegistrationForm(data=request.POST)
        if user_creation_form.is_valid():
            auth_user = user_creation_form.save()
            clientes_group, created = Group.objects.get_or_create(name="Clientes")
            auth_user.groups.add(clientes_group)
            auth_user = authenticate(
                username=auth_user.username,
                password=user_creation_form.cleaned_data['password1']
            )
            if auth_user is not None:
                login(request, auth_user)
                return redirect('indexCar')
            else:
                data['error'] = "Error de autenticación. Por favor, intenta de nuevo."
        else:
            data['error'] = "El formulario no es válido. Revisa los datos ingresados."
        data['form'] = user_creation_form 
    return render(request, 'registration/register.html', data)


@login_required
def CotizadorView(request, vehículoId):
    vehículo = get_object_or_404(Vehículo, id=vehículoId)
    return render(request, 'cotizador.html', {'vehículo': vehículo})

@login_required
def CatalogoView(request):
    vehículos = Vehículo.objects.all()
    return render(request, 'CatalogoAutos.html', {'vehículos': vehículos})

@login_required
def PanelUsuarioView(request):
    actual_user = request.user
    planes = Plan.objects.filter(usuario=actual_user)
    return render(request, "panelUsuario.html", {'planes': planes})

def borrar_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, usuario=request.user)  # Asegurarte de que el plan pertenezca al usuario
    plan.delete()
    messages.success(request, "El plan se ha eliminado correctamente.")
    return redirect('panelUsuario')

def exit(request):
    logout(request)
    return redirect('indexCar')

# def Registro2View(request):
#     return render(request,'registration/register2.html')

def guardar_cotizacion(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            usuario = request.user
            vehículo_id = data.get('vehiculo_id')
            mensualidades = data.get('mensualidades')
            plazo = data.get('plazo')
            monto_a_financiar = data.get('monto_a_financiar')
            pago_inicial = data.get('pago_inicial')
            seguro_contado = data.get('seguro_contado')
            
            vehículo = get_object_or_404(Vehículo, id=vehículo_id)

            # Crear y guardar el nuevo plan
            plan = Plan.objects.create(
                mensualidades=int(mensualidades),
                plazo=int(plazo),
                montoAFinanciar=float(monto_a_financiar),
                pagoInicial=float(pago_inicial),
                seguroContado=float(seguro_contado),
                usuario=usuario,
                vehículo=vehículo
            )
            return JsonResponse({"success": True, 
                                 "message": "Cotización guardada exitosamente.",
                                 "redirect_url": reverse('panelUsuario')})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "message": "Método no permitido o usuario no autenticado."})