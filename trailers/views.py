from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Viaje, Unidad, TipoUnidad
from .forms import ViajeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import AdminUserCreationForm
import requests as http_requests


# Create your views here.

@login_required
def lista_viajes(request):
    """Vista para listar todos los viajes"""
    viajes = Viaje.objects.all()
    return render(request, 'trailers/lista_viajes.html', {'viajes': viajes})


@login_required
def agregar_viaje(request):
    """Vista para agregar un nuevo viaje"""
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje agregado exitosamente.')
            return redirect('lista_viajes')
    else:
        form = ViajeForm()
    tipos_unidad = TipoUnidad.objects.all()
    return render(request, 'trailers/agregar_viaje.html', {'form': form, 'tipos_unidad': tipos_unidad})


@login_required
def editar_viaje(request, viaje_id):
    """Vista para editar un viaje existente"""
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if request.method == 'POST':
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje actualizado exitosamente.')
            return redirect('lista_viajes')
    else:
        form = ViajeForm(instance=viaje)
    tipos_unidad = TipoUnidad.objects.all()
    return render(request, 'trailers/editar_viaje.html', {'form': form, 'viaje': viaje, 'tipos_unidad': tipos_unidad})


@login_required
def detalle_viaje(request, viaje_id):
    """Vista de solo lectura para ver todos los datos de un viaje"""
    viaje = get_object_or_404(Viaje, id=viaje_id)
    return render(request, 'trailers/detalle_viaje.html', {'viaje': viaje})


@login_required
def borrar_viaje(request, viaje_id):
    """Vista para borrar un viaje"""
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if request.method == 'POST':
        viaje.delete()
        messages.success(request, 'Viaje eliminado exitosamente.')
        return redirect('lista_viajes')
    return render(request, 'trailers/borrar_viaje.html', {'viaje': viaje})


def staff_check(user):
    return user.is_authenticated and user.is_staff


@login_required
def calcular_distancia(request):
    """Endpoint interno que consulta OpenRouteService y devuelve km entre origen y destino."""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    origen = request.GET.get('origen', '').strip()
    destino = request.GET.get('destino', '').strip()

    if not origen or not destino:
        return JsonResponse({'error': 'Origen y destino son requeridos'}, status=400)

    api_key = settings.ORS_API_KEY
    if not api_key:
        return JsonResponse({'error': 'API key de ORS no configurada'}, status=500)

    def geocodificar(lugar):
        url = 'https://api.openrouteservice.org/geocode/search'
        params = {
            'api_key': api_key,
            'text': lugar + ', México',
            'size': 1,
            'boundary.country': 'MX',
        }
        resp = http_requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        features = resp.json().get('features', [])
        if not features:
            return None
        coords = features[0]['geometry']['coordinates']  # [lon, lat]
        return coords

    try:
        coords_origen = geocodificar(origen)
        coords_destino = geocodificar(destino)

        if not coords_origen or not coords_destino:
            return JsonResponse({'error': 'No se pudo encontrar alguna de las ubicaciones'}, status=404)

        url_ruta = 'https://api.openrouteservice.org/v2/directions/driving-hgv'
        headers = {'Authorization': api_key, 'Content-Type': 'application/json'}
        body = {'coordinates': [coords_origen, coords_destino]}
        resp_ruta = http_requests.post(url_ruta, json=body, headers=headers, timeout=15)
        resp_ruta.raise_for_status()
        data = resp_ruta.json()
        distancia_metros = data['routes'][0]['summary']['distance']
        km = round(distancia_metros / 1000, 2)
        return JsonResponse({'km': km})

    except http_requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al consultar ORS: {str(e)}'}, status=502)
    except (KeyError, IndexError):
        return JsonResponse({'error': 'Respuesta inesperada de ORS'}, status=502)


@login_required
@user_passes_test(staff_check)
def register(request):
    """Crear un nuevo usuario. Accesible solo para usuarios con is_staff."""
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('lista_viajes')
    else:
        form = AdminUserCreationForm()
    return render(request, 'trailers/register.html', {'form': form})

