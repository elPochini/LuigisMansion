import os
from PyQt5.QtCore import pyqtSignal, QObject
import parametros as P


class VentanaInicioBackend(QObject):
    senal_mensaje_error = pyqtSignal()
    senal_empezar_juego = pyqtSignal()
    senal_nuevo_juego = pyqtSignal()
    senal_cargar_juego = pyqtSignal(dict)
    senal_mostrar_juego = pyqtSignal()
    senal_modo_constructor = pyqtSignal()
    senal_nombre_usuario = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    def verificar_usuario(self, nombre_usuario):

        if P.MIN_CARACTERES < len(nombre_usuario) < P.MAX_CARACTERES:
            self.senal_empezar_juego.emit()
            self.senal_nombre_usuario.emit(nombre_usuario)
        else:
            self.senal_mensaje_error.emit()

    def selector_tipo_juego(self, nombre_partida):

        ### MODO CONSTRUCTOR ###
        if nombre_partida == 'Modo Constructor':
            self.senal_modo_constructor.emit()

        ### TABLERO LISTO ###
        else:
            dicc = abrir_tablero(nombre_partida)
            self.senal_cargar_juego.emit(dicc)
            self.senal_mostrar_juego.emit()


def abrir_tablero(nombre_archivo: str) -> list:
    """
    Abre un archivo sin el txt y lo carga desde la carpeta de mapas y
    devuelve un dict
    """
    diccionario = {'Estrella': (), 'Pared': [], 'Fuego': [],
                   'Roca': [], 'FantasmaH': [], 'FantasmaV': []}

    with open(os.path.join('backend', 'utilidades', 'mapas', nombre_archivo + '.txt'), 'r') as mapa:
        lineas = mapa.readlines()
        tablero = []

        for linea in lineas:
            tablero.append(linea.strip())
    print(tablero[0])
    for fila in range(14):
        for columna in range(9):
            print(tablero[fila][columna])
            if tablero[fila][columna] == '-':
                pass
            elif tablero[fila][columna] == 'L':
                diccionario['Luigi'] = (columna, fila)
            elif tablero[fila][columna] == 'F':
                diccionario['Fuego'].append((columna, fila))
            elif tablero[fila][columna] == 'S':
                diccionario['Estrella'] = (columna, fila)
            elif tablero[fila][columna] == 'R':
                diccionario['Roca'].append((columna, fila))
            elif tablero[fila][columna] == 'P':
                diccionario['Pared'].append((columna, fila))
            elif tablero[fila][columna] == 'V':
                diccionario['FantasmaV'].append((columna, fila))
            elif tablero[fila][columna] == 'H':
                diccionario['FantasmaH'].append((columna, fila))

    return diccionario
