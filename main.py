"""
main.py - Juego Farkle en consola.
Ejecutar: python main.py

# TODO: Agregar modo vs computadora
"""
from setup_archivos import GestorJuego
from dados_reglas import MotorDados
from logica_turno import DirectorJuego


def jugar_turno(director, motor):
    """Ejecuta el turno completo de un jugador."""
    nombre = director.jugador_actual()
    puntos_turno = 0
    dados_disp = 6
    print(f"\n── Turno de {nombre} ──")

    while True:
        input("Presiona ENTER para lanzar...")
        dados = motor.lanzar(dados_disp)
        print(f"🎲 Dados: {dados}")

        # Verificar Farkle
        if motor.es_farkle(dados):
            print("💀 ¡FARKLE! Pierdes los puntos del turno.")
            return 0

        pts, puntuan = motor.calcular_puntos(dados)
        print(f"💰 Puntos disponibles: {pts} (dados que puntúan: {puntuan})")
        puntos_turno += pts
        dados_disp -= len(puntuan)
        if dados_disp == 0:  # Hot dice
            print("🔥 ¡HOT DICE! Relanza los 6 dados")
            dados_disp = 6

        print(f"📊 Acumulado del turno: {puntos_turno}")
        # Decisión: seguir o plantarse
        try:
            opc = input("¿Sigues (s), te plantas (p) o abandonas (a)? ").strip().lower()
        except EOFError:
            return puntos_turno
        if opc == "p":
            return puntos_turno
        if opc == "a":
            return "ABANDONAR"
        # ------------------------------
    


def menu_historial(gestor):
    """Muestra historial y permite buscar por jugador."""
    if not gestor.historial:
        print("📭 No hay partidas guardadas.")
        return
    nombre = input("Buscar jugador (ENTER para ver todo): ").strip()
    partidas = gestor.buscar_jugador(nombre) if nombre else gestor.historial
    for i, p in enumerate(partidas, 1):
        print(f"\n#{i} {p['fecha']} → Ganó: {p['ganador']}")
        for n, pts in p["jugadores"].items():
            print(f"  • {n}: {pts}")


def main():
    """Función principal del juego."""
    print("\n🎲 ═══ FARKLE ═══ 🎲")
    print("""
    ===========================================
               REGLAS DE FARKLE
    ===========================================
    1. Lanza 6 dados para empezar.
    2. Debes acumular al menos un dado que sume puntos.
    3. Si no sacas puntos en un tiro, ¡es FARKLE! 
       Pierdes todo lo acumulado en el turno.
    4. Gana el primero en llegar a 10,000 puntos.
    ===========================================
    """)
    input("Presiona ENTER para comenzar...")

    gestor = GestorJuego()
    motor = MotorDados()

    # Menú: ver historial o jugar
    if gestor.historial:
        if input("¿Ver historial? (s/n): ").strip().lower() == "s":
            menu_historial(gestor)

    # Pedir cantidad de jugadores con try-except
    while True:
        try:
            n = int(input("\n¿Cuántos jugadores (2-6)? "))
            if 2 <= n <= 6:
                break
            print("Debe ser entre 2 y 6")
        except ValueError:
            print("Ingresa un número válido")

    # Pedir nombres
    nombres = [input(f"Nombre jugador {i+1}: ") for i in range(n)]
    res = gestor.crear_jugadores(nombres)
    if isinstance(res, str):  # Error de validación
        print(f"❌ {res}")
        return

    # Crear director e iniciar ciclo principal
    director = DirectorJuego(gestor, motor)

    # Ciclo principal del juego
    while not director.hay_ganador():
        # Mostrar marcador
        print("\n📋 MARCADOR:")
        for nom, pts in gestor.jugadores.items():
            marca = " ◀" if nom == director.jugador_actual() else ""
            print(f"  {nom}: {pts}{marca}")

# Jugar turno y verificar si decide abandonar
        puntos = jugar_turno(director, motor)
        
        if puntos == "ABANDONAR":
            nombre_fuera = director.jugador_actual()
            director.eliminar_jugador_actual() # <--- Aquí usas el método nuevo
            print(f"\n❌ {nombre_fuera} ha abandonado la partida.")
            
            if len(gestor.jugadores) == 0:
                print("🏁 No quedan jugadores. Fin del juego.")
                return # Sale de la función main
            continue # Salta al siguiente jugador sin ejecutar el resto del código

        # Si no abandonó, continúa normal
        nuevo = director.sumar_puntos(puntos)
        print(f"✅ {director.jugador_actual()} ahora tiene {nuevo} puntos")

        # Si no ganó, pasar al siguiente
        if not director.hay_ganador():
            director.siguiente()

    # Fin del juego: mostrar ganador y guardar
    ganador = director.jugador_actual()
    print(f"\n🏆 ¡{ganador} GANA con {gestor.jugadores[ganador]} puntos! 🏆")
    print("\n📊 Resultados finales:")
    for nom, pts in sorted(gestor.jugadores.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {nom}: {pts}")

    gestor.guardar()
    print("\n📁 Guardado en resultados.csv e historial.json")


if __name__ == "__main__":
    main()
