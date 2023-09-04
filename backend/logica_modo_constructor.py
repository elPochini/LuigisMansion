
from PyQt5.QtCore import pyqtSignal, QObject
import parametros as P


class VentanaModoConstructorBackend(QObject):
    senal_username = pyqtSignal(str)
    senal_parametros_Constructor = pyqtSignal(dict)
    senal_iniciar_juego_Constructor = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.nombre_usuario = ""
        self.Luigi = None
        self.coord_estrella = ()
        self.fantasmas_ver = []
        self.fantasmas_hor = []
        self.paredes = []
        self.fuegos = []
        self.rocas = []

    def generar_partida(self, diccionario):

        for fila in range(P.ANCHO_GRILLA - 2):
            for columna in range(P.LARGO_GRILLA - 2):
                if diccionario[(fila, columna)] == "-":
                    pass
                elif diccionario[(fila, columna)] == "L":
                    self.Luigi = fila, columna
                elif diccionario[(fila, columna)] == "F":
                    self.fuegos.append((fila, columna))
                elif diccionario[(fila, columna)] == "S":
                    self.coord_estrella = (fila, columna)
                elif diccionario[(fila, columna)] == "R":
                    self.rocas.append((fila, columna))
                elif diccionario[(fila, columna)] == "P":
                    self.paredes.append((fila, columna))
                elif diccionario[(fila, columna)] == "V":
                    self.fantasmas_ver.append((fila, columna))
                elif diccionario[(fila, columna)] == "H":
                    self.fantasmas_hor.append((fila, columna))

        dict_juego = {'Luigi': self.Luigi, 'Estrella': self.coord_estrella, 'Pared': self.paredes,
                      'Fuego': self.fuegos, 'Roca': self.rocas, 'FantasmaH': self.fantasmas_hor,
                      'FantasmaV': self.fantasmas_ver}

        self.senal_parametros_Constructor.emit(dict_juego)
        self.senal_iniciar_juego_Constructor.emit()
