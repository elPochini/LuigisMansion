import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import parametros as P


class BotonLuigi(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(*P.RUTA_PERSONAJES, 'luigi_front.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = 1
        self.id = 'L'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = 1
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class PlaceHolder(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = ''

        self.cantidad = 200
        self.id = '-'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = 2000
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonFantasmaHorizontal(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(
            *P.RUTA_PERSONAJES, 'white_ghost_left_1.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = P.MAXIMO_FANTASMAS_HORIZONTAL
        self.id = 'H'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = P.MAXIMO_FANTASMAS_HORIZONTAL
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonFantasmaVertical(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(
            *P.RUTA_PERSONAJES, 'red_ghost_vertical_1.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = P.MAXIMO_FANTASMAS_VERTICAL
        self.id = 'V'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = P.MAXIMO_FANTASMAS_VERTICAL
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonPared(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(*P.RUTA_ELEMENTOS, 'wall.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = P.MAXIMO_PARED
        self.id = 'P'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = P.MAXIMO_PARED
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonEstrella(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(*P.RUTA_ELEMENTOS, 'osstar.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = 1
        self.id = 'S'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = 1
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonRoca(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(*P.RUTA_ELEMENTOS, 'rock.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = P.MAXIMO_ROCA
        self.id = 'R'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = P.MAXIMO_ROCA
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')


class BotonFuego(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap_path = os.path.join(*P.RUTA_ELEMENTOS, 'fire.png')
        self.setIcon(QtGui.QIcon(self.pixmap_path))
        self.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.cantidad = P.MAXIMO_FUEGO
        self.id = 'F'
        self.setText(f'({self.cantidad})')
        self.hide()

    def reiniciar(self):
        self.cantidad = P.MAXIMO_FUEGO
        self.setDisabled(False)
        self.setText(f'({self.cantidad})')

    def poner_boton(self):
        self.cantidad -= 1
        if self.cantidad == 0:
            self.setDisabled(True)

        self.setText(f'({self.cantidad})')
