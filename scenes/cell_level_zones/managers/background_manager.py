# scenes/cell_level_zones/managers/background_manager.py
import pygame
import os

class BackgroundManager:
    def __init__(self, screen, ruta_fondo="assets/backgrounds/background_1.png", velocidad=2):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.background_y = 0  
        self.background_speed = velocidad  
        self.original_background_speed = velocidad  
        
        self.fondo_y = 0
        self.velocidad_fondo = velocidad
        self.velocidad_original = velocidad
        self.ruta_fondo = ruta_fondo
        
        self.fondo = self._cargar_fondo()

        self.en_transicion = False
        self.alpha_overlay = 0
        self.overlay_surface = pygame.Surface(self.screen.get_size())
        self.overlay_surface.fill((0, 0, 0))
        self.transicion_callback = None
        self.transicion_tipo = None
        
    def _cargar_fondo(self):
        if not os.path.exists(self.ruta_fondo):
            print(f"Advertencia: Archivo de fondo no encontrado: {self.ruta_fondo}")
            return None
            
        try:
            fondo = pygame.image.load(self.ruta_fondo).convert()
            fondo = pygame.transform.scale(fondo, self.screen_rect.size)
            return fondo
        except pygame.error as e:
            print(f"Error al cargar imagen de fondo: {e}")
            return None
    
    def actualizar_fondo(self, dt=1):
        self.background_speed = self.velocidad_fondo  
        self.background_y += self.background_speed * dt
        self.fondo_y = self.background_y  
    
    def update_background(self, dt=1):
        self.actualizar_fondo(dt)
    
    def dibujar_fondo(self):
        if self.fondo:
            altura_fondo = self.fondo.get_height()
            offset = self.background_y % altura_fondo
            
            self.screen.blit(self.fondo, (0, offset - altura_fondo))
            self.screen.blit(self.fondo, (0, offset))
        else:
            self.screen.fill((20, 20, 40)) 
    
    def draw_background(self):
        self.dibujar_fondo()

        if self.en_transicion:
            if self.transicion_tipo == "oscurecer":
                self.alpha_overlay += 5
                if self.alpha_overlay >= 255:
                    self.alpha_overlay = 255
                    self.en_transicion = False
                    if self.transicion_callback:
                        self.transicion_callback()
                        # Después del callback (cambiar fondo), iniciamos "aclarar"
                        self.iniciar_transicion("aclarar")
            elif self.transicion_tipo == "aclarar":
                self.alpha_overlay -= 5
                if self.alpha_overlay <= 0:
                    self.alpha_overlay = 0
                    self.en_transicion = False

            self.overlay_surface.set_alpha(self.alpha_overlay)
            self.screen.blit(self.overlay_surface, (0, 0))
    
    def establecer_velocidad(self, velocidad):
        self.velocidad_fondo = velocidad
        self.background_speed = velocidad  
    
    def resetear_velocidad(self):
        self.velocidad_fondo = self.velocidad_original
        self.background_speed = self.velocidad_original
        self.original_background_speed = self.velocidad_original
    
    def pausar_fondo(self):
        self.velocidad_fondo = 0
        self.background_speed = 0
    
    def reanudar_fondo(self):
        self.velocidad_fondo = self.velocidad_original
        self.background_speed = self.velocidad_original
    
    def resetear_posicion(self):
        self.fondo_y = 0
        self.background_y = 0
    
    def cambiar_fondo(self, nueva_ruta_fondo):
        ruta_anterior = self.ruta_fondo
        self.ruta_fondo = nueva_ruta_fondo
        nuevo_fondo = self._cargar_fondo()
        
        if nuevo_fondo:
            self.fondo = nuevo_fondo
        else:
            self.ruta_fondo = ruta_anterior
            print(f"Error al cambiar fondo, manteniendo actual: {ruta_anterior}")
    
    def obtener_progreso_scroll(self):
        if self.fondo:
            altura_fondo = self.fondo.get_height()
            return (self.background_y % altura_fondo) / altura_fondo * 100
        return 0
    
    @property
    def altura_fondo(self):
        return self.fondo.get_height() if self.fondo else 0
    
    @property
    def esta_pausado(self):
        return self.background_speed == 0
    
    def sincronizar_velocidades(self):
        self.background_speed = self.velocidad_fondo
        self.original_background_speed = self.velocidad_original
    
    def sincronizar_posiciones(self):
        self.background_y = self.fondo_y
    
    def iniciar_transicion(self, tipo="oscurecer", callback=None):
        self.en_transicion = True
        self.transicion_tipo = tipo
        self.transicion_callback = callback
        self.alpha_overlay = 0 if tipo == "oscurecer" else 255

    def change_end_background(self):
        def aplicar_cambio():
            self.cambiar_fondo("assets/backgrounds/escen_004.png")

        self.iniciar_transicion("oscurecer", aplicar_cambio)