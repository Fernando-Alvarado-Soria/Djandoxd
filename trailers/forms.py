from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdminUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label='Con permisos de administrador (is_staff)')

    class Meta:
        model = User
        fields = ('username', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        if commit:
            user.save()
        return user
from django import forms
from .models import Viaje, Unidad, TipoUnidad


class ViajeForm(forms.ModelForm):
    PAGADO_CHOICES = [
        (False, 'No'),
        (True, 'Sí'),
    ]

    pagado = forms.ChoiceField(
        choices=PAGADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_pagado'}),
        label='¿Viaje pagado?'
    )

    class Meta:
        model = Viaje
        fields = [
            'numero_viaje', 'numero_contenedor', 'numero_factura',
            'tipo_unidad', 'origen', 'destino',
            'km_distancia', 'viaje_redondo', 'precio_diesel_litro',
            'pagado', 'fecha_pago', 'fecha_viaje',
            'gastos_casetas', 'gastos_diesel', 'otros_gastos',
            'costo_viaje', 'ganancia',
        ]
        widgets = {
            'numero_viaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: V-001'}),
            'numero_contenedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contenedor'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura'}),
            'tipo_unidad': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_unidad'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lázaro Cárdenas, Michoacán'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Puebla, Puebla'}),
            'km_distancia': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'id': 'id_km_distancia', 'placeholder': 'Se calcula automáticamente'
            }),
            'viaje_redondo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_viaje_redondo'}),
            'precio_diesel_litro': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'id': 'id_precio_diesel_litro', 'placeholder': 'Ej: 24.50'
            }),
            'fecha_pago': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_viaje': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gastos_casetas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'gastos_diesel': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'id': 'id_gastos_diesel'
            }),
            'otros_gastos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'costo_viaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'ganancia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Agregar al finalizar el viaje'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ganancia'].required = False
        self.fields['fecha_pago'].required = False
        self.fields['fecha_viaje'].required = False
        self.fields['km_distancia'].required = False
        self.fields['precio_diesel_litro'].required = False
        self.fields['tipo_unidad'].required = False
        self.fields['tipo_unidad'].queryset = TipoUnidad.objects.all()
        self.fields['tipo_unidad'].empty_label = '— Selecciona tipo de unidad —'

