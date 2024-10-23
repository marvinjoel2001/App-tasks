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