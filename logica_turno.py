"""Rama 3: Control de turnos y rondas."""
from setup_archivos import GestorJuego


class DirectorJuego:
    """Dirige el flujo: turnos, rondas y victoria."""

    def __init__(self, gestor, motor):
        self.gestor = gestor   # Rama 1
        self.motor = motor     # Rama 2
        self.idx = 0           # Jugador actual
        self.ronda = 1

    def jugador_actual(self):
        """Retorna nombre del jugador en turno."""
        return list(self.gestor.jugadores.keys())[self.idx]

    def siguiente(self):
        """Pasa al siguiente jugador. Si pasaron todos, nueva ronda."""
        total = len(self.gestor.jugadores)
        self.idx = (self.idx + 1) % total
        if self.idx == 0:
            self.ronda += 1

    def sumar_puntos(self, puntos):
        """Suma puntos al jugador actual y retorna su total."""
        nombre = self.jugador_actual()
        self.gestor.jugadores[nombre] += puntos
        return self.gestor.jugadores[nombre]

    def hay_ganador(self):
        """True si el jugador actual llegó a 10,000."""
        return self.gestor.jugadores[self.jugador_actual()] >= GestorJuego.META
    
    def eliminar_jugador_actual(self):
        """Elimina al jugador actual de la partida y ajusta el índice."""
        nombre = self.jugador_actual()
        
        # 1. Eliminar del diccionario de datos (GestorJuego)
        if nombre in self.gestor.jugadores:
            del self.gestor.jugadores[nombre]
        
        # 2. Ajustar el índice
        # Si el jugador que se va es el último de la lista, volvemos al inicio (0)
        # Si no, el índice se queda igual porque el "siguiente" ahora ocupa esa posición
        if self.idx >= len(self.gestor.jugadores):
            self.idx = 0