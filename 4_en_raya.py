# Juego de 4 en raya
# Autor: Rodrigo Torrealba

# Importar librerias
import random

# Definir funciones
def imprimir_tablero(tablero):
    for fila in tablero:
        print(fila)

def crear_tablero(filas=6, columnas=7):
    tablero = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(0)
        tablero.append(fila)
    return tablero

def tirar_ficha(tablero, columna, jugador):
    for fila in range(len(tablero)-1, -1, -1):
        if tablero[fila][columna] == 0:
            tablero[fila][columna] = jugador
            return tablero, True
    return tablero, False

def revisar_ganador(tablero, jugador):
    # Revisar filas
    for fila in tablero:
        contador = 0
        for columna in fila:
            if columna == jugador:
                contador += 1
                if contador == 4:
                    return True
            else:
                contador = 0
    # Revisar columnas
    for columna in range(len(tablero[0])):
        contador = 0
        for fila in range(len(tablero)):
            if tablero[fila][columna] == jugador:
                contador += 1
                if contador == 4:
                    return True
            else:
                contador = 0
    # Revisar diagonales
    for fila in range(len(tablero)-3):
        for columna in range(len(tablero[0])-3):
            contador = 0
            for i in range(4):
                if tablero[fila+i][columna+i] == jugador:
                    contador += 1
                    if contador == 4:
                        return True
                else:
                    contador = 0
    for fila in range(len(tablero)-3):
        for columna in range(3, len(tablero[0])):
            contador = 0
            for i in range(4):
                if tablero[fila+i][columna-i] == jugador:
                    contador += 1
                    if contador == 4:
                        return True
                else:
                    contador = 0
    return False

def revisar_empate(tablero):
    for fila in tablero:
        for columna in fila:
            if columna == 0:
                return False
    return True

def reiniciar_tablero(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            tablero[fila][columna] = 0
    return tablero

def puntuacion(tablero, jugador):
    # Revisar filas
    puntuacion = 0
    for fila in tablero:
        contador = 0
        for columna in fila:
            if columna == jugador:
                contador += 1
            else:
                contador = 0
            if contador == 2:
                puntuacion += 1
            elif contador == 3:
                puntuacion += 10
    # Revisar columnas
    for columna in range(len(tablero[0])):
        contador = 0
        for fila in range(len(tablero)):
            if tablero[fila][columna] == jugador:
                contador += 1
            else:
                contador = 0
            if contador == 2:
                puntuacion += 1
            elif contador == 3:
                puntuacion += 10
    # Revisar diagonales
    for fila in range(len(tablero)-3):
        for columna in range(len(tablero[0])-3):
            contador = 0
            for i in range(4):
                if tablero[fila+i][columna+i] == jugador:
                    contador += 1
                else:
                    contador = 0
                if contador == 2:
                    puntuacion += 1
                elif contador == 3:
                    puntuacion += 10
    for fila in range(len(tablero)-3):
        for columna in range(3, len(tablero[0])):
            contador = 0
            for i in range(4):
                if tablero[fila+i][columna-i] == jugador:
                    contador += 1
                else:
                    contador = 0
                if contador == 2:
                    puntuacion += 1
                elif contador == 3:
                    puntuacion += 10
    return puntuacion

def minimax(tablero, jugador, profundidad):
    # Regresa la columna que maximiza la puntuacion

    if jugador == 1:
        oponente = 2
    else:
        oponente = 1

    if profundidad == 0 or revisar_ganador(tablero, jugador) or revisar_ganador(tablero, oponente) or revisar_empate(tablero):
        return puntuacion(tablero, jugador)
    
    if jugador == 1:
        maximo = -100
        for columna in range(len(tablero[0])):
            copia_tablero = [fila[:] for fila in tablero]
            copia_tablero, valido = tirar_ficha(copia_tablero, columna, jugador)
            if valido:
                puntuacion_actual = minimax(copia_tablero, oponente, profundidad-1)
                if puntuacion_actual > maximo:
                    maximo = puntuacion_actual
                    mejor_columna = columna
        return maximo
    
    else:
        minimo = 100
        for columna in range(len(tablero[0])):
            copia_tablero = [fila[:] for fila in tablero]
            copia_tablero, valido = tirar_ficha(copia_tablero, columna, jugador)
            if valido:
                puntuacion_actual = minimax(copia_tablero, oponente, profundidad-1)
                if puntuacion_actual < minimo:
                    minimo = puntuacion_actual
                    mejor_columna = columna
        return minimo
    
def tirar_ficha_maquina(tablero, jugador):
    profundidad = 4
    if jugador == 1:
        oponente = 2
    else:
        oponente = 1
    maximo = -100
    mejor_columna = random.randint(0, len(tablero[0])-1)
    for columna in range(len(tablero[0])):
        copia_tablero = [fila[:] for fila in tablero]
        copia_tablero, valido = tirar_ficha(copia_tablero, columna, jugador)
        if valido:
            puntuacion_actual = minimax(copia_tablero, oponente, profundidad-1)
            if puntuacion_actual > maximo:
                maximo = puntuacion_actual
                mejor_columna = columna
    tablero, valido = tirar_ficha(tablero, mejor_columna, jugador)
    return tablero, valido

# Programa principal
tablero = crear_tablero()
imprimir_tablero(tablero)
jugadores = [1, 2]
random.shuffle(jugadores)
turno = 0
while True:
    jugador = jugadores[turno]
    print("Turno del jugador", jugador)
    if jugador == 1:
        columna = int(input("Ingrese la columna: "))
        tablero, valido = tirar_ficha(tablero, columna-1, jugador)
    else:
        tablero, valido = tirar_ficha_maquina(tablero, jugador)
    if valido:
        imprimir_tablero(tablero)
        if revisar_ganador(tablero, jugador):
            print("El jugador", jugador, "gano!")
            break
        elif revisar_empate(tablero):
            print("Empate!")
            break
        turno = (turno + 1) % 2
    else:
        print("Columna invalida")
        turno = (turno + 1) % 2

        

# Fin del programa
        

