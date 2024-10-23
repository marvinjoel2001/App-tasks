from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    @swagger_auto_schema(
        operation_description="Crea una nueva tarea",
        request_body=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request):
        """Endpoint para crear una nueva tarea"""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Elimina una tarea específica",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def destroy(self, request, pk=None):
        """Endpoint para eliminar una tarea específica"""
        try:
            tarea = self.get_object()
            tarea.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Marca una tarea como completada",
        responses={
            200: TaskSerializer,
            404: "Not Found"
        }
    )
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
        

    @swagger_auto_schema(
        operation_description="Lista todas las tareas pendientes",
        responses={200: TaskSerializer(many=True)}
    )
    def list(self, request):
        """Endpoint para listar todas las tareas pendientes"""
        tareas = Task.objects.filter(completed=False)
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtiene los detalles de una tarea específica",
        responses={
            200: TaskSerializer,
            404: "Not Found"
        }
    )
    def retrieve(self, request, pk=None):
        """Endpoint para obtener detalles de una tarea específica"""
        try:
            tarea = self.get_object()
            serializer = self.get_serializer(tarea)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

