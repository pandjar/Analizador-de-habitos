"""
#¡ PYTHON 3
Proyecto: Analizador de Hábitos Personales Gamificado
Materia: Programación Orientada a Objetos
Versión: Interactiva con entrada de usuario
Creador: Hernandez Castro Jared
"""
import json
import datetime
from abc import ABC, abstractmethod

# =============================================
# CLASE PRINCIPAL: HABITO
# =============================================
class Habito:
    "Clase que representa un hábito que el usuario quiere desarrollar"
    def __init__(self, nombre, descripcion, dificultad, frecuencia_semanal, categoria):
        "Constructor de la clase Habito"
        self._nombre = nombre
        self._descripcion = descripcion
        self._dificultad = dificultad
        self._frecuencia_semanal = frecuencia_semanal
        self._categoria = categoria
        self._registros = []
        self._puntos = 0
        self._fecha_creacion = datetime.date.today()
    # GETTERS Y SETTERS
    def get_nombre(self):
        return self._nombre
    def get_dificultad(self):
        return self._dificultad
    def get_puntos(self):
        return self._puntos
    def get_categoria(self):
        return self._categoria
    def get_frecuencia_semanal(self):
        return self._frecuencia_semanal
    def set_nombre(self, nuevo_nombre):
        try:
            if len(nuevo_nombre.strip()) > 0:
                self._nombre = nuevo_nombre
                print(" Nombre actualizado correctamente")
            else:
                raise ValueError("El nombre no puede estar vacío")
        except ValueError as e:
            print(f" Error: {e}")
    
    def set_descripcion(self, nueva_descripcion):
        self._descripcion = nueva_descripcion
        print(" Descripción actualizada correctamente")
    # MÉTODOS PRINCIPALES
    def registrar_cumplimiento(self):
        """
        Registra que el hábito fue cumplido hoy
        """
        try:
            fecha_hoy = datetime.date.today()
            
            # Verificar si ya se registró hoy
            for fecha in self._registros:
                if fecha == fecha_hoy:
                    print(" ¡Ya registraste este hábito hoy!")
                    return False
            # Agregar a registros
            self._registros.append(fecha_hoy)
            # Calcular puntos (dificultad * 10 + bono por racha)
            puntos_base = self._dificultad * 10
            bono_racha = self._calcular_bono_racha()
            puntos_totales = puntos_base + bono_racha
            self._puntos += puntos_totales
            print(f" ¡Hábito '{self._nombre}' registrado exitosamente!")
            print(f" Puntos ganados: {puntos_base} (base) + {bono_racha} (bono racha) = {puntos_totales}")
            return True
        except Exception as e:
            print(f" Error al registrar cumplimiento: {e}")
            return False
    def _calcular_bono_racha(self):
        "Calcula bono por racha de días consecutivos"
        try:
            if not self._registros:
                return 0
            # Ordenar fechas y verificar racha actual
            fechas_ordenadas = sorted(self._registros)
            racha_actual = 1
            
            for i in range(len(fechas_ordenadas)-1, 0, -1):
                diferencia = (fechas_ordenadas[i] - fechas_ordenadas[i-1]).days
                if diferencia == 1:
                    racha_actual += 1
                else:
                    break
            # Bono: 2 puntos por cada día de racha (máximo 20)
            bono = min(racha_actual * 2, 20)
            if bono > 0:
                print(f" ¡Racha de {racha_actual} días! Bono: +{bono} puntos")
            return bono
            
        except Exception as e:
            print(f"Error calculando bono de racha: {e}")
            return 0
    def calcular_eficiencia(self):
        "Calcula qué tan bien se está cumpliendo el hábito"
        try:
            semana_actual = datetime.date.today().isocalendar()[1]
            registros_esta_semana = 0
            
            for fecha in self._registros:
                if fecha.isocalendar()[1] == semana_actual:
                    registros_esta_semana += 1
            
            if self._frecuencia_semanal > 0:
                eficiencia = (registros_esta_semana / self._frecuencia_semanal) * 100
                return min(eficiencia, 100)
            else:
                return 0
        except Exception as e:
            print(f"Error al calcular eficiencia: {e}")
            return 0
    def mostrar_estadisticas(self):
        "Muestra estadísticas detalladas del hábito"
        eficiencia = self.calcular_eficiencia()
        total_registros = len(self._registros)
        print(f"\n ESTADÍSTICAS DE '{self._nombre}'")
        print("=" * 40)
        print(f" Descripción: {self._descripcion}")
        print(f"️  Categoría: {self._categoria}")
        print(f" Dificultad: {self._dificultad}/5")
        print(f" Frecuencia semanal: {self._frecuencia_semanal} veces")
        print(f" Puntos acumulados: {self._puntos}")
        print(f" Eficiencia semanal: {eficiencia:.1f}%")
        print(f" Total de registros: {total_registros}")
        print(f" Creado el: {self._fecha_creacion}")
        # Mostrar últimos 5 registros
        if self._registros:
            print(f" Últimos registros: {', '.join(str(fecha) for fecha in sorted(self._registros[-5:]))}")    
    def to_dict(self):
        """Convierte a diccionario para guardar"""
        return {
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'dificultad': self._dificultad,
            'frecuencia_semanal': self._frecuencia_semanal,
            'categoria': self._categoria,
            'registros': [fecha.isoformat() for fecha in self._registros],
            'puntos': self._puntos,
            'fecha_creacion': self._fecha_creacion.isoformat()
        }
    @classmethod
    def from_dict(cls, data):
        "Crea objeto desde diccionario"
        habito = cls(
            data['nombre'],
            data['descripcion'],
            data['dificultad'],
            data['frecuencia_semanal'],
            data['categoria']
        )
        habito._registros = [datetime.date.fromisoformat(fecha) for fecha in data['registros']]
        habito._puntos = data['puntos']
        habito._fecha_creacion = datetime.date.fromisoformat(data['fecha_creacion'])
        return habito
    def __str__(self):
        eficiencia = self.calcular_eficiencia()
        return f"️ {self._nombre} | {self._dificultad}/5 | {eficiencia:.1f}% | {self._puntos} pts | ️{self._categoria}"
# =============================================
# SISTEMA DE RECOMPENSAS GAMIFICADO
# =============================================
class SistemaRecompensas:
    "Sistema de recompensas y niveles gamificados"
    def __init__(self):
        self._niveles = {
            100: "Principiante",
            300: " Aprendiz", 
            600: " Avanzado",
            1000: " Experto",
            1500: " Maestro",
            2500: " Leyenda"
        }
        self._logros_desbloqueados = []
        self._insignias = {
            'primer_habito': {'nombre': ' Iniciador', 'desbloqueada': False},
            'racha_7_dias': {'nombre': ' Racha de Fuego', 'desbloqueada': False},
            'eficiencia_100': {'nombre': ' Perfeccionista', 'desbloqueada': False},
            'habitos_multiple': {'nombre': ' Multitarea', 'desbloqueada': False}
        }
    def verificar_niveles(self, puntos):
        "Verifica si se alcanzó algún nuevo nivel"
        try:
            for puntos_requeridos, nivel in self._niveles.items():
                if puntos >= puntos_requeridos and nivel not in self._logros_desbloqueados:
                    self._logros_desbloqueados.append(nivel)
                    return True, nivel
            return False, None
        except Exception as e:
            print(f"Error al verificar niveles: {e}")
            return False, None
    def verificar_insignias(self, habitos, puntos_totales):
        "Verifica y desbloquea insignias"
        insignias_desbloqueadas = []
        # Insignia por primer hábito
        if not self._insignias['primer_habito']['desbloqueada'] and len(habitos) >= 1:
            self._insignias['primer_habito']['desbloqueada'] = True
            insignias_desbloqueadas.append(self._insignias['primer_habito']['nombre'])
        # Insignia por múltiples hábitos
        if not self._insignias['habitos_multiple']['desbloqueada'] and len(habitos) >= 3:
            self._insignias['habitos_multiple']['desbloqueada'] = True
            insignias_desbloqueadas.append(self._insignias['habitos_multiple']['nombre'])
        # Insignia por racha (simulada para ejemplo)
        if not self._insignias['racha_7_dias']['desbloqueada'] and puntos_totales >= 500:
            self._insignias['racha_7_dias']['desbloqueada'] = True
            insignias_desbloqueadas.append(self._insignias['racha_7_dias']['nombre']) 
        return insignias_desbloqueadas
    def obtener_nivel_actual(self, puntos):
        "Obtiene el nivel actual basado en puntos"
        nivel_actual = " Novato"
        for puntos_requeridos, nivel in sorted(self._niveles.items()):
            if puntos >= puntos_requeridos:
                nivel_actual = nivel
        return nivel_actual
    def mostrar_progreso(self, puntos):
        "Muestra el progreso hacia el siguiente nivel"
        nivel_actual = self.obtener_nivel_actual(puntos)
        niveles_ordenados = sorted(self._niveles.items())
        # Encontrar nivel actual y siguiente
        for i, (puntos_req, nivel) in enumerate(niveles_ordenados):
            if puntos < puntos_req:
                nivel_siguiente = nivel
                puntos_siguiente = puntos_req
                puntos_anterior = niveles_ordenados[i-1][0] if i > 0 else 0
                break
        else:
            # Si está en el nivel máximo
            nivel_siguiente = "Nivel Máximo"
            puntos_siguiente = puntos
            puntos_anterior = niveles_ordenados[-1][0]
        if nivel_siguiente != "Nivel Máximo":
            progreso = ((puntos - puntos_anterior) / (puntos_siguiente - puntos_anterior)) * 100
            print(f" Progreso al siguiente nivel: {progreso:.1f}%")
            print(f" Puntos necesarios para {nivel_siguiente}: {puntos_siguiente - puntos}")
        return nivel_actual
# =============================================
# GESTOR PRINCIPAL DE HÁBITOS
# =============================================
class GestorHabitos:
    "Clase principal que gestiona todos los hábitos"
    def __init__(self):
        self._habitos = []
        self._sistema_recompensas = SistemaRecompensas()
        self._archivo_datos = "habitos_data.json"
        self._categorias_disponibles = [
            "Salud", "Deporte", "Estudio", "Trabajo", 
            "Personal", "Finanzas", "Social", "Otros"
        ]
    def _obtener_entrada_usuario(self, mensaje, tipo=str, rango=None):
        "Función auxiliar para obtener entrada del usuario con validación"
        while True:
            try:
                entrada = input(mensaje).strip()
                if tipo == int:
                    entrada = int(entrada)
                    if rango and (entrada < rango[0] or entrada > rango[1]):
                        print(f" Por favor ingresa un número entre {rango[0]} y {rango[1]}")
                        continue
                elif tipo == str and not entrada:
                    print(" Esta campo no puede estar vacío")
                    continue
                return entrada
            except ValueError:
                print(" Por favor ingresa un número válido")
            except Exception as e:
                print(f" Error: {e}")
    def _mostrar_categorias(self):
        "Muestra las categorías disponibles"
        print("\n️ CATEGORÍAS DISPONIBLES:")
        for i, categoria in enumerate(self._categorias_disponibles, 1):
            print(f"   {i}. {categoria}")
    def agregar_habito(self):
        "Interfaz para que el usuario agregue un nuevo hábito"
        print("\n" + "="*50)
        print("          AGREGAR NUEVO HÁBITO")
        print("="*50)
        # Obtener datos del usuario
        nombre = self._obtener_entrada_usuario(" Nombre del hábito: ", str)
        descripcion = self._obtener_entrada_usuario(" Descripción: ", str)
        # Mostrar y seleccionar categoría
        self._mostrar_categorias()
        opcion_categoria = self._obtener_entrada_usuario(
            "️ Selecciona una categoría (número): ", 
            int, 
            (1, len(self._categorias_disponibles))
        )
        categoria = self._categorias_disponibles[opcion_categoria - 1]
        
        dificultad = self._obtener_entrada_usuario(
            " Dificultad (1-5, donde 5 es más difícil): ",
            int,
            (1, 5)
        )
        frecuencia_semanal = self._obtener_entrada_usuario(
            " Veces por semana que quieres realizarlo: ",
            int,
            (1, 7)
        )
        # Confirmar creación
        print(f"\n RESUMEN DEL HÁBITO:")
        print(f"   Nombre: {nombre}")
        print(f"   Descripción: {descripcion}")
        print(f"   Categoría: {categoria}")
        print(f"   Dificultad: {dificultad}/5")
        print(f"   Frecuencia: {frecuencia_semanal} veces por semana")
        confirmar = input("\n¿Crear este hábito? (s/n): ").strip().lower()
        if confirmar == 's':
            try:
                nuevo_habito = Habito(nombre, descripcion, dificultad, frecuencia_semanal, categoria)
                self._habitos.append(nuevo_habito)
                print("¡Hábito creado exitosamente!")
                
                # Verificar insignias
                puntos_totales = self.calcular_puntos_totales()
                insignias = self._sistema_recompensas.verificar_insignias(self._habitos, puntos_totales)
                if insignias:
                    print(" ¡Nueva insignia desbloqueada!")
                    for insignia in insignias:
                        print(f" (*) {insignia}")
            except Exception as e:
                print(f" Error al crear hábito: {e}")
        else:
            print(" Creación cancelada")
    def listar_habitos(self):
        "Muestra todos los hábitos con opciones interactivas"
        if not self._habitos:
            print("\n No hay hábitos registrados.")
            return
        print("\n" + "="*50)
        print("           TUS HÁBITOS")
        print("="*50)
        for i, habito in enumerate(self._habitos, 1):
            print(f"{i}. {habito}")
        # Opciones adicionales
        print("\n OPCIONES:")
        print("   • Ingresa el número de un hábito para ver detalles")
        print("   • Ingresa '0' para volver al menú principal")
        opcion = self._obtener_entrada_usuario(
            "\nTu elección: ",
            int,
            (0, len(self._habitos))
        )
        if opcion > 0:
            self._mostrar_detalles_habito(opcion - 1)
    def _mostrar_detalles_habito(self, indice):
        "Muestra detalles de un hábito específico con opciones"
        habito = self._habitos[indice]
        while True:
            habito.mostrar_estadisticas()
            
            print("\n🔧 OPCIONES:")
            print("   1.  Registrar cumplimiento")
            print("   2.  Editar hábito")
            print("   3.  Ver estadísticas completas")
            print("   4.  Volver a la lista")
            
            opcion = self._obtener_entrada_usuario(
                "\nSelecciona una opción: ",
                int,
                (1, 4)
            )
            if opcion == 1:
                self.registrar_habito_cumplido(indice)
                break
            elif opcion == 2:
                self._editar_habito(indice)
            elif opcion == 3:
                self._mostrar_estadisticas_completas(indice)
            elif opcion == 4:
                break
    def _editar_habito(self, indice):
        "Permite al usuario editar un hábito"
        habito = self._habitos[indice]
        print("\n️ EDITAR HÁBITO")
        print("1. Cambiar nombre")
        print("2. Cambiar descripción")
        print("3. Cambiar categoría")
        print("4. Cancelar")
        opcion = self._obtener_entrada_usuario(
            "Selecciona qué quieres editar: ",
            int,
            (1, 4)
        )
        if opcion == 1:
            nuevo_nombre = self._obtener_entrada_usuario("Nuevo nombre: ", str)
            habito.set_nombre(nuevo_nombre)
        elif opcion == 2:
            nueva_desc = self._obtener_entrada_usuario("Nueva descripción: ", str)
            habito.set_descripcion(nueva_desc)
        elif opcion == 3:
            self._mostrar_categorias()
            nueva_cat = self._obtener_entrada_usuario(
                "Nueva categoría (número): ",
                int,
                (1, len(self._categorias_disponibles))
            )
            habito._categoria = self._categorias_disponibles[nueva_cat - 1]
            print(" Categoría actualizada correctamente")
    def _mostrar_estadisticas_completas(self, indice):
        "Muestra estadísticas detalladas de un hábito"
        habito = self._habitos[indice]
        print("\n" + "="*50)
        print("        ESTADÍSTICAS COMPLETAS")
        print("="*50)
        habito.mostrar_estadisticas()
        # Estadísticas adicionales
        total_registros = len(habito._registros)
        if total_registros > 0:
            primer_registro = min(habito._registros)
            dias_activo = (datetime.date.today() - primer_registro).days
            print(f" Días activo: {dias_activo}")
            print(f" Promedio por día: {total_registros / max(dias_activo, 1):.2f}")
    def registrar_habito_cumplido(self, indice=None):
        "Registra un hábito como cumplido"
        if indice is None:
            self.listar_habitos()
            if not self._habitos:
                return
            
            indice = self._obtener_entrada_usuario(
                "Número del hábito a registrar: ",
                int,
                (1, len(self._habitos))
            ) - 1
        if 0 <= indice < len(self._habitos):
            habito = self._habitos[indice]
            if habito.registrar_cumplimiento():
                # Verificar recompensas
                puntos_totales = self.calcular_puntos_totales()
                nuevo_nivel, nivel = self._sistema_recompensas.verificar_niveles(puntos_totales)
                if nuevo_nivel:
                    print(f"\n ¡FELICIDADES! Has alcanzado el nivel: {nivel} ")
                # Verificar insignias
                insignias = self._sistema_recompensas.verificar_insignias(self._habitos, puntos_totales)
                for insignia in insignias:
                    print(f" ¡Nueva insignia desbloqueada: {insignia}!")
        else:
            print(" Índice de hábito no válido")
    def calcular_puntos_totales(self):
        "Calcula puntos totales de todos los hábitos"
        return sum(habito.get_puntos() for habito in self._habitos)
    def mostrar_progreso_general(self):
        "Muestra el progreso general del usuario"
        puntos_totales = self.calcular_puntos_totales()
        print("\n" + "="*50)
        print("           PROGRESO GENERAL")
        print("="*50)
        nivel_actual = self._sistema_recompensas.mostrar_progreso(puntos_totales)
        print(f" Nivel actual: {nivel_actual}")
        print(f" Puntos totales: {puntos_totales}")
        print(f" Total de hábitos: {len(self._habitos)}")
        # Estadísticas por categoría
        categorias = {}
        for habito in self._habitos:
            cat = habito.get_categoria()
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(habito)
        print(f"\n HÁBITOS POR CATEGORÍA:")
        for categoria, habitos in categorias.items():
            print(f"   {categoria}: {len(habitos)} hábito(s)")
        # Eficiencia promedio
        if self._habitos:
            eficiencia_promedio = sum(habito.calcular_eficiencia() for habito in self._habitos) / len(self._habitos)
            print(f" Eficiencia promedio: {eficiencia_promedio:.1f}%")
            # Hábito más eficiente
            habito_mas_eficiente = max(self._habitos, key=lambda h: h.calcular_eficiencia())
            print(f" Hábito más eficiente: {habito_mas_eficiente.get_nombre()} ({habito_mas_eficiente.calcular_eficiencia():.1f}%)")
    # MÉTODOS DE PERSISTENCIA
    def guardar_datos(self):
        "Guarda los datos en archivo JSON"
        try:
            datos = {
                'habitos': [habito.to_dict() for habito in self._habitos],
                'fecha_actualizacion': datetime.datetime.now().isoformat()
            }
            with open(self._archivo_datos, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            print(" Datos guardados exitosamente!")
        except Exception as e:
            print(f" Error al guardar datos: {e}")
    def cargar_datos(self):
        "Carga los datos desde archivo JSON"
        try:
            with open(self._archivo_datos, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            self._habitos = [Habito.from_dict(habito_data) for habito_data in datos['habitos']]
            print(" Datos cargados exitosamente!")
            print(f" Se cargaron {len(self._habitos)} hábitos")
        except FileNotFoundError:
            print(" No se encontró archivo de datos. Comenzando desde cero.")
        except Exception as e:
            print(f" Error al cargar datos: {e}")
# =============================================
# MENÚ PRINCIPAL INTERACTIVO
# =============================================
def mostrar_menu_principal():
    "Muestra el menú principal con opciones"
    print("\n" + "="*50)
    print(" ANALIZADOR DE HÁBITOS - GAMIFICADO")
    print("="*50)
    print("1.  Agregar nuevo hábito")
    print("2.  Listar mis hábitos")
    print("3.  Registrar hábito cumplido")
    print("4.  Ver progreso general")
    print("5.  Guardar y salir")
    print("="*50)
def main():
    "Función principal del programa"
    gestor = GestorHabitos()
    # Cargar datos existentes
    print(" Iniciando Analizador de Hábitos Gamificado...")
    gestor.cargar_datos()
    while True:
        try:
            mostrar_menu_principal()
            opcion = input("Selecciona una opción (1-5): ").strip()
            if opcion == "1":
                gestor.agregar_habito()
            elif opcion == "2":
                gestor.listar_habitos()
            elif opcion == "3":
                gestor.registrar_habito_cumplido()
            elif opcion == "4":
                gestor.mostrar_progreso_general()
            elif opcion == "5":
                gestor.guardar_datos()
                print("\n ¡Datos guardados! ¡Hasta pronto! ")
                print(" Sigue trabajando en tus hábitos. ¡Tú puedes! ")
                break
            else:
                print(" Opción no válida. Por favor selecciona 1-5.")
        except KeyboardInterrupt:
            print("\n\n Programa interrumpido. Guardando datos...")
            gestor.guardar_datos()
            break
        except Exception as e:
            print(f" Error inesperado: {e}")
# =============================================
# INICIO DEL PROGRAMA
# =============================================
if __name__ == "__main__":
    main()
