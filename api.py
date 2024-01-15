from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Clases import AdminTarea

app = FastAPI()
admin_tarea = AdminTarea()

class Credenciales(BaseModel):
    nombre: str
    contraseña: str

class Tarea(BaseModel):
    titulo: str
    descripcion: str

@app.post("/login")
async def login(credenciales: Credenciales):
    if admin_tarea.autenticar(credenciales.nombre, credenciales.contraseña):
        return {"mensaje": "Inicio de sesión exitoso"}
    else:
        return {"error": "Credenciales inválidas"}

@app.post("/tareas")
async def crear_tarea(tarea: Tarea):
    tarea_id = admin_tarea.agregar_tarea(tarea.titulo, tarea.descripcion)
    return {"tarea_id": tarea_id}

@app.get("/tareas/{tarea_id}")
async def obtener_tarea(tarea_id: int):
    tarea = admin_tarea.obtener_tarea(tarea_id)
    if tarea:
        return tarea
    else:
        return {"error": "Tarea no encontrada"}

@app.put("/tareas/{tarea_id}")
async def actualizar_tarea(tarea_id: int, tarea: Tarea):
    if admin_tarea.actualizar_tarea(tarea_id, tarea.titulo, tarea.descripcion):
        return {"mensaje": "Tarea actualizada correctamente"}
    else:
        return {"error": "No se pudo actualizar la tarea"}

@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: int):
    if admin_tarea.eliminar_tarea(tarea_id):
        return {"mensaje": "Tarea eliminada correctamente"}
    else:
        return {"error": "No se pudo eliminar la tarea"}