import tkinter as tk
from tkinter import messagebox
from Clases import AdminTarea, Usuario
import requests

admin_tarea = AdminTarea()
usuario_autenticado = None

def validar_credenciales():
    global usuario_autenticado

    usuario = entrada_usuario.get()
    contraseña = entrada_contraseña.get()

    usuario_obj = Usuario(None, None, None, None, None, contraseña)  # Creamos un objeto Usuario para utilizar su método autenticar
    if usuario_obj.autenticar(usuario, contraseña):
        usuario_autenticado = usuario
        messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario}!")
        ventana_principal()
    else:
        messagebox.showerror("Error de inicio de sesión", "Credenciales inválidas. Inténtalo nuevamente.")

def ventana_principal():
    root.withdraw()  # Ocultar la ventana de inicio de sesión

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Admin de Tareas")
    ventana.geometry("400x500")

    # Etiqueta y entrada para el título de la tarea
    lbl_titulo = tk.Label(ventana, text="Título:")
    lbl_titulo.pack(anchor=tk.W)
    entrada_titulo = tk.Entry(ventana)
    entrada_titulo.pack(fill=tk.X)

    # Etiqueta y entrada para la descripción de la tarea
    lbl_descripcion = tk.Label(ventana, text="Descripción:")
    lbl_descripcion.pack(anchor=tk.W)
    entrada_descripcion = tk.Entry(ventana)
    entrada_descripcion.pack(fill=tk.X)

    def agregar_tarea():
        titulo = entrada_titulo.get()
        descripcion = entrada_descripcion.get()

        tarea_id = admin_tarea.agregar_tarea(titulo, descripcion)
        messagebox.showinfo("Tarea agregada", f"Se ha agregado la tarea con ID: {tarea_id}")
        entrada_titulo.delete(0, tk.END)
        entrada_descripcion.delete(0, tk.END)

    def eliminar_tarea():
        tarea_id = entrada_eliminar.get()
        if tarea_id:
            tarea_id = int(tarea_id)
            if admin_tarea.eliminar_tarea(tarea_id):
                messagebox.showinfo("Tarea eliminada", f"Se ha eliminado la tarea con ID: {tarea_id}")
                entrada_eliminar.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea. Verifica el ID.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingresa el ID de la tarea a eliminar.")

    def traer_tareas():
        tareas = admin_tarea.obtener_tareas()
        if tareas:
            texto_tareas.delete("1.0", tk.END)  # Limpiar el cuadro de texto
            for tarea in tareas:
                tarea_texto = f"ID: {tarea[0]}\nTítulo: {tarea[1]}\nDescripción: {tarea[2]}\nEstado: {tarea[3]}\nCreada: {tarea[4]}\nActualizada: {tarea[5]}\n\n"
                texto_tareas.insert(tk.END, tarea_texto)
        else:
            messagebox.showinfo("Sin tareas", "No hay tareas registradas.")

    # Botón Agregar Tarea
    btn_agregar_tarea = tk.Button(ventana, text="Agregar Tarea", command=agregar_tarea)
    btn_agregar_tarea.pack(pady=10)

    # Etiqueta y entrada para el ID de la tarea a eliminar
    lbl_eliminar = tk.Label(ventana, text="ID Tarea a Eliminar:")
    lbl_eliminar.pack(anchor=tk.W)
    entrada_eliminar = tk.Entry(ventana)
    entrada_eliminar.pack(fill=tk.X)

    # Botón Eliminar Tarea
    btn_eliminar_tarea = tk.Button(ventana, text="Eliminar Tarea", command=eliminar_tarea)
    btn_eliminar_tarea.pack(pady=10)

    # Botón Traer Tareas
    btn_traer_tareas = tk.Button(ventana, text="Traer Tareas", command=traer_tareas)
    btn_traer_tareas.pack(pady=10)

    # Cuadro de texto para mostrar las tareas
    texto_tareas = tk.Text(ventana, width=40, height=10)
    texto_tareas.pack()

    ventana.mainloop()

# Crear la ventana de inicio de sesión
root = tk.Tk()
root.title("Inicio de sesión")
root.geometry("400x300")

# Frame principal
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Etiqueta y entrada para el nombre de usuario
lbl_usuario = tk.Label(frame, text="Usuario:")
lbl_usuario.pack(anchor=tk.W)
entrada_usuario = tk.Entry(frame)
entrada_usuario.pack(fill=tk.X)

# Etiqueta y entrada para la contraseña
lbl_contraseña = tk.Label(frame, text="Contraseña:")
lbl_contraseña.pack(anchor=tk.W)
entrada_contraseña = tk.Entry(frame, show="*")
entrada_contraseña.pack(fill=tk.X)

# Botón Iniciar Sesión
btn_iniciar_sesion = tk.Button(frame, text="Iniciar Sesión", command=validar_credenciales, width=15)
btn_iniciar_sesion.pack(pady=10)

root.mainloop()