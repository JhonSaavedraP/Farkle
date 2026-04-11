"""Rama 2: Dados, puntuación y Farkle."""
import random #Se usa para generar números aleatorios
from collections import Counter #cuenta cuántas veces aparece cada número en una lista.

class MotorDados: # Lógica de dados y puntuación del Farkle.

    def lanzar(self, cantidad): #Lanza los dados y devuelve una lista con los resultados.
        return [random.randint(1, 6) for _ in range(cantidad)]

    def calcular_puntos(self, dados): # aqui se calcula el puntaje total y una lista de los dados . 
    # valores  1=100, 5=50, trío 1=1000, trío N=N*100, escalera=1500, 3 pares=1500.

        if not dados: # si no hay dados 0
            return 0, []
        conteo = Counter(dados)
        
        if len(dados) == 6 and set(dados) == {1, 2, 3, 4, 5, 6}: # aqui vemos la logica de la escalera completa 
            return 1500, list(dados)                                # usando len y set 
       
        if len(dados) == 6 and len(conteo) == 3 and all(c == 2 for c in conteo.values()):  # para Tres pares debemos tener 6 dados por eso el len al inico 
            return 1500, list(dados)                               # usando len y all para verificar que cada número aparezca exactamente dos veces.
      
        puntos, puntuan = 0, []
        for val, cant in conteo.items(): # si no hacemos 3 pares usamos la logica de  val es el número del dado y cant es cuántas veces salió
            if cant >= 3:
                base = 1000 if val == 1 else val * 100 #aqui vemos la logica para el 1 y todos los demas numeros que hacen trio
                puntos += base * (2 ** (cant - 3))  # aqui como se calcula todos los puntos de los trios y si hay más de 3 dados iguales se multiplica 
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