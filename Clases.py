import sqlite3
import datetime as dt
import hashlib

class Persona:
    def __init__(self, id, nombre, apellido, fecha_nacimiento, dni):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.dni = dni

class Usuario(Persona):
    def __init__(self, id, nombre, apellido, fecha_nacimiento, dni, contraseña):
        super().__init__(id, nombre, apellido, fecha_nacimiento, dni)
        self.contraseña = hashlib.md5(contraseña.encode()).hexdigest()
        self.ultimo_acceso = None

    def verificar_contraseña(self, contraseña):
        return hashlib.md5(contraseña.encode()).hexdigest() == self.contraseña

    @staticmethod
    def autenticar(usuario, contraseña):
        if usuario == "User" and contraseña == "1234":
            return True
        return False

class AdminTarea:
    def __init__(self):
        self.db_connection = sqlite3.connect('tareas.db')
        self.db_cursor = self.db_connection.cursor()
        self._crear_tabla_tareas()

    def _crear_tabla_tareas(self):
        query = """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT
        )
        """
        self.db_cursor.execute(query)
        self.db_connection.commit()

    def agregar_tarea(self, titulo: str, descripcion: str):
        creada = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        actualizada = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        query = """
        INSERT INTO tareas (titulo, descripcion, estado, creada, actualizada)
        VALUES (?, ?, ?, ?, ?)
        """
        self.db_cursor.execute(query, (titulo, descripcion, 'pendiente', creada, actualizada))
        self.db_connection.commit()
        return self.db_cursor.lastrowid

    def eliminar_tarea(self, tarea_id: int):
        query = """
        DELETE FROM tareas WHERE id = ?
        """
        self.db_cursor.execute(query, (tarea_id,))
        self.db_connection.commit()
        return self.db_cursor.rowcount > 0

    def obtener_tareas(self):
        query = """
        SELECT * FROM tareas
        """
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def actualizar_tarea(self, tarea_id: int, titulo: str, descripcion: str):
        actualizada = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        query = """
        UPDATE tareas SET titulo = ?, descripcion = ?, actualizada = ? WHERE id = ?
        """
        self.db_cursor.execute(query, (titulo, descripcion, actualizada, tarea_id))
        self.db_connection.commit()
        return self.db_cursor.rowcount > 0