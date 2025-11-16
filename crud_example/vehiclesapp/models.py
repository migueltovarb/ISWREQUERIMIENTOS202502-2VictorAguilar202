from django.db import models

class Vehicle(models.Model):
    COLORS = [
        ('rojo', 'Rojo'),
        ('azul', 'Azul'),
        ('verde', 'Verde'),
        
    ]
    
    numero_placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLORS)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_placa}"
    
    class Meta:
        ordering = ['-fecha_creacion']