"""Rama 2: Dados, puntuación y Farkle."""
import random
from collections import Counter


class MotorDados:
# Lógica de dados y puntuación del Farkle.

    def lanzar(self, cantidad):
    #Lanza N dados (1-6). Retorna lista.
        return [random.randint(1, 6) for _ in range(cantidad)]

    def calcular_puntos(self, dados):
    
# valores  1=100, 5=50, trío 1=1000, trío N=N*100, escalera=1500, 3 pares=1500.

        if not dados:
            return 0, []
        conteo = Counter(dados)
        # Escalera completa
        if len(dados) == 6 and set(dados) == {1, 2, 3, 4, 5, 6}:
            return 1500, list(dados)
        # Tres pares
        if len(dados) == 6 and len(conteo) == 3 and all(c == 2 for c in conteo.values()):
            return 1500, list(dados)
        # Evaluar cada valor
        puntos, puntuan = 0, []
        for val, cant in conteo.items():
            if cant >= 3:
                base = 1000 if val == 1 else val * 100
                puntos += base * (2 ** (cant - 3)) 
                puntuan.extend([val] * cant)
            elif val == 1:
                puntos += cant * 100
                puntuan.extend([1] * cant)
            elif val == 5:
                puntos += cant * 50
                puntuan.extend([5] * cant)
        return puntos, puntuan

    def es_farkle(self, dados):
        """True si ningún dado puntúa."""
        return self.calcular_puntos(dados)[0] == 0