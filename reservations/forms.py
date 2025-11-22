from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Room, Reservation

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Correo Institucional', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@campusucc.edu.co'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'location', 'equipment', 'image']
        labels = {
            'name': 'Nombre de la Sala',
            'capacity': 'Capacidad',
            'location': 'Ubicación',
            'equipment': 'Equipamiento',
            'image': 'Imagen',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Pizarra, TV, Proyector'}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'date', 'start_time', 'end_time', 'reason']
        labels = {
            'room': 'Sala',
            'date': 'Fecha',
            'start_time': 'Hora de Inicio',
            'end_time': 'Hora de Fin',
            'reason': 'Motivo de la Reserva',
        }
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')

        if date:
            if date.weekday() >= 5: # 5 is Saturday, 6 is Sunday
                self.add_error('date', 'Las reservas solo están permitidas de lunes a viernes.')

        if start_time and end_time:
            # Define limits
            import datetime
            limit_start = datetime.time(7, 0)
            limit_end = datetime.time(21, 0)

            if start_time < limit_start or start_time > limit_end:
                self.add_error('start_time', 'Las reservas solo están permitidas entre las 7:00 AM y las 9:00 PM.')
            
            if end_time < limit_start or end_time > limit_end:
                self.add_error('end_time', 'Las reservas solo están permitidas entre las 7:00 AM y las 9:00 PM.')

            if start_time >= end_time:
                self.add_error('end_time', 'La hora de fin debe ser posterior a la hora de inicio.')
            
            # Check duration
            # Create dummy dates to calculate difference
            dummy_date = datetime.date(2000, 1, 1)
            dt_start = datetime.datetime.combine(dummy_date, start_time)
            dt_end = datetime.datetime.combine(dummy_date, end_time)
            duration = dt_end - dt_start
            
            if duration > datetime.timedelta(hours=2):
                self.add_error('end_time', 'La duración máxima de la reserva es de 2 horas.')
        
        return cleaned_data
