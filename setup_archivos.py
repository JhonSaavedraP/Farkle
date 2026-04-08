"""Rama 1: Jugadores y archivos (CSV/JSON)."""
import csv, json, os, re
from datetime import datetime


class GestorJuego:
    """Maneja jugadores, puntajes y archivos."""
    META = 10000  # Puntos para ganar

    def __init__(self):
        self.jugadores = {}   # {nombre: puntaje}
        self.historial = []   # Partidas pasadas
        # Cargar historial si existe el JSON
        try:
            if os.path.exists("historial.json"):
                with open("historial.json", encoding="utf-8") as f:
                    self.historial = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.historial = []

    def crear_jugadores(self, nombres):
        """Valida nombres con regex y crea dict con puntaje 0."""
        self.jugadores = {}
        for n in nombres:
            n = n.strip()
            # Validar con regex: letras, números y espacios (1-15)
            if not re.match(r"^[a-zA-Z0-9áéíóúñÑ ]{1,15}$", n):
                return f"'{n}' no es válido"
            if n in self.jugadores:
                return f"'{n}' está repetido"
            self.jugadores[n] = 0
        return self.jugadores

    def guardar(self):
        """Guarda resultados en CSV y JSON."""
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        ganador = max(self.jugadores, key=self.jugadores.get)
        # CSV
        try:
            nuevo = not os.path.exists("resultados.csv")
            with open("resultados.csv", "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                if nuevo:
                    w.writerow(["Fecha", "Jugador", "Puntaje"])
                for nom, pts in self.jugadores.items():
                    w.writerow([fecha, nom, pts])
        except IOError:
            pass
        # JSON
        self.historial.append({"fecha": fecha, "ganador": ganador,
                               "jugadores": dict(self.jugadores)})
        try:
            with open("historial.json", "w", encoding="utf-8") as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def buscar_jugador(self, nombre):
        """Busca partidas con un jugador (regex parcial)."""
        patron = re.compile(re.escape(nombre), re.IGNORECASE)
        return [p for p in self.historial
                if any(patron.search(j) for j in p["jugadores"])]
