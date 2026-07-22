from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Viaje, TipoUnidad, Operador


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


class OperadorForm(forms.ModelForm):
    class Meta:
        model = Operador
        fields = ['nombre', 'licencia', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del chofer'
            }),
            'licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de licencia'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del chofer',
            'licencia': 'Número de licencia',
            'activo': 'Chofer activo',
        }


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
            'operador', 'tipo_unidad', 'peso_carga', 'unidad_peso',
            'origen', 'codigo_postal_origen', 'destino', 'codigo_postal_destino',
            'km_distancia', 'viaje_redondo', 'precio_diesel_litro',
            'pagado', 'fecha_pago', 'fecha_viaje',
            'gastos_casetas', 'gastos_diesel', 'otros_gastos',
            'costo_viaje', 'ganancia',
        ]
        widgets = {
            'numero_viaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: V-001'}),
            'numero_contenedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contenedor'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura'}),
            'operador': forms.Select(attrs={'class': 'form-control', 'id': 'id_operador'}),
            'tipo_unidad': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_unidad'}),
            'peso_carga': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'id': 'id_peso_carga', 'placeholder': 'Ej: 12.5'
            }),
            'unidad_peso': forms.Select(attrs={'class': 'form-control', 'id': 'id_unidad_peso'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lázaro Cárdenas, Michoacán'}),
            'codigo_postal_origen': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: 60950',
                'inputmode': 'numeric'
            }),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Puebla, Puebla'}),
            'codigo_postal_destino': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: 72000',
                'inputmode': 'numeric'
            }),
            'km_distancia': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'id': 'id_km_distancia', 'placeholder': 'Se calcula automáticamente'
            }),
            'viaje_redondo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_viaje_redondo'}),
            'precio_diesel_litro': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.001', 'min': '0',
                'id': 'id_precio_diesel_litro', 'placeholder': 'Ej: 28.015'
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
        self.fields['codigo_postal_origen'].required = False
        self.fields['codigo_postal_destino'].required = False
        self.fields['peso_carga'].required = False
        self.fields['unidad_peso'].required = False
        self.fields['operador'].required = False
        operadores_qs = Operador.objects.filter(activo=True)
        if self.instance and self.instance.pk and self.instance.operador_id:
            operadores_qs = Operador.objects.filter(
                Q(activo=True) | Q(pk=self.instance.operador_id)
            )
        self.fields['operador'].queryset = operadores_qs.order_by('nombre')
        self.fields['operador'].empty_label = '— Elegir chofer —'
        self.fields['operador'].label = 'Elegir chofer'
        self.fields['tipo_unidad'].required = False
        self.fields['tipo_unidad'].queryset = TipoUnidad.objects.all()
        self.fields['tipo_unidad'].empty_label = '— Selecciona tipo de unidad —'

