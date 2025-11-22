from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

def validate_institutional_email(value):
    if not value.endswith('@campusucc.edu.co'):  # Placeholder domain
        raise ValidationError(
            _('Solo se permiten correos institucionales (@campusucc.edu.co).'),
            params={'value': value},
        )

class User(AbstractUser):
    email = models.EmailField(_('dirección de correo'), unique=True, validators=[validate_institutional_email])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def role_name(self):
        if self.is_staff:
            return "Administrador"
        if self.groups.filter(name='Profesor').exists():
            return "Profesor"
        return "Estudiante"

class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad")
    location = models.CharField(max_length=100, verbose_name="Ubicación")
    equipment = models.TextField(help_text="Lista de equipamiento separado por comas", verbose_name="Equipamiento")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name="Imagen de la Sala")

    def __str__(self):
        return f"{self.name} ({self.capacity} pers.)"

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Sala") # Delete reservations if room is deleted
    date = models.DateField(verbose_name="Fecha")
    start_time = models.TimeField(verbose_name="Hora Inicio")
    end_time = models.TimeField(verbose_name="Hora Fin")
    reason = models.TextField(verbose_name="Motivo")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.date} {self.start_time}"
