from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from datetime import datetime
import os

class TaskViewSet(viewsets.ModelViewSet):
    json_file = 'tareas.json' #nombre del archivo usado como base de datos para persistir los datos
    serializer_class = TaskSerializer  # Utiliza el serializer para Swagger
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_tasks(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _write_tasks(self, tasks):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

    def _get_next_id(self, tasks):
        return max([task['id'] for task in tasks], default=0) + 1

    @swagger_auto_schema(
        operation_description="Lista todas las tareas pendientes",
        responses={200: TaskSerializer(many=True)}
    )
    def list(self, request):
        """Endpoint para listar todas las tareas pendientes"""
        tasks = self._read_tasks()
        pending_tasks = [task for task in tasks if not task['completed']]
        return Response(pending_tasks)

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
        tasks = self._read_tasks()
        new_task = {
            'id': self._get_next_id(tasks),
            'title': request.data.get('title'),
            'description': request.data.get('description', ''),
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Validamos los datos usando el serializer
        serializer = TaskSerializer(data=new_task)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        tasks.append(new_task)
        self._write_tasks(tasks)
        return Response(new_task, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Obtiene los detalles de una tarea específica",
        responses={
            200: TaskSerializer,
            404: "Not Found"
        }
    )
    def retrieve(self, request, pk=None):
        """Endpoint para obtener detalles de una tarea específica"""
        tasks = self._read_tasks()
        task = next((task for task in tasks if task['id'] == int(pk)), None)
        if task:
            return Response(task)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Elimina una tarea específica",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def destroy(self, request, pk=None):
        """Endpoint para eliminar una tarea específica"""
        tasks = self._read_tasks()
        original_length = len(tasks)
        tasks = [task for task in tasks if task['id'] != int(pk)]
        
        if len(tasks) == original_length:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self._write_tasks(tasks)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        tasks = self._read_tasks()
        for task in tasks:
            if task['id'] == int(pk):
                task['completed'] = True
                self._write_tasks(tasks)
                return Response(task)
        return Response(status=status.HTTP_404_NOT_FOUND)