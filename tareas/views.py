from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def create(self, request):
        """Endpoint para crear una nueva tarea"""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        """Endpoint para eliminar una tarea específica"""
        try:
            tarea = self.get_object()
            tarea.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['put'])
    def completar(self, request, pk=None):
        """Endpoint para marcar una tarea como completada"""
        try:
            tarea = self.get_object()
            tarea.completed = True
            tarea.save()
            serializer = self.get_serializer(tarea)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        """Endpoint para listar todas las tareas pendientes"""
        tareas = Task.objects.filter(completed=False)
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        """Endpoint para obtener detalles de una tarea específica"""
        try:
            tarea = self.get_object()
            serializer = self.get_serializer(tarea)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

