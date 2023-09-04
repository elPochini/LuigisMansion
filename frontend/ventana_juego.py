import sys
import os
import time
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QObject, QPropertyAnimation, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout,
    QVBoxLayout, QPushButton, QGridLayout, QShortcut, QMessageBox
)
import parametros as P
from backend.utilidades import misc as M


dict_direcciones = {'derecha': (0, 1), 'izquierda': (0, -1),
                    'abajo': (1, 0), 'arriba': (-1, 0)}


class VentanaJuego(QWidget):

    senal_teclas = pyqtSignal(dict)
    senal_check_win = pyqtSignal()
    senal_timeout = pyqtSignal()
    senal_KIL = pyqtSignal()
    senal_INF = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tiempo_restante = P.TIEMPO_CUENTA_REGRESIVA
        self.init_gui()

    def init_gui(self):
        self.resize(550, 520)
        self.setMinimumSize(QtCore.QSize(550, 520))
        self.setMaximumSize(QtCore.QSize(550, 520))
        self.setWindowTitle('DCCazafantasmaG')
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            *P.RUTA_PERSONAJES, 'white_ghost_left_1.png')))
        self.crear_tablero()
        self.bloquear_teclado = False
        self.tiempo_bloqueo = 150
        self.lista_labels_roca = []
        self.labels_fantasmas_ver = {}
        self.labels_fantasmas_hor = {}
        self.INF_activo = False
        self.label_tiempo()
        self.label_vida()

        # self.show()

        self.shortcut_KIL = QShortcut(QKeySequence(
            Qt.Key.Key_K, Qt.Key.Key_I, Qt.Key.Key_L), self)
        self.shortcut_KIL.activated.connect(self.senal_KIL)
        self.shortcut_INF = QShortcut(QKeySequence(
            Qt.Key.Key_I, Qt.Key.Key_N, Qt.Key.Key_F), self)
        self.shortcut_INF.activated.connect(lambda: self.timer_contador.stop())
        self.shortcut_INF.activated.connect(self.shortcut_INF_activo)

    def shortcut_INF_activo(self):
        self.INF_activo = True
        self.senal_INF.emit()
        self.timer_contador.stop()
        self.label_vida_luigi.hide()
        self.label_INF = QLabel(self)
        self.label_INF.setGeometry(QtCore.QRect(100, 70, 50, 13))
        self.label_INF.setText(f'{self.label_vida_luigi.text()}')
        self.label_INF.show()

    def label_vida(self):
        self.label_vida_txt = QLabel(self)
        self.label_vida_txt.setText('Vidas:')
        self.label_vida_txt.setGeometry(QtCore.QRect(20, 70, 50, 13))
        self.label_vida_luigi = QLabel(self)
        self.label_vida_luigi.setGeometry(QtCore.QRect(100, 70, 50, 13))
        self.label_vida_luigi.setText(f'{P.CANTIDAD_VIDAS}')
        self.label_vida_luigi.show()

    def actualizar_vida_luigi(self, vidas_luigi):
        self.label_vida_luigi.setText(f'{vidas_luigi}')

    def label_tiempo(self):
        self.label_texto_time = QLabel(self)
        self.label_texto_time.setText('Tiempo:')
        self.label_texto_time.setGeometry(QtCore.QRect(20, 50, 50, 13))
        self.label_texto_time.show()
        self.label_contador = QLabel(self)
        self.label_contador.setGeometry(QtCore.QRect(100, 50, 50, 13))
        self.actualizar_contador()
        self.label_contador.show()
        self.timer_contador = QTimer(self)
        self.timer_contador.timeout.connect(self.actualizar_contador)

    def actualizar_contador(self):
        if not self.INF_activo:
            self.tiempo_restante -= 1
            if self.tiempo_restante < 0:
                self.tiempo_restante = 0

        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        texto = f"{minutos:02}:{segundos:02}"
        self.label_contador.setText(texto)

        if self.tiempo_restante == 0:
            self.senal_timeout.emit()

    def keyPressEvent(self, event):
        """
        Se modifica el keyPressEvent para que no se pueda spamear pero se sienta fluido el juego
        """
        if self.bloquear_teclado:
            return
        if event.key() == Qt.Key.Key_A:
            self.procesar_tecla({'direccion': 'izquierda'})
        elif event.key() == Qt.Key.Key_D:
            self.procesar_tecla({'direccion': 'derecha'})
        elif event.key() == Qt.Key.Key_W:
            self.procesar_tecla({'direccion': 'arriba'})
        elif event.key() == Qt.Key.Key_S:
            self.procesar_tecla({'direccion': 'abajo'})
        elif event.key() == Qt.Key.Key_G:
            self.senal_check_win.emit()

    def procesar_tecla(self, datos_tecla):
        self.senal_teclas.emit(datos_tecla)
        self.bloquear_teclado = True
        QTimer.singleShot(self.tiempo_bloqueo, self.desbloquear_teclado)

    def desbloquear_teclado(self):
        self.bloquear_teclado = False

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
                    muro.move(30 * j + 210, 460)

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

    def mostrar_ventana(self):
        self.timer_contador.start(1000)
        self.show()

    def esconder_ventana(self):
        self.hide()

    def reiniciar_labels(self):
        for label in self.lista_labels_roca:
            label.hide()
        self.label_luigi.hide()
        for label in self.labels_fantasmas_hor.values():
            label.hide()
        for label in self.labels_fantasmas_ver.values():
            label.hide()

    def animar_luigi(self, direccion: str):
        nuevaX = self.label_luigi.x() + dict_direcciones[direccion][1] * 30
        nuevaY = self.label_luigi.y() + dict_direcciones[direccion][0] * 30

        self.anim_luigi = QPropertyAnimation(self.label_luigi, b'pos')
        self.anim_luigi.setEndValue(QPoint(nuevaX, nuevaY))
        self.anim_luigi.setDuration(130)
        self.anim_luigi.start()
        ruta_sprites = M.dict_luigi[direccion]
        self.cambiar_pixmap(self.label_luigi, ruta_sprites,
                            0, len(ruta_sprites) - 1)

    def cambiar_pixmap(self, label_cambio, ruta_sprites, indice, ultimo_indice):
        if indice > ultimo_indice:
            return

        pixmap = QtGui.QPixmap(ruta_sprites[indice])
        label_cambio.setPixmap(pixmap)
        label_cambio.raise_()

        QTimer.singleShot(70, lambda: self.cambiar_pixmap
                          (label_cambio, ruta_sprites, indice + 1, ultimo_indice))

    def crear_luigi(self, x, y):
        '''
        Funcion que se encarga de crear la label unica de Luigi que se modifica
        '''
        self.label_luigi = QLabel(self)
        self.label_luigi.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                               (*P.RUTA_PERSONAJES, 'luigi_front.png'))))
        self.label_luigi.setGeometry(QtCore.QRect(
            240 + 30 * x, 40 + 30 * y, 30, 30))
        self.label_luigi.raise_()
        self.label_luigi.show()

    def crear_paredes(self, lista_paredes: list):
        for coordenada in lista_paredes:
            x, y = coordenada[0], coordenada[1]
            self.label_pared = QLabel(self)
            self.label_pared.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                                   (*P.RUTA_ELEMENTOS, 'wall.png'))))
            self.label_pared.setGeometry(QtCore.QRect(
                240 + 30 * x, 40 + 30 * y, 30, 30))
            self.label_pared.show()

    def crear_rocas(self, lista_rocas: list):
        for roca in self.lista_labels_roca:
            roca.hide()
        for coordenada in lista_rocas:
            x, y = coordenada[0], coordenada[1]
            self.label_roca = QLabel(self)
            self.label_roca.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                                  (*P.RUTA_ELEMENTOS, 'rock.png'))))
            self.label_roca.setGeometry(QtCore.QRect(
                240 + 30 * x, 40 + 30 * y, 30, 30))
            self.label_roca.show()
            self.lista_labels_roca.append(self.label_roca)

    def crear_label_estrella(self, tupla_estrella: tuple):
        x, y = tupla_estrella[0], tupla_estrella[1]
        self.label_estrella = QLabel(self)
        self.label_estrella.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                                  (*P.RUTA_ELEMENTOS, 'osstar.png'))))
        self.label_estrella.setScaledContents(True)
        self.label_estrella.setGeometry(QtCore.QRect(
            240 + 30 * x, 40 + 30 * y, 30, 30))
        self.label_estrella.show()

    def crear_label_fuego(self, lista_fuego: list):
        print('Creando lista fuego')
        print(lista_fuego)
        for coordenada in lista_fuego:
            x, y = coordenada[0], coordenada[1]
            self.label_fuego = QLabel(self)
            self.label_fuego.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                                   (*P.RUTA_ELEMENTOS, 'fire.png'))))
            self.label_fuego.setGeometry(QtCore.QRect(
                240 + 30 * x, 40 + 30 * y, 30, 30))
            self.label_fuego.setScaledContents(True)
            self.label_fuego.show()

    def crear_labels_fantasmas(self, id_fantasma: int, tipo: str, x, y):
        print(f'Creando fantasma de tipo {tipo}')
        if tipo == "V":
            label = QLabel(self)
            label.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                        (*P.RUTA_PERSONAJES, 'red_ghost_vertical_1.png'))))
            label.setScaledContents(True)
            label.setGeometry(240 + 30 * x, 40 + 30 * y, 30, 30)
            self.labels_fantasmas_ver[id_fantasma] = label
            label.raise_()
            label.show()

        if tipo == "H":
            label = QLabel(self)
            label.setPixmap(QtGui.QPixmap(QtGui.QPixmap(os.path.join
                                                        (*P.RUTA_PERSONAJES, 'white_ghost_right_1.png'))))
            label.setScaledContents(True)
            label.setGeometry(240 + 30 * x, 40 + 30 * y, 30, 30)
            self.labels_fantasmas_hor[id_fantasma] = label
            label.raise_()
            label.show()

    def animar_fantasma(self, tipo: str, id_fantasma: int, direccion):
        if tipo in 'V':
            pond = 1 if direccion == "abajo" else -1
            label_fantasmaV = self.labels_fantasmas_ver[id_fantasma]
            self.anim = QPropertyAnimation(label_fantasmaV, b'pos')
            self.anim.setEndValue(
                QPoint(label_fantasmaV.x(), label_fantasmaV.y() + 30 * pond))
            self.anim.setDuration(150)
            self.anim.start()
            ruta_sprites = M.sprites_fantasmaV
            self.cambiar_pixmap(label_fantasmaV, ruta_sprites,
                                0, len(ruta_sprites) - 1)

        elif tipo in "H":  # Lo
            pond = -1 if direccion == "izquierda" else 1
            label_fantasmaH = self.labels_fantasmas_hor[id_fantasma]
            ruta_sprites = M.dict_fantasma_hor[direccion]
            self.anim = QPropertyAnimation(label_fantasmaH, b'pos')
            self.anim.setEndValue(
                QPoint(label_fantasmaH.x() + pond * 30, label_fantasmaH.y()))
            self.anim.setDuration(150)
            self.anim.start()
            self.cambiar_pixmap(label_fantasmaH, ruta_sprites,
                                0, len(ruta_sprites) - 1)

    def remover_fantasma(self, tipo, id_fantasma):

        if tipo == 'V':
            label = self.labels_fantasmas_ver[id_fantasma]
            label.hide()
        elif tipo == 'H':
            label = self.labels_fantasmas_hor[id_fantasma]
            label.hide()

    def finalizar_partida(self, dato: str, vidas_luigi, nombre_usuario):
        self.hide()
        self.ventana_puntaje = QWidget()
        self.ventana_puntaje.resize(300, 200)
        self.mensaje = QLabel(self.ventana_puntaje)
        self.mensaje.setGeometry(110, 20, 50, 90)
        self.mensaje.show()
        self.puntaje_txt = QLabel(self.ventana_puntaje)
        self.puntaje_txt.setGeometry(110, 50, 50, 90)
        self.puntaje_txt.show()
        self.boton_salir = QPushButton(self.ventana_puntaje)
        self.boton_salir.setGeometry(QtCore.QRect(227, 11, 61, 169))
        self.boton_salir.setText("EXIT")
        self.boton_salir.clicked.connect(self.salir)
        self.label_puntaje = QLabel(self.ventana_puntaje)
        self.label_puntaje.setGeometry(169, 50, 50, 90)
        self.label_puntaje.show()
        self.mensaje.setText(nombre_usuario)
        if not self.INF_activo:  # Victoria sin cheats
            if dato == 'WIN':
                self.ventana_puntaje.setWindowTitle('VICTORY')
                if vidas_luigi == P.CANTIDAD_VIDAS:
                    self.puntaje = self.tiempo_restante * P.MULTIPLICADOR_PUNTAJE
                else:
                    self.puntaje = ((self.tiempo_restante * P.MULTIPLICADOR_PUNTAJE)
                                    / P.CANTIDAD_VIDAS - vidas_luigi)
            else:
                self.ventana_puntaje.setWindowTitle('YOU LOSE')
                self.puntaje = 0

        elif self.INF_activo:
            self.ventana_puntaje.setWindowTitle('CHEATER')
            self.puntaje = (P.TIEMPO_CUENTA_REGRESIVA *
                            P.MULTIPLICADOR_PUNTAJE)

        self.puntaje_txt.setText('PUNTAJE:')
        self.label_puntaje.setText(str(self.puntaje))
        self.ventana_puntaje.show()

    def salir(self):
        self.close()
        self.ventana_puntaje.close()
