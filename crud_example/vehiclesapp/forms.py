from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['numero_placa', 'marca', 'modelo', 'color']
        widgets = {
            'numero_placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC-123'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Corolla'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }