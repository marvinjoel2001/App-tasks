💻 Instalación

1:  Clonar el repositorio
git clone https://github.com/marvinjoel2001/App-tasks.git



2:  Crear y activar entorno virtual

python -m venv env
source env/bin/activate  # En Linux/Mac



3:  Instalar dependencias

pip install -r requirements.txt



4:  Ejecutar migraciones

python manage.py makemigrations
python manage.py migrate



5: Ejecutar APP EN CONSOLA

python manage.py todo_cli 

/****************************************************************/
 1: Ejecutar APIS
 python manage.py runserver
 2: Curls de prueba
 # Crear tarea
curl -X POST http://localhost:8000/api/tareas/ \
     -H "Content-Type: application/json" \
     -d '{"title":"Nueva tarea","description":"Descripción"}'

# Eliminar tarea
curl -X DELETE http://localhost:8000/api/tareas/1/

# Marcar como completada
curl -X PUT http://localhost:8000/api/tareas/1/completar/

# Listar tareas pendientes
curl http://localhost:8000/api/tareas/

# Ver detalle de tarea
curl http://localhost:8000/api/tareas/1/