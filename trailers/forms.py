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
from .models import Viaje


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
        fields = ['numero_viaje', 'numero_contenedor', 'numero_factura', 'origen', 'destino', 
                  'pagado', 'fecha_pago', 'fecha_viaje', 'gastos_casetas', 
                  'gastos_diesel', 'otros_gastos', 'costo_viaje', 'ganancia']
        widgets = {
            'numero_viaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: V-001'}),
            'numero_contenedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contenedor'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura'}),
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de origen'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de destino'}),
            'fecha_pago': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_viaje': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gastos_casetas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'gastos_diesel': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'otros_gastos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'costo_viaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'ganancia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Agregar al finalizar el viaje'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ganancia'].required = False
        self.fields['fecha_pago'].required = False
        self.fields['fecha_viaje'].required = False

