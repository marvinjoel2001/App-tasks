💻 Instalación

1:  Clonar el repositorio
git clone https://github.com/marvinjoel2001/App-tasks.git



2:  Crear y activar entorno virtual

python -m venv env
source env/bin/activate  # En Linux/Mac



3:  Instalar dependencias

pip install -r requirements.txt



4:  Ejecutar migraciones
!!! ya no son necesarias 
#python manage.py makemigrations
#python manage.py migrate



5: Ejecutar APP EN CONSOLA

python manage.py todo_cli 

/****************************************************************/
 1: Ejecutar APIS
 python manage.py runserver



 2: Curls de prueba
Api Documentation: http://localhost:8000/swagger/


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




/****************************************************************/

Decisiones de Diseño - Gestor de Tareas
Bueno pues, armé esta app:
1. Por qué elegí trabajar con archivo JSON en vez de base de datos o otro formato de datos:

Es más liviano y no necesita instalar nada extra
Los datos se pueden ver fácil abriendo el archivo nomás
Si quieres hacer backup, copias el archivo y listo

2. Cómo organicé el código:

Puse todo en una clase bien ordenada pa' que cualquiera lo entienda
Cada método hace una cosa nomás (agregar, eliminar, etc.)
Los emojis los puse para que se vea más bonito en la consola y mas entendible para mi usuario
Todo está comentado pa' que otro programador le entienda rápido

3. Estructura del JSON:
json
[
    {
        "id": 1,
        "title": "Hacer las compras",
        "description": "Pan, leche, huevos",
        "completed": false,
        "created_at": "2024-10-23 15:30:00"
    }
]
Así queda bien clarito y ordenado.
4. Ventajas que tiene:

Bien fácil de usar
No hay que estar instalando programas extras
Si algo falla, es fácil de arreglar


5. Por qué usé Python y Django:

Todo el mundo lo usa y hay harta y ayuda en internet
Es rapido pa' hacer este tipo de apps
Los errores los muestra clarito
La documentación está bien completa

