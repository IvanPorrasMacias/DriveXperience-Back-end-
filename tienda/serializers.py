from rest_framework import serializers
from .models import Usuario,Vehículo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class VehículoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehículo
        fields = '__all__'