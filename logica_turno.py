"""Rama 3: Control de turnos y rondas."""
from setup_archivos import GestorJuego

class DirectorJuego:
    """Dirige el flujo: turnos, rondas y victoria."""

    def __init__(self, gestor, motor):
        # Aquí recibimos los objetos de las otras ramas (Inyección de Dependencias).
        # El Director no hace los puntos solo, usa al 'gestor' y al 'motor'.
        self.gestor = gestor   
        self.motor = motor     
        self.idx = 0           # El índice controla la posición en la lista de jugadores.
        self.ronda = 1

    def jugador_actual(self):
        """Retorna nombre del jugador en turno."""
        #Convertimos las llaves del diccionario en lista para usar el índice actual.
        return list(self.gestor.jugadores.keys())[self.idx]

    def siguiente(self):
        """Pasa al siguiente jugador. Si pasaron todos, nueva ronda."""
        # Usamos el operador módulo (%) para que el turno sea circular.
        # Cuando el índice vuelve a 0, significa que todos ya jugaron y sube la ronda.
        total = len(self.gestor.jugadores)
        self.idx = (self.idx + 1) % total
        if self.idx == 0:
            self.ronda += 1

    def sumar_puntos(self, puntos):
        """Suma puntos al jugador actual y retorna su total."""
        #Convertimos las llaves del diccionario en lista para usar el índice actual.
        nombre = self.jugador_actual()
        self.gestor.jugadores[nombre] += puntos
        return self.gestor.jugadores[nombre]

    def hay_ganador(self):
        """True si el jugador actual llegó a 10,000."""
        #Convertimos las llaves del diccionario en lista para usar el índice actual.
        return self.gestor.jugadores[self.jugador_actual()] >= GestorJuego.META
    
    def eliminar_jugador_actual(self):
        """Elimina al jugador actual de la partida y ajusta el índice."""
        #Convertimos las llaves del diccionario en lista para usar el índice actual.
        nombre = self.jugador_actual()
        
        # 1. Limpieza de datos: Lo borramos del diccionario global.
        if nombre in self.gestor.jugadores:
            del self.gestor.jugadores[nombre]
        
        # 2. Control de errores (Índice): 
        # Si borramos al último jugador, el índice quedaría apuntando al vacío.
        # Reiniciamos a 0 si es necesario para evitar que el programa se detenga por error.
        if self.idx >= len(self.gestor.jugadores):
            self.idx = 0