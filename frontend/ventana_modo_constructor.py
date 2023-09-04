
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout,
    QVBoxLayout, QPushButton, QGridLayout
)
from frontend.botones import (BotonEstrella, BotonFantasmaHorizontal, BotonFantasmaVertical,
                              BotonFuego, BotonLuigi, BotonPared, BotonRoca, PlaceHolder)
import parametros as P


class VentanaModoConstructor(QWidget):

    senal_coordenadas = pyqtSignal(int, int)
    senal_boton_jugar = pyqtSignal(dict)
    senal_boton_limpiar = pyqtSignal()
    senal_cambiar_label = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botones = {
            'Luigi': BotonLuigi(self), 'Fuego': BotonFuego(self),
            'Estrella': BotonEstrella(self), 'Roca': BotonRoca(self),
            'Pared': BotonPared(self), 'FantasmaHorizontal': BotonFantasmaHorizontal(self),
            'FantasmaVertical': BotonFantasmaVertical(self)}
        self.init_gui()
        self.mostrar_todos()
        self.diccionario = {}
        self.diccionario_vacio()
        self.labels = {}
        self.contador = 1

    def init_gui(self):

        self.resize(550, 520)
        self.setMinimumSize(QtCore.QSize(550, 520))
        self.setMaximumSize(QtCore.QSize(550, 520))
        self.setWindowTitle('DCCazafantasmaC')
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            *P.RUTA_PERSONAJES, 'white_ghost_left_1.png')))

        self.label_coords = QLabel(self)
        self.label_coords.move(460, 490)
        self.label_coords.resize(110, 16)
        self.label_coords.setText("Pos:")

        self.setMouseTracking(True)

        self.selector = QtWidgets.QComboBox(self)
        self.selector.setGeometry(QtCore.QRect(10, 20, 180, 25))
        self.selector.addItems(['Todos', 'Entidades', 'Bloques'])
        self.selector.currentTextChanged.connect(self.seleccionar)

        self.boton_jugar = QPushButton(self)
        self.boton_jugar.setGeometry(QtCore.QRect(10, 420, 180, 25))
        self.boton_jugar.setText('Jugar')
        self.boton_jugar.clicked.connect(self.empezar_partida)

        self.boton_limpiar = QPushButton(self)
        self.boton_limpiar.setGeometry(QtCore.QRect(10, 460, 180, 25))
        self.boton_limpiar.setText('Limpiar')
        self.boton_limpiar.clicked.connect(self.reiniciar)

        self.label_sel_txt = QLabel(self)
        self.label_sel_txt.setGeometry(QtCore.QRect(30, 380, 80, 18))
        self.label_sel_txt.setText("Seleccionado: ")
        self.label_sel_txt.show()
        self.label_seleccionado = QLabel(self)
        self.label_seleccionado.setGeometry(QtCore.QRect(120, 370, 30, 30))
        self.label_seleccionado.show()

        for boton in self.botones.values():
            boton.clicked.connect(self.cambiar_label_seleccionado)

        self.entidad_seleccionada = PlaceHolder()

        self.crear_tablero()
        # self.show()

    def cambiar_label_seleccionado(self):
        self.entidad_seleccionada = self.sender()
        self.label_seleccionado.setPixmap(QtGui.QPixmap(
            self.entidad_seleccionada.pixmap_path))
        self.label_seleccionado.setScaledContents(True)

    def mouseMoveEvent(self, event) -> None:
        objeto_pos = event.pos()
        self.label_coords.setText(f'Pos: {objeto_pos.x()}, {objeto_pos.y()}')

    def mousePressEvent(self, event) -> None:
        posX = (event.x() - 240) // 30
        posY = (event.y() - 40) // 30
        if 240 < event.x() < 510 and 40 < event.y() < 460:
            self.senal_coordenadas.emit(posX, posY)
            self.label_coords.setText(f'{posX}, {posY}')

            if self.diccionario[posX, posY] == "-":
                if self.entidad_seleccionada.cantidad == 0:
                    self.entidad_seleccionada = PlaceHolder(self)
                    self.label_seleccionado.setPixmap(QtGui.QPixmap())

                else:
                    label = QLabel(self)
                    label.setPixmap(QtGui.QPixmap(
                        self.entidad_seleccionada.pixmap_path))
                    label.setGeometry(240 + 30 * posX, 40 + 30 * posY, 30, 30)
                    label.setScaledContents(True)
                    label.show()
                    self.labels[self.contador] = label

                    self.contador += 1
                    self.entidad_seleccionada.poner_boton()
                    self.diccionario[posX, posY] = self.entidad_seleccionada.id

    def mostrar_ventana(self):
        self.show()

    def seleccionar(self, opcion):
        if opcion == "Todos":
            self.mostrar_todos()
        elif opcion == "Entidades":
            self.mostrar_entidades()
        else:
            self.mostrar_bloques()

    def esconder_ventana(self):
        self.hide()

    def crear_tablero(self):
        origenX = 240
        origenY = 40
        for i in range(14):
            for j in range(9):
                casilla = QLabel(self)
                casilla.setMouseTracking(True)
                casilla.setGeometry(QtCore.QRect(0, 0, 30, 30))
                casilla.setStyleSheet("background-color: rgb(94, 94, 94);")
                casilla.setFrameShape(QtWidgets.QFrame.Panel)
                casilla.setFrameShadow(QtWidgets.QFrame.Raised)
                casilla.setLineWidth(3)
                casilla.setText("")
                casilla.move(30 * j + origenX, origenY)
                casilla.show()

            origenY += 30

        for i in range(16):
            for j in range(11):
                if i == 0:
                    muro = QLabel(self)
                    muro.setMouseTracking(True)
                    muro.setGeometry(QtCore.QRect(0, 0, 30, 30))
                    muro.setPixmap(QtGui.QPixmap(os.path.join(
                        *P.RUTA_ELEMENTOS, 'bordermap.png')))
                    muro.move(30*j + 210, 10)

                elif i == 15:
                    muro = QLabel(self)
                    muro.setMouseTracking(True)
                    muro.setGeometry(QtCore.QRect(0, 0, 30, 30))
                    muro.setPixmap(QtGui.QPixmap(os.path.join(
                        *P.RUTA_ELEMENTOS, 'bordermap.png')))
                    muro.move(30*j + 210, 460)

                else:
                    if j == 0:
                        muro = QLabel(self)
                        muro.setMouseTracking(True)
                        muro.setGeometry(QtCore.QRect(0, 0, 30, 30))
                        muro.setPixmap(QtGui.QPixmap(os.path.join(
                            *P.RUTA_ELEMENTOS, 'bordermap.png')))
                        muro.move(210, i * 30 + 10)

                    elif j == 10:
                        muro = QLabel(self)
                        muro.setMouseTracking(True)
                        muro.setGeometry(QtCore.QRect(0, 0, 30, 30))
                        muro.setPixmap(QtGui.QPixmap(os.path.join(
                            *P.RUTA_ELEMENTOS, 'bordermap.png')))
                        muro.move(510, i * 30 + 10)

    def mostrar_todos(self):
        self.esconder_botones()
        self.botones['Pared'].move(10, 50)
        self.botones['Pared'].show()
        self.botones['Estrella'].move(10, 90)
        self.botones['Estrella'].show()
        self.botones['Roca'].move(10, 130)
        self.botones['Roca'].show()
        self.botones['Fuego'].move(10, 170)
        self.botones['Fuego'].show()
        self.botones['Luigi'].move(10, 210)
        self.botones['Luigi'].show()
        self.botones['FantasmaVertical'].move(10, 250)
        self.botones['FantasmaVertical'].show()
        self.botones['FantasmaHorizontal'].move(10, 290)
        self.botones['FantasmaHorizontal'].show()

    def mostrar_entidades(self):
        self.esconder_botones()
        self.botones['Luigi'].move(10, 50)
        self.botones['Luigi'].show()
        self.botones['FantasmaVertical'].move(10, 90)
        self.botones['FantasmaVertical'].show()
        self.botones['FantasmaHorizontal'].move(10, 130)
        self.botones['FantasmaHorizontal'].show()

    def mostrar_bloques(self):
        self.esconder_botones()
        self.botones['Pared'].move(10, 50)
        self.botones['Pared'].show()
        self.botones['Estrella'].move(10, 90)
        self.botones['Estrella'].show()
        self.botones['Roca'].move(10, 130)
        self.botones['Roca'].show()
        self.botones['Fuego'].move(10, 170)
        self.botones['Fuego'].show()

    def esconder_botones(self):
        for boton in self.botones.values():
            boton.hide()

    def diccionario_vacio(self):

        for fila in range(P.ANCHO_GRILLA - 2):
            for columna in range(P.LARGO_GRILLA - 2):
                self.diccionario[(fila, columna)] = '-'

    def reiniciar(self):
        for label in self.labels.values():
            label.hide()
        self.diccionario_vacio()
        for boton in self.botones.values():
            boton.reiniciar()
        self.labels = {}
        self.contador = 1

    def empezar_partida(self):
        print("se apreto el boton de jugar voy a esconder Ventana Modo constructor")
        self.senal_boton_jugar.emit(self.diccionario)
        self.esconder_ventana()
