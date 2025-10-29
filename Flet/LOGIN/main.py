import flet as ft
import sqlite3
import os

# Clase para manejar la base de datos
class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "User.db")
        self.inicializar_db()

    def inicializar_db(self):
        conn = sqlite3.connect(self.db_path)
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

    def registrar_usuario(self, nombre, apellido, usuarioid, correo, contrasena):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE UsuarioID=? OR Correo=?", (usuarioid, correo))
        if cursor.fetchone():
            conn.close()
            return False
        cursor.execute(
            "INSERT INTO User (Nombre, Apellido, UsuarioID, Correo, Contraseña) VALUES (?, ?, ?, ?, ?)",
            (nombre, apellido, usuarioid, correo, contrasena)
        )
        conn.commit()
        conn.close()
        return True

    def validar_usuario(self, correo, contrasena):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE Correo=? AND Contraseña=?", (correo, contrasena))
        user = cursor.fetchone()
        conn.close()
        return user is not None


# Clase principal de la app
class HabitApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Habit Login"
        self.page.bgcolor = ft.Colors.WHITE
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Configuración de ventana (simula celular)
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.window_resizable = False

        # Rutas
        self.img_path = os.path.join(os.path.dirname(__file__), "Imagenes")
        self.db = DatabaseManager()

        # Verificar ruta de imagen
        print("Ruta de imagen esperada:", os.path.join(self.img_path, "Imagen1.png"))
        print("Existe imagen:", os.path.exists(os.path.join(self.img_path, "Imagen1.png")))

        # Inicia en pantalla de inicio
        self.pantalla_inicio()

    
    # Pantallas

    def pantalla_inicio(self):
        correo = ft.TextField(label="correo@electrónico.com", width=300, color="black")
        btn_continuar = ft.ElevatedButton(
            "Continuar", bgcolor="black", color="white", on_click=lambda e: self.mostrar_login_contra()
        )
        registrar_link = ft.TextButton(
            "¿No tienes una cuenta? Regístrate",
            on_click=lambda e: self.mostrar_registro(),
            style=ft.ButtonStyle(color="blue"),
        )

        contenido = ft.Column(
            [
                ft.Image(src=os.path.join(self.img_path, "Imagen3.png"), width=150, height=150),
                ft.Text("Crea una cuenta", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text(
                    "Ingresa tu correo electrónico para registrarte en esta aplicación",
                    color="black"
                ),
                correo,
                btn_continuar,
                registrar_link,
                ft.Text("Términos de servicio y Política de privacidad", size=10, color="black54"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.clean()
        self.page.add(contenido)

    def mostrar_registro(self):
        nombre = ft.TextField(label="Nombre(s)", width=300, color="black")
        apellido = ft.TextField(label="Apellidos", width=300, color="black")
        usuarioid = ft.TextField(label="Nombre de usuario (id)", width=300, color="black")
        correo = ft.TextField(label="Correo", width=300, color="black")
        contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, color="black")
        confirmar = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, width=300, color="black")
        mensaje = ft.Text("", color="red")

        def registrar_click(e):
            if not all([nombre.value, apellido.value, usuarioid.value, correo.value, contrasena.value, confirmar.value]):
                mensaje.value = "Por favor completa todos los campos."
                self.page.update()
                return
            if contrasena.value != confirmar.value:
                mensaje.value = "Las contraseñas no coinciden."
                self.page.update()
                return
            if self.db.registrar_usuario(nombre.value, apellido.value, usuarioid.value, correo.value, contrasena.value):
                self.mostrar_exito()
            else:
                mensaje.value = "El usuario o correo ya existe."
                self.page.update()

        contenido = ft.Column(
            [
                ft.Text("Hola Soy Habit", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("¿Listo para programar tus hábitos y optimizar tu día?", color="black"),
                ft.Image(src=os.path.join(self.img_path, "Imagen1.png"), width=100, height=100),
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
                    color="black"
                ),
                mensaje,
                ft.ElevatedButton("Registrarse", bgcolor="black", color="white", on_click=registrar_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.clean()
        self.page.add(contenido)

    def mostrar_exito(self):
        contenido = ft.Column(
            [
                ft.Text("Excelente", size=22, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Ya estás conectado conmigo, y juntos construiremos algo grande", color="black"),
                ft.Image(src=os.path.join(self.img_path, "Imagen2.png"), width=120, height=120),
                ft.ElevatedButton("¡Iniciar!", bgcolor="black", color="white", on_click=lambda e: self.mostrar_login_contra()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.clean()
        self.page.add(contenido)

    def mostrar_login_contra(self):
        correo = ft.TextField(label="Correo electrónico", width=300, color="black")
        contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, color="black")
        mensaje = ft.Text("", color="red")

        def login_click(e):
            if self.db.validar_usuario(correo.value, contrasena.value):
                mensaje.value = "Inicio de sesión exitoso 🎉"
                mensaje.color = "green"
            else:
                mensaje.value = "Correo o contraseña incorrectos."
                mensaje.color = "red"
            self.page.update()

        contenido = ft.Column(
            [
                ft.Image(src=os.path.join(self.img_path, "Imagen4.png"), width=150, height=150),
                ft.Text("Ingresa tu contraseña para registrarte en esta aplicación", color="black"),
                correo,
                contrasena,
                mensaje,
                ft.ElevatedButton("Continuar", bgcolor="black", color="white", on_click=login_click),
                ft.Text("Términos de servicio y Política de privacidad", size=10, color="black54"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.clean()
        self.page.add(contenido)



# Función principal

def main(page: ft.Page):
    HabitApp(page)


ft.app(target=main)
