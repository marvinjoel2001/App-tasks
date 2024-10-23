from django.db import models

# tareas/models.py
class Task(models.Model):
    """
    Modelo que representa una tarea en el sistema.
    """
    title = models.CharField(
        max_length=200,
        help_text="Título de la tarea"
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción detallada de la tarea"
    )
    completed = models.BooleanField(
        default=False,
        help_text="Indica si la tarea está completada"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación de la tarea"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title