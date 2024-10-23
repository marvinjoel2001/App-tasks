from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=200,
        help_text="Título de la tarea"
    )
    description = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Descripción detallada de la tarea"
    )
    completed = serializers.BooleanField(
        default=False,
        help_text="Indica si la tarea está completada"
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Fecha y hora de creación de la tarea"
    )