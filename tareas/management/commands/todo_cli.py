from django.core.management.base import BaseCommand
import json
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Gestión de tareas con guardado en archivo json'

    def __init__(self):
        super().__init__()
        self.file_path = 'tareas.json'  # Archivo donde guardaremos las tareas
        # Si no existe el archivo, lo creamos vacío
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _leer_tareas(self):
        """Lee las tareas del archivo json"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _guardar_tareas(self, tareas):
        """Guarda las tareas en el archivo json"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(tareas, f, indent=2, ensure_ascii=False)
    
    def _obtener_siguiente_id(self, tareas):
        """Calcula el siguiente ID disponible"""
        return max([tarea['id'] for tarea in tareas], default=0) + 1

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('''
╔════════════════════════════╗
║     Gestor de Tareas      ║
╚════════════════════════════╝
'''))
        
        while True:
            self.stdout.write("""
¿Qué quieres hacer?
------------------
1. 📝 Agregar tarea
2. ❌ Eliminar tarea
3. ✅ Marcar tarea como completada
4. 📋 Listar tareas
5. 📊 Ver archivo de tareas
6. 🚪 Salir
            """)
            
            try:
                opcion = input("\nElige una opción: ").strip()
                
                if opcion == "1":
                    self.agregar_tarea()
                elif opcion == "2":
                    self.eliminar_tarea()
                elif opcion == "3":
                    self.completar_tarea()
                elif opcion == "4":
                    self.listar_tareas(solo_pendientes=True)
                elif opcion == "5":
                    self.ver_archivo_tareas()
                elif opcion == "6":
                    self.stdout.write(self.style.SUCCESS("\n¡Chau! Nos vemos 👋\n"))
                    break
                else:
                    self.stdout.write(self.style.WARNING("\n⚠️  Opción inválida. Intenta de nuevo.\n"))
            
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("\n\n¡Chau! Nos vemos 👋\n"))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\n❌ Error: {str(e)}\n"))

    def agregar_tarea(self):
        """Agregar una nueva tarea"""
        self.stdout.write("\n📝 NUEVA TAREA")
        self.stdout.write("-" * 20)
        
        titulo = input("Título: ").strip()
        if not titulo:
            self.stdout.write(self.style.ERROR("❌ El título no puede estar vacío"))
            return
            
        descripcion = input("Descripción (opcional): ").strip()
        
        try:
            # Lee las tareas actuales
            tareas = self._leer_tareas()
            
            # Crea la nueva tarea
            nueva_tarea = {
                'id': self._obtener_siguiente_id(tareas),
                'title': titulo,
                'description': descripcion,
                'completed': False,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Agrega y guardamos
            tareas.append(nueva_tarea)
            self._guardar_tareas(tareas)
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Tarea '{titulo}' creada con éxito!\n"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error al crear la tarea: {str(e)}\n"))

    def eliminar_tarea(self):
        """Eliminar una tarea existente"""
        self.listar_tareas(solo_pendientes=True)
        try:
            id_tarea = input("\nID de la tarea a eliminar (0 para cancelar): ").strip()
            
            if id_tarea == "0":
                return
            
            # Carga las tareas y buscamos la que queremos eliminar    
            tareas = self._leer_tareas()
            tarea = next((t for t in tareas if t['id'] == int(id_tarea)), None)
            
            if not tarea:
                self.stdout.write(self.style.ERROR("\n❌ Tarea no encontrada\n"))
                return
            
            # Filtra la tarea a eliminar
            tareas = [t for t in tareas if t['id'] != int(id_tarea)]
            self._guardar_tareas(tareas)
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Tarea '{tarea['title']}' eliminada con éxito!\n"))
            
        except ValueError:
            self.stdout.write(self.style.ERROR("\n❌ ID inválido\n"))

    def completar_tarea(self):
        """Marcar una tarea como completada"""
        self.listar_tareas(solo_pendientes=True)
        try:
            id_tarea = input("\nID de la tarea a completar (0 para cancelar): ").strip()
            
            if id_tarea == "0":
                return
            
            # Carga y buscamos la tarea a completar    
            tareas = self._leer_tareas()
            tarea_completada = False
            
            for tarea in tareas:
                if tarea['id'] == int(id_tarea) and not tarea['completed']:
                    tarea['completed'] = True
                    tarea_completada = True
                    self._guardar_tareas(tareas)
                    self.stdout.write(self.style.SUCCESS(f"\n✅ ¡Tarea '{tarea['title']}' completada!\n"))
                    break
            
            if not tarea_completada:
                self.stdout.write(self.style.ERROR("\n❌ Tarea no encontrada o ya está completada\n"))
            
        except ValueError:
            self.stdout.write(self.style.ERROR("\n❌ ID inválido\n"))

    def listar_tareas(self, solo_pendientes=False):
        """Listar tareas con formato bonito"""
        tareas = self._leer_tareas()
        
        # Filtras las tareas si solo queremos ver las pendientes
        if solo_pendientes:
            tareas = [t for t in tareas if not t['completed']]
        
        if not tareas:
            self.stdout.write("\n📋 No hay tareas" + (" pendientes" if solo_pendientes else "") + "\n")
            return
            
        self.stdout.write("\n📋 LISTA DE TAREAS" + (" PENDIENTES" if solo_pendientes else ""))
        self.stdout.write("-" * 50)
        
        for tarea in tareas:
            #Usamos simbolos para representar el estado de las tareas
            estado = "⭕" if not tarea['completed'] else "✅"
            self.stdout.write(f"[{tarea['id']}] {estado} {tarea['title']} ({tarea['created_at']})")
            if tarea['description']:
                self.stdout.write(f"    └─ {tarea['description']}")
        
        self.stdout.write("-" * 50)

    def ver_archivo_tareas(self):
        """Ver el contenido del archivo de tareas"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                tareas = json.load(f)
            
            self.stdout.write("\n📊 CONTENIDO DEL ARCHIVO DE TAREAS")
            self.stdout.write("-" * 50)
            self.stdout.write(json.dumps(tareas, indent=2, ensure_ascii=False))
            self.stdout.write("-" * 50)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("\n❌ El archivo de tareas aún no existe\n"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("\n❌ Error al leer el archivo de tareas\n"))