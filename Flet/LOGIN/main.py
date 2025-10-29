import flet as ft
import sqlite3
import os
# Ruta de la base de datos
DB_PATH = r"C:\Users\Jared Hernández\OneDrive\Escritorio\sqlite-tools-win-x64-3500400\User.db"
# Ruta de imágenes
IMG_PATH = r"C:\GIT\Git\p1\Flet\Imagenes"
# Crear tabla si no existe
def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT,
            Apellido TEXT,
            UsuarioID TEXT,
            Correo TEXT,
            Contraseña TEXT
        )
    """)
    conn.commit()
    conn.close()

# Llamar para crear tabla al iniciar
inicializar_db()
# Función para insertar usuarios en la base de datos
def registrar_usuario(nombre, apellido, usuarioid, correo, contrasena):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE UsuarioID=? OR Correo=?", (usuarioid, correo))
    if cursor.fetchone():
        conn.close()
        return False  # Ya existe
    cursor.execute(
        "INSERT INTO User (Nombre, Apellido, UsuarioID, Correo, Contraseña) VALUES (?, ?, ?, ?, ?)",
        (nombre, apellido, usuarioid, correo, contrasena),
    )
    conn.commit()
    conn.close()
    return True
# Función para validar inicio de sesión
def validar_usuario(correo, contrasena):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE Correo=? AND Contraseña=?", (correo, contrasena))
    user = cursor.fetchone()
    conn.close()
    return user is not None
# Pantallas de la app
def main(page: ft.Page):
    page.title = "Habit Login"
    page.bgcolor = ft.Colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # Pantalla 3: Inicio de sesión
    def pantalla_inicio():
        correo = ft.TextField(label="correo@electrónico.com", width=300)
        btn_continuar = ft.ElevatedButton(
            "Continuar", bgcolor="black", color="white", on_click=lambda e: mostrar_login_contra()
        )
        registrar_link = ft.TextButton("¿No tienes una cuenta? Regístrate", on_click=lambda e: mostrar_registro())

        contenido = ft.Column(
            [
                ft.Image(src=os.path.join(IMG_PATH, "Imagen3.png"), width=150, height=150),
                ft.Text("Crea una cuenta", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Ingresa tu correo electrónico para registrarte en esta aplicación"),
                correo,
                btn_continuar,
                registrar_link,
                ft.Text("Términos de servicio y Política de privacidad", size=10, color="black54"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.clean()
        page.add(contenido)
    # Pantalla 1: Registro de usuario
    def mostrar_registro():
        nombre = ft.TextField(label="Nombre(s)", width=300)
        apellido = ft.TextField(label="Apellidos", width=300)
        usuarioid = ft.TextField(label="Nombre de usuario (id)", width=300)
        correo = ft.TextField(label="Correo", width=300)
        contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        confirmar = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, width=300)
        mensaje = ft.Text("", color="red")

        def registrar_click(e):
            if not all([nombre.value, apellido.value, usuarioid.value, correo.value, contrasena.value, confirmar.value]):
                mensaje.value = "Por favor completa todos los campos."
                page.update()
                return
            if contrasena.value != confirmar.value:
                mensaje.value = "Las contraseñas no coinciden."
                page.update()
                return
            if registrar_usuario(nombre.value, apellido.value, usuarioid.value, correo.value, contrasena.value):
                mostrar_exito()
            else:
                mensaje.value = "El usuario o correo ya existe."
                page.update()

        contenido = ft.Column(
            [
                ft.Text("Hola Soy Habit", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("¿Listo para programar tus hábitos y optimizar tu día?"),
                ft.Image(src=os.path.join(IMG_PATH, "Imagen1.png"), width=100, height=100),
                nombre,
                apellido,
                usuarioid,
                correo,
                contrasena,
                confirmar,
                ft.Text(
                    "Al hacer clic en registrarse, aceptas nuestros Términos de servicio y Política de privacidad",
                    size=10,
                    text_align=ft.TextAlign.CENTER,
                ),
                mensaje,
                ft.ElevatedButton("Registrarse", bgcolor="black", color="white", on_click=registrar_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.clean()
        page.add(contenido)
    # Pantalla 2: Mensaje de éxito
    def mostrar_exito():
        contenido = ft.Column(
            [
                ft.Text("Excelente", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Ya estás conectado conmigo, y juntos construiremos algo grande"),
                ft.Image(src=os.path.join(IMG_PATH, "Imagen2.png"), width=120, height=120),
                ft.ElevatedButton("¡Iniciar!", bgcolor="black", color="white", on_click=lambda e: mostrar_login_contra()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.clean()
        page.add(contenido)
    # Pantalla 4: Login con contraseña
    def mostrar_login_contra():
        correo = ft.TextField(label="Correo electrónico", width=300)
        contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        mensaje = ft.Text("", color="red")

        def login_click(e):
            if validar_usuario(correo.value, contrasena.value):
                mensaje.value = "Inicio de sesión exitoso 🎉"
                mensaje.color = "green"
            else:
                mensaje.value = "Correo o contraseña incorrectos."
                mensaje.color = "red"
            page.update()

        contenido = ft.Column(
            [
                ft.Image(src=os.path.join(IMG_PATH, "Imagen4.png"), width=150, height=150),
                ft.Text("Ingresa tu contraseña para registrarte en esta aplicación"),
                correo,
                contrasena,
                mensaje,
                ft.ElevatedButton("Continuar", bgcolor="black", color="white", on_click=login_click),
                ft.Text("Términos de servicio y Política de privacidad", size=10, color="black54"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.clean()
        page.add(contenido)

    # Iniciar en pantalla de inicio
    pantalla_inicio()

# Lanzar la app
ft.app(target=main)
