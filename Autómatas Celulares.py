"""
Taller de programacion - Proyecto 1
Omar Zuñiga, José Manuel Granados, Maria Daniela Chaves
"""
from random import randint, choice
from copy import deepcopy
import pygame 
import json 

FILAS = 100 
COLS = 100
TAM = 7
if type(FILAS) != int or type(COLS) != int or type(TAM) != int:
    raise Exception("Las filas, las columnas y el tamaño deben ser un numero entero")
else:
    # - - - - - - - - - - - - - - - - - - - - - - - -
    #Subrutinas
    def crearMatriz(filas, columnas):
        """Función que crea una matriz acorde a las filas y columnas
        Entradas y restricciones
        filas: un n° entero
        columnas: un n° entero
        Salida:
        Matriz"""
        M = []
        for f in range(filas): 
            fila = []
            for c in range(columnas):
                fila.append(randint(0, 2))
            M.append(fila)
        return M 

    def crearMatrizNeutra(filas, columnas):
        """Función encargada de hacer una matriz vacía
        Entradas y restriciones:
        Entradas y restricciones
        filas: un n° entero
        columnas: un n° entero
        Salida:
        Matriz vacía"""
        M = []
        for f in range(filas): 
            fila = []
            for c in range(columnas):
                fila.append(0)
            M.append(fila)
        return M     

    def buscarVecinos(M, fila, col):
        """Función que se encarga de buscar los vecinos de cada célula
        Entradas y restricciones
        filas: un n° entero
        columnas: un n° entero
        Matriz
        Salida:
        los vecinos de cada cécula
        """
        filas = len(M)
        cols = len(M[0])
        vecinos = []

        for f in range(fila -1, fila + 2):
            for c in range(col - 1, col + 2):
                if f != fila or c != col: 
                    vecinos.append(M[f % filas][c % cols])
        return vecinos

    def guardarAutomata(M):
        """Funcion que se encarga de guardar una imagen de la matriz
        Entradaz y restricciones:
        M: matriz
        Salida:
        Dice si el arcgivo se guardó"""
        archivo = open("EsperemosQueEsteArchivoNoExista123.txt", "w")
        json.dump(M, archivo) #Guarda en el archivo M
        archivo.close()
        print("Archivo Guardado Exitosamente")

    def cargarAutomata():
        """Carga el automata desde un archivo guardado
        No hay entradas
        Salidas:
        Matriz"""
        global FILAS, COLS
        archivo = open("EsperemosQueEsteArchivoNoExista123.txt", "r")
        M = json.load(archivo)
        print(type(M))
        archivo.close()
        FILAS = len(M)
        COLS = len(M[0])
        print("Archivo Cargado Exitosamente")
        return M

    # - - - - - - - - - - - - - - - - - - - - - - - - 
    # El Cerebro de Brian: 
    def elCerebrodeBrian():
        """
        Subrutina la cual se encarga de generar la representacion del 
        Cerebro de Brian.
        No hay entradas
        Salidas:
        representación visual del cerebro de Brian.
        """
        pygame.init()
        window = pygame.display.set_mode((COLS * TAM, FILAS * TAM))
        loop=True
        pausa = False
        M = crearMatriz(FILAS,COLS)
        while loop:
            pygame.time.delay(16)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop=False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: #Pausa
                        pausa = not pausa
                    if keys[pygame.K_r]: #Reinicia la Matriz
                        M = crearMatriz(FILAS, COLS)
                    if keys[pygame.K_b]: #Vuelve la Matriz vacia
                        M = crearMatrizNeutra(FILAS, COLS)
                    if keys[pygame.K_g]:#Guarda la Matriz
                        print("Va a guardar")
                        guardarAutomata(M)
                    if keys[pygame.K_c]:#Carga la Matriz guardada
                        try:
                            M = cargarAutomata()
                        except: 
                            print("Archivo 'pruebasJson.txt no encontrado'")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    x, y = pygame.mouse.get_pos()
                    fila = y // TAM 
                    col = x // TAM 
                    if buttons[0]: #boton izquierdo solamente
                        cambiarCelulaBrian(M, fila, col, 1) 
                    if buttons[1]: 
                        cambiarCelulaBrian(M, fila, col, 0)
                    if buttons[2]: 
                        cambiarCelulaBrian(M, fila, col, 2)

            
            window.fill((0,0,0))
            dibujarMatrizBrian(M, window)
            pygame.display.update()
            if not pausa: 
                M = siguienteGenBrian(M)
        pygame.quit()

    def siguienteGenBrian(M):
        """
        Subrutina que hace la matriz que sigue en el cerebro de Brian acorde a
        sus reglas.
        Entradas y restricciones:
        Matriz vieja
        Salidas:
        Matriz nueva
        """
        M2 = deepcopy(M)
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                vecinos = buscarVecinos(M, f, c)
                #Regla #1 
                if M[f][c] == 0 and vecinos.count(1) == 2:
                    M2[f][c] = 1 
                #Regla #2 
                if M[f][c] == 1: 
                    M2[f][c] = 2
                #Regla #3
                if M[f][c] == 2: 
                    M2[f][c] = 0
        return M2

    def cambiarCelulaBrian(M,fila, col, num):
        """Función que cambia el estado de las células.
        Entradas y restricciones:
        Matriz(M)
        fila
        columna(col)
        estado de la celula(num)
        Salidas:
        Célula con otro estado
        """
        M[fila][col] = num

    def dibujarMatrizBrian(M,window):
        """Función que dibuja la matriz en pygame
        Entradas y rstricciones:
        Matriz(M)
        Ventana(window)
        Salidas:
        El estado de cada celula representado en la ventana."""
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                if M[f][c]==1:
                    pygame.draw.rect(window, (0,0,255), (c * TAM, f * TAM, TAM, TAM)) #Viva
                if M[f][c]==2: 
                    pygame.draw.rect(window, (255,0,0), (c * TAM, f * TAM, TAM, TAM)) #Muriendo
    # - - - - - - - - - - - - - - - - - - - - - - - - 
    # Automata celular ciclico: 
    def AutomataCelularCiclico():
        """Subrutina la cual se encarga de generar la representacion del automata
        Celular cíclico.
        No hay entradas
        Salidas:
        representación visual del automata celular cíclico."""
        pygame.init()
        window = pygame.display.set_mode((COLS * TAM, FILAS * TAM))
        loop = True
        pausa = False
        M = crearMatrizCiclico(FILAS, COLS)
        while loop: 
            pygame.time.delay(16)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop=False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: #Pausa
                        pausa = not pausa
                    if keys[pygame.K_r]: #Reinicia la Matriz
                        M = crearMatrizCiclico(FILAS, COLS)
                    if keys[pygame.K_b]: #Vuelve la Matriz vacia
                        M = crearMatrizNeutra(FILAS, COLS)
                    if keys[pygame.K_g]:#Guarda la Matriz
                        print("Va a guardar")
                        guardarAutomata(M)
                    if keys[pygame.K_c]:#Carga la Matriz guardada
                        try:
                            M = cargarAutomata()
                        except: 
                            print("Archivo 'pruebasJson.txt no encontrado'")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0]: #boton izquierdo solamente
                        x, y = pygame.mouse.get_pos()
                        fila = y // TAM 
                        col = x // TAM 
                        cambiarCelulaCiclico(M, fila, col) 

            window.fill((0,0,0))
            dibujarMatrizCiclico(M, window)
            pygame.display.update()
            if not pausa: 
                M = siguienteGenCiclico(M)
            
        pygame.quit()

    def crearMatrizCiclico(filas, columnas):
        """
        Subrutina que crea una matriz para el automata celular cíclico
        Entradas:
        filas: un n° entero
        columnas: un n° entero
        Salida:
        Matriz
        """
        M = []
        for f in range(filas): 
            fila = []
            for c in range(columnas):
                fila.append(randint(0, 15))
            M.append(fila)
        return M 

    def siguienteGenCiclico(M):
        """
        Subrutina que hace la siguiente generación de una matriz en
        automata celular cíclico.
        Entradas:
        Matriz(M) vieja
        Salidas
        Matriz nueva
        """
        M2 = deepcopy(M)
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                vecinos = buscarVecinos(M, f, c)
                if (M[f][c] + 1) % 16 in vecinos: 
                    M2[f][c] = (M[f][c] + 1) %16 
        return M2

    def cambiarCelulaCiclico(M,fila, col):
        """Función que cambia el estado de las células.
        Entradas y restricciones:
        Matriz(M)
        fila
        columna(col)
        estado de la celula(num)
        Salidas:
        Célula con otro estado
        """
        M[fila][col] = (M[fila][col] + 1) % 16

    def dibujarMatrizCiclico(M,window):
        """
        Función que se encarga de representar el automata celular ciclico en pygame.
        Entradas:
        Matriz(M)
        ventana(window)
        Salida:
        Automata representado en una ventana de pygame
        """
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                if M[f][c]==0:
                    pygame.draw.rect(window, (250,250,110), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==1: 
                    pygame.draw.rect(window, (217,242,113), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==2:
                    pygame.draw.rect(window, (185,233,118), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==3:
                    pygame.draw.rect(window, (156,223,124), (c * TAM, f * TAM, TAM, TAM))
                if M[f][c]==4:
                    pygame.draw.rect(window, (127,212,130), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==5:
                    pygame.draw.rect(window, (100,201,135), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==6:
                    pygame.draw.rect(window, (74,189,140), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==7:
                    pygame.draw.rect(window, (48,176,142), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==8:
                    pygame.draw.rect(window, (20,163,143), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==9:
                    pygame.draw.rect(window, (0,150,142), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==10:
                    pygame.draw.rect(window, (0, 137, 138), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==11:
                    pygame.draw.rect(window, (0, 123, 132), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==12:
                    pygame.draw.rect(window, (16, 110, 124), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==13:
                    pygame.draw.rect(window, (29, 97, 114), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==14:
                    pygame.draw.rect(window, (38, 84, 102), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==15:
                    pygame.draw.rect(window, (42, 72, 88) , (c * TAM, f * TAM, TAM, TAM)) 
            
    # - - - - - - - - - - - - - - - - - - - - - - - - 
    # Hormiga de Langton: 
    def HormigaDeLangton(Opcion = False):
        """Subrutina la cual se encarga de generar la representacion del automata
        Hormiga de Langton.
        Entradas y restricciones:
        opicón: es igual a False
        Salidas:
        representación visual de la Hormiga de Langton"""
        pygame.init()
        window = pygame.display.set_mode((COLS * TAM, FILAS * TAM))
        loop = True
        pausa = False
        if Opcion: 
            M = crearMatrizHormiga(FILAS, COLS)
        else: 
            M = crearMatrizNeutra(FILAS, COLS)
        posAnt = [[window.get_width() // (2*TAM), window.get_height() // (2*TAM)], 3]

        while loop: 
            pygame.time.delay(16)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop=False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: 
                        pausa = not pausa
                    if keys[pygame.K_r]:
                        if Opcion: 
                            M = crearMatrizHormiga(FILAS, COLS)
                        else: 
                            M = crearMatrizNeutra(FILAS, COLS)
                    if keys[pygame.K_b]: 
                        M = crearMatrizNeutra(FILAS, COLS)
                    if keys[pygame.K_g]:
                        print("Va a guardar")
                        guardarAutomata(M)
                    if keys[pygame.K_c]:
                        try:
                            M = cargarAutomata()
                        except: 
                            print("Archivo 'pruebasJson.txt no encontrado'")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0]: 
                        x, y = pygame.mouse.get_pos()
                        fila = y // TAM 
                        col = x // TAM 
                        cambiarCelulaAnt(M, fila, col) 
                    if buttons[2]:
                        x, y = pygame.mouse.get_pos()
                        fila = y // TAM 
                        col = x // TAM 
                        posAnt[0][0] = col
                        posAnt[0][1] = fila 

            window.fill((0,0,0))

            Hormiga(window, posAnt)
            dibujarMatrizAnt(M, window)

            pygame.display.update()
            if not pausa: 
                posAnt, M = NexHormiga(M, posAnt)
            
        pygame.quit()

    def crearMatrizHormiga(filas, columnas):
        """
        Función que crea la matriz para la Hormiga de Langton.
        Entradas:
        filas: un n° entero
        columnas: un n° entero
        Salida:
        Matriz
        """
        M = []
        for f in range(filas): 
            fila = []
            for c in range(columnas):
                fila.append(randint(0, 1))
            M.append(fila)
        return M 

    def Hormiga(window, pos):
        """Función que dibuja la "hormiga" en pygame
        Entradas:
        ventana(window)
        pos: posicion de la hormiga
        Salida:
        hormiga"""
        pygame.draw.rect(window, (0, 255, 0) , (pos[0][0] * TAM, pos[0][1] * TAM, TAM, TAM))

    def NexHormiga(M, posAnt):
        """Función para cambiar la hormiga en la siguiente generación
        Entradas:
        Matriz(M)
        posAnt: posicion de la hormiga
        Salida:
        hormiga cambiada en la siguiente generació"""
        M2 = deepcopy(M)
        x = [["valorx", "valory"], "direccion"]
        M[posAnt[0][1]][posAnt[0][0]] = (M[posAnt[0][1]][posAnt[0][0]] + 1) % 2

        if M2[posAnt[0][1]][posAnt[0][0]] == 0: 
            posAnt[1] = (posAnt[1] + 1) % 4 
        else: 
            posAnt[1] = (posAnt[1] - 1) % 4 
        
        return moveAnt(posAnt, M), M 

    def moveAnt(pos, M):
        """Funcion para saber hacia donde debe moverse la hormiga
        Entradas:
        Matrriz(M)
        posición de hormiga (pos)
        Salida:
        direccion"""
        if pos[1] == 0: 
            pos[0][1] = (pos[0][1] - 1) 
        if pos[1] == 1: 
            pos[0][0] = (pos[0][0] + 1) 
        if pos[1] == 2: 
            pos[0][1] = (pos[0][1] + 1) 
        if pos[1] == 3:  
            pos[0][0] = (pos[0][0] - 1) 
        
        pos[0][0] %= len(M[0])
        pos[0][1] %= len(M)
        return pos

    def dibujarMatrizAnt(M, window):
        """Función que dibuja la matriz de la Hormiga de Langton en pygame
        Entradas:
        Matriz(M)
        ventana(window)
        Salida:
        Automata representado en pygame"""
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                if M[f][c]==1: 
                    pygame.draw.rect(window, (135, 80, 171), (c * TAM, f * TAM, TAM, TAM)) 

    def cambiarCelulaAnt(M,fila, col):
        M[fila][col] = (M[fila][col] + 1) % 2

    # - - - - - - - - - - - - - - - - - - - - - - - - 
    # Modelo de tráfico Biham-Middleton-Levine
    def ModeloDeTrafico():
        """Subrutina la cual se encarga de generar la representacion del modelo
        de tráfico Biham-Middleton-Levine.
        No hay entradas
        Salidas:
        representación visual del modelo."""
        pygame.init()
        window = pygame.display.set_mode((COLS * TAM, FILAS * TAM))
        loop = True
        pausa = False
        M = crearMatrizTrafico(FILAS, COLS)
        i = 0
        while loop: 
            pygame.time.delay(16)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop=False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: #Pausa
                        pausa = not pausa
                    if keys[pygame.K_r]: #Reinicia la Matriz
                        M = crearMatrizTrafico(FILAS, COLS)
                    if keys[pygame.K_b]: #Vuelve la Matriz vacia
                        M = crearMatrizNeutra(FILAS, COLS)
                    if keys[pygame.K_g]:#Guarda la Matriz
                        print("Va a guardar")
                        guardarAutomata(M)
                    if keys[pygame.K_c]:#Carga la Matriz guardada
                        try:
                            M = cargarAutomata()
                        except: 
                            print("Archivo 'pruebasJson.txt no encontrado'")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    x, y = pygame.mouse.get_pos()
                    fila = y // TAM 
                    col = x // TAM 
                    if buttons[0]: #boton izquierdo solamente
                        cambiarCelulaTrafico(M, fila, col, 1) 
                    if buttons[1]: 
                        cambiarCelulaTrafico(M, fila, col, 0)
                    if buttons[2]:   
                        cambiarCelulaTrafico(M, fila, col, 2)

            window.fill((0,0,0))
            dibujarMatrizTrafico(M, window)
            pygame.display.update()
            if not pausa: 
                M = nextGenTrafico(M, i)
            i += 1
            i %= 2
        pygame.quit()

    def crearMatrizTrafico(filas, columnas):
        """
        Función que se encaraga de crear matriz para el modelo.
        Entradas:
        filas: un n° entero
        columnas: un n° entero
        Salida:
        Matriz
        """
        M = []
        for f in range(filas): 
            fila = [choice([0,0,0,1,2]) for x in range(columnas )]
            M.append(fila)
        return M 

    def dibujarMatrizTrafico(M, window):
        """
        Función que dibuja la matriz de modelo
        de tráfico Biham-Middleton-Levine en pygame.
        Entradas:
        Matriz(M)
        ventana(window)
        Salida:
        Modelo representado en pygame
        """
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                if M[f][c]==1: 
                    pygame.draw.rect(window, (0,0,255), (c * TAM, f * TAM, TAM, TAM)) 
                if M[f][c]==2: 
                    pygame.draw.rect(window, (255,0,0), (c * TAM, f * TAM, TAM, TAM)) 

    def nextGenTrafico(M, i):
        """
        Función que crea la suguiente generación.
        Entradas:
        Matriz(M)
        Estado de la celula(i)
        Salida:
        Matriz nueva.
        """
        M2 = deepcopy(M)
        filas = len(M)
        cols = len(M[0])
        for f in range(filas):
            for c in range(cols):
                if M2[f][c] == 1 and  M[(f+1)%filas][c] == 0 and i == 0: 
                    M[f][c] = 0
                    M[(f+1)%filas][c] = 1
                if M2[f][c] == 2 and M[f][(c+1)%cols] == 0 and i == 1:  
                    M[f][c] = 0 
                    M[f][(c+1)%cols] = 2
        return M

    def cambiarCelulaTrafico(M, fila, col, valor):
        M[fila][col] = valor

elCerebrodeBrian()
#AutomataCelularCiclico()
#ModeloDeTrafico()
#HormigaDeLangton(Opcion = False)
