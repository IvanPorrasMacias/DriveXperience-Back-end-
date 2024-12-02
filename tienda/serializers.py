from rest_framework import serializers
from .models import Usuario,Vehículo,Plan

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class VehículoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehículo
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__' 