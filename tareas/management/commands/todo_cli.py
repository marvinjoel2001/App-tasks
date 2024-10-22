from django.core.management.base import BaseCommand
from django.utils import timezone
from tareas.models import Task
import json


class Command(BaseCommand):
    help = 'Gestión de tareas con guardado en BD y archivo'

    def __init__(self):
        super().__init__()
        self.file_path = 'tareas.json'  # Archivo donde guardaremos las tareas
        self.sync_db_to_file()  # Sincronizamos al iniciar

    def sync_db_to_file(self):
        """Sincroniza las tareas de la base de datos al archivo"""
        tareas = list(Task.objects.all().values(
            'id', 
            'title', 
            'description', 
            'completed', 
            'created_at'
        ))
        
        # Convertimos el datetime a string para poder guardarlo en JSON
        for tarea in tareas:
            tarea['created_at'] = tarea['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(tareas, f, indent=2, ensure_ascii=False)

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
            # Aqui Guardamos en la base de datos
            tarea = Task.objects.create(
                title=titulo,
                description=descripcion,
                created_at=timezone.now()
            )
            
            # se sincroniza con el archivo
            self.sync_db_to_file()
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Tarea '{tarea.title}' creada con éxito!\n"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error al crear la tarea: {str(e)}\n"))
    def eliminar_tarea(self):
        """Eliminar una tarea existente"""
        self.listar_tareas(solo_pendientes=True)
        try:
            id_tarea = input("\nID de la tarea a eliminar (0 para cancelar): ").strip()
            
            if id_tarea == "0":
                return
                
            tarea = Task.objects.get(id=id_tarea)
            titulo = tarea.title
            tarea.delete()
            
            # sincronizamos con el archivo
            self.sync_db_to_file()
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Tarea '{titulo}' eliminada con éxito!\n"))
            
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("\n❌ Tarea no encontrada\n"))
        except ValueError:
            self.stdout.write(self.style.ERROR("\n❌ ID inválido\n"))
    def completar_tarea(self):
        """Marcar una tarea como completada"""
        self.listar_tareas(solo_pendientes=True)
        try:
            id_tarea = input("\nID de la tarea a completar (0 para cancelar): ").strip()
            
            if id_tarea == "0":
                return
                
            tarea = Task.objects.get(id=id_tarea, completed=False)
            tarea.completed = True
            tarea.save()
            
            # sincroniza con el archivo
            self.sync_db_to_file()
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ ¡Tarea '{tarea.title}' completada!\n"))
            
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("\n❌ Tarea no encontrada o ya está completada\n"))
        except ValueError:
            self.stdout.write(self.style.ERROR("\n❌ ID inválido\n"))

    def listar_tareas(self, solo_pendientes=False):
        """Listar tareas con formato bonito"""
        queryset = Task.objects.filter(completed=False) if solo_pendientes else Task.objects.all()
        
        if not queryset.exists():
            self.stdout.write("\n📋 No hay tareas" + (" pendientes" if solo_pendientes else "") + "\n")
            return
            
        self.stdout.write("\n📋 LISTA DE TAREAS" + (" PENDIENTES" if solo_pendientes else ""))
        self.stdout.write("-" * 50)
        
        for tarea in queryset:
            #Usamos simbolos para representar el estado de la tareas con su atributo completed
            estado = "⭕" if not tarea.completed else "✅"
            fecha = tarea.created_at.strftime("%d/%m/%Y %H:%M")
            self.stdout.write(f"[{tarea.id}] {estado} {tarea.title} ({fecha})")
            if tarea.description:
                self.stdout.write(f"    └─ {tarea.description}")
        
        self.stdout.write("-" * 50)
           

