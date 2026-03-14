from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Viaje
from .forms import ViajeForm

# Create your views here.

def lista_viajes(request):
    """Vista para listar todos los viajes"""
    viajes = Viaje.objects.all()
    return render(request, 'trailers/lista_viajes.html', {'viajes': viajes})


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
    return render(request, 'trailers/agregar_viaje.html', {'form': form})


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
    return render(request, 'trailers/editar_viaje.html', {'form': form, 'viaje': viaje})


def borrar_viaje(request, viaje_id):
    """Vista para borrar un viaje"""
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if request.method == 'POST':
        viaje.delete()
        messages.success(request, 'Viaje eliminado exitosamente.')
        return redirect('lista_viajes')
    return render(request, 'trailers/borrar_viaje.html', {'viaje': viaje})

