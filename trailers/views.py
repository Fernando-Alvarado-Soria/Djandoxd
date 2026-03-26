from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Viaje
from .forms import ViajeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import AdminUserCreationForm


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
    return render(request, 'trailers/agregar_viaje.html', {'form': form})


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
    return render(request, 'trailers/editar_viaje.html', {'form': form, 'viaje': viaje})


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

