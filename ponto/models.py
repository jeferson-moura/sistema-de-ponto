from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models

class RegistroPonto(models.Model):
    atrasado = models.BooleanField(default=False)
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    data_hora = models.DateTimeField(auto_now_add=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.funcionario} - {self.tipo} - {self.data_hora}"