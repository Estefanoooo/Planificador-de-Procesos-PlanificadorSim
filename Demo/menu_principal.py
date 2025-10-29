import pygame
import sys
import subprocess
from enum import Enum

# ==========================================================
#   Proyecto: PlanificadorSim
#   Descripción: Interfaz principal del simulador visual
#   de algoritmos de planificación de procesos (FCFS, SJF,
#   Round Robin y Prioridad).
# ==========================================================

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO = 1400
ALTO = 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PlanificadorSim - Sistema de Planificación de Procesos")

# Colores
FONDO_OSCURO = (26, 32, 44)
FONDO_MEDIO = (45, 55, 72)
PANEL = (30, 41, 59)
TEXTO = (226, 232, 240)
TEXTO_SECUNDARIO = (148, 163, 184)
ACENTO = (99, 102, 241)
ACENTO_HOVER = (79, 70, 229)
VERDE = (34, 197, 94)
ROJO = (239, 68, 68)
NARANJA = (251, 146, 60)
AZUL_CLARO = (59, 130, 246)

# Fuentes
fuente_titulo = pygame.font.SysFont("Segoe UI", 48, bold=True)
fuente_subtitle = pygame.font.SysFont("Segoe UI", 28, bold=True)
fuente_normal = pygame.font.SysFont("Segoe UI", 20, bold=False)
fuente_boton = pygame.font.SysFont("Segoe UI", 22, bold=True)


# Estados
class Estado(Enum):
    MENU_PRINCIPAL = 1
    SELECCIONAR_ALGORITMO = 2
    SELECCIONAR_DETALLES = 3


class Boton:
    """Clase para crear botones interactivos."""
    def __init__(self, x, y, ancho, alto, texto, color, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.accion = accion
        self.hover = False

    def dibujar(self, pantalla):
        """Dibuja el botón en pantalla."""
        color = self.color_hover if self.hover else self.color
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, TEXTO, self.rect, 2, border_radius=10)

        texto_surf = fuente_boton.render(self.texto, True, TEXTO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        pantalla.blit(texto_surf, texto_rect)

    def actualizar_hover(self, pos_mouse):
        """Actualiza el estado hover según el puntero."""
        self.hover = self.rect.collidepoint(pos_mouse)

    def fue_clickeado(self, pos_mouse):
        """Verifica si fue clickeado."""
        return self.rect.collidepoint(pos_mouse)


class MenuPrincipal:
    """Menú principal del simulador PlanificadorSim."""
    def __init__(self):
        self.estado = Estado.MENU_PRINCIPAL

        # Botones distribuidos en cuadrícula 2x2
        self.boton_prioridad = Boton(150, 280, 480, 100, "Prioridad (Estática/Dinámica)", ACENTO, ACENTO_HOVER)
        self.boton_fcfs = Boton(770, 280, 480, 100, "FCFS (First Come First Served)", AZUL_CLARO, (69, 120, 226))
        self.boton_rr = Boton(150, 450, 480, 100, "Round Robin", VERDE, (24, 167, 84))
        self.boton_sjf = Boton(770, 450, 480, 100, "SJF (Shortest Job First)", NARANJA, (231, 136, 50))
        self.boton_salir = Boton(575, 620, 250, 60, "Salir", ROJO, (209, 58, 58))

        self.reloj = pygame.time.Clock()
        self.animacion_angulo = 0

    def dibujar_menu_principal(self):
        """Dibuja la interfaz principal."""
        pantalla.fill(FONDO_OSCURO)

        # Gradiente de fondo
        for i in range(ALTO):
            color = (
                26 + int((45 - 26) * i / ALTO),
                32 + int((55 - 32) * i / ALTO),
                44 + int((72 - 44) * i / ALTO)
            )
            pygame.draw.line(pantalla, color, (0, i), (ANCHO, i))

        # Título principal
        titulo = fuente_titulo.render("PlanificadorSim", True, TEXTO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, 60))
        pantalla.blit(titulo, titulo_rect)

        subtitulo_app = fuente_subtitle.render("Simulador de Algoritmos de Planificación de Procesos", True, TEXTO_SECUNDARIO)
        subtitulo_rect = subtitulo_app.get_rect(center=(ANCHO // 2, 110))
        pantalla.blit(subtitulo_app, subtitulo_rect)

        # Línea decorativa
        pygame.draw.line(pantalla, ACENTO, (200, 150), (ANCHO - 200, 150), 3)

        # Subtítulo secundario
        subtitulo = fuente_subtitle.render("Selecciona un algoritmo de planificación", True, TEXTO_SECUNDARIO)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, 200))
        pantalla.blit(subtitulo, subtitulo_rect)

        # Botones principales
        for boton in [self.boton_prioridad, self.boton_fcfs, self.boton_rr, self.boton_sjf]:
            sombra = pygame.Surface((boton.rect.width, boton.rect.height))
            sombra.fill(FONDO_MEDIO)
            pantalla.blit(sombra, (boton.rect.x + 5, boton.rect.y + 5))
            boton.dibujar(pantalla)

        # Botón Salir
        self.boton_salir.dibujar(pantalla)

        # Información al pie
        info = fuente_normal.render("Haz clic en cualquier algoritmo para ejecutarlo", True, TEXTO_SECUNDARIO)
        info_rect = info.get_rect(center=(ANCHO // 2, ALTO - 30))
        pantalla.blit(info, info_rect)

    def manejar_eventos(self):
        """Maneja los eventos del menú."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.boton_prioridad.fue_clickeado(pos):
                    self.ejecutar_algoritmo("PrioridadEstaticaDinamica.py")
                    return False

                elif self.boton_fcfs.fue_clickeado(pos):
                    self.ejecutar_algoritmo("fcfs2.py")
                    return False

                elif self.boton_rr.fue_clickeado(pos):
                    self.ejecutar_algoritmo("Round Robin.py")
                    return False

                elif self.boton_sjf.fue_clickeado(pos):
                    self.ejecutar_algoritmo("DemoSO_SJF_3.py")
                    return False

                elif self.boton_salir.fue_clickeado(pos):
                    return False

        return True

    def actualizar_hover(self):
        """Actualiza el estado hover de los botones."""
        pos_mouse = pygame.mouse.get_pos()
        for boton in [self.boton_prioridad, self.boton_fcfs, self.boton_rr, self.boton_sjf, self.boton_salir]:
            boton.actualizar_hover(pos_mouse)

    def ejecutar_algoritmo(self, archivo):
        """Ejecuta el algoritmo seleccionado."""
        try:
            pygame.quit()
            subprocess.Popen([sys.executable, archivo])
            sys.exit()
        except Exception as e:
            print(f"Error al ejecutar {archivo}: {e}")

    def ejecutar(self):
        """Bucle principal del menú."""
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar_hover()
            self.dibujar_menu_principal()
            pygame.display.flip()
            self.reloj.tick(60)
        pygame.quit()


def main():
    """Función principal de PlanificadorSim."""
    menu = MenuPrincipal()
    menu.ejecutar()


if __name__ == "__main__":
    main()
