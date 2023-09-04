from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
import os
import parametros as P
from backend.logica_ventana_inicio import VentanaInicioBackend


class VentanaInicio(QWidget):

    senal_verificar_usuario = pyqtSignal(str)
    senal_tipo_juego = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("VentanaInicio")
        self.resize(600, 500)
        self.setMinimumSize(QtCore.QSize(600, 500))
        self.setMaximumSize(QtCore.QSize(600, 500))
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            *P.RUTA_PERSONAJES, 'white_ghost_left_1.png')))

        self.fondo = QtWidgets.QLabel(self)
        self.fondo.setGeometry(QtCore.QRect(-20, -270, 621, 681))
        self.fondo.setText("")
        self.fondo.setPixmap(QtGui.QPixmap(QtGui.QPixmap(
            os.path.join(*P.RUTA_FONDOS, 'fondo_inicio.png'))))
        self.fondo.setScaledContents(True)
        self.fondo.setObjectName("fondo")

        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(QtCore.QRect(20, 20, 351, 111))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(QtGui.QPixmap(
            os.path.join(*P.RUTA_ELEMENTOS, 'logo.png'))))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.black = QtWidgets.QLabel(self)
        self.black.setGeometry(QtCore.QRect(-30, 400, 631, 111))
        self.black.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.black.setText("")
        self.black.setObjectName("black")

        self.txt_usuario = QtWidgets.QLabel(self)
        self.txt_usuario.setGeometry(QtCore.QRect(10, 410, 61, 21))
        self.txt_usuario.setStyleSheet("color: rgb(255, 255, 255);")
        self.txt_usuario.setText("  Usuario: ")

        self.nombre_usuario = QtWidgets.QLineEdit(self)
        self.nombre_usuario.setGeometry(QtCore.QRect(70, 410, 371, 20))
        self.nombre_usuario.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                          "color: rgb(253, 253, 253)")
        self.nombre_usuario.setInputMask("")
        self.nombre_usuario.setText("")
        self.nombre_usuario.setObjectName("nombre_usuario")

        self.boton_login = QtWidgets.QPushButton(self)
        self.boton_login.setGeometry(QtCore.QRect(464, 412, 111, 61))
        self.boton_login.setText("Login")
        self.boton_login.clicked.connect(self.verificar_usuario)

        self.boton_salir = QtWidgets.QPushButton(self)
        self.boton_salir.setGeometry(QtCore.QRect(520, 10, 75, 25))
        self.boton_salir.setText("SALIR")
        self.boton_salir.clicked.connect(self.salir)

        self.Partidas = QtWidgets.QComboBox(self)
        self.Partidas.setGeometry(QtCore.QRect(10, 450, 431, 22))
        self.Partidas.setObjectName("Partidas")
        self.mostrarListaPartidas()
        self.show()

    def verificar_usuario(self):
        print(self.nombre_usuario.text())
        self.senal_verificar_usuario.emit(self.nombre_usuario.text())

    def salir(self):
        self.close()

    def seleccionar_tipo_juego(self):
        """
        Maneja la seleccion del nuevo juego o selecciona un mapa
        """
        seleccion = self.Partidas.currentText()
        self.senal_tipo_juego.emit(seleccion)
        self.hide()

    def mostrar_error_usuario(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle('Error 300')
        self.msg.setText('El nombre de usuario no es valido')
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.show()

    def mostrarListaPartidas(self):
        self.Partidas.addItem('Modo Constructor')
        for Partida in os.listdir(os.path.join(*P.RUTA_PARTIDAS)):
            self.Partidas.addItem(Partida[:-4])
