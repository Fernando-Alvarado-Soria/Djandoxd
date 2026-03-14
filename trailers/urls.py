from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_viajes, name='lista_viajes'),
    path('agregar/', views.agregar_viaje, name='agregar_viaje'),
    path('editar/<int:viaje_id>/', views.editar_viaje, name='editar_viaje'),
    path('borrar/<int:viaje_id>/', views.borrar_viaje, name='borrar_viaje'),
]
