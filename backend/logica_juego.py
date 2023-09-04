import os
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from random import uniform
import parametros as P


dict_direcciones = {'derecha': (0, 1), 'izquierda': (0, -1),
                    'abajo': (1, 0), 'arriba': (-1, 0)}


class FantasmasThread(QThread):
    def __init__(self, padre) -> None:
        super().__init__(parent=padre)
        self.juego = padre
        self.tiempo = int(1 / uniform(P.MIN_VELOCIDAD, P.MAX_VELOCIDAD))

    def run(self):
        self.pausa = False
        self.msleep(self.tiempo * 1000)
        while not self.pausa:
            for fantasma_ver in self.juego.fantasmas_ver:
                fantasma_ver.mover()
            self.msleep(180)
            for fantasma_hor in self.juego.fantasmas_hor:
                fantasma_hor.mover()
            self.msleep(self.tiempo * 1000)


class Juego(QObject):

    senal_inicio_juego = pyqtSignal(dict)
    senal_enviar_tablero = pyqtSignal(dict)
    senal_game_over = pyqtSignal(str, int, str)
    senal_anim_luigi = pyqtSignal(str)
    senal_enviar_coords_luigi = pyqtSignal(int, int)
    senal_paredes = pyqtSignal(list)
    senal_rocas = pyqtSignal(list)
    senal_mover_roca = pyqtSignal()
    senal_estrella = pyqtSignal(tuple)
    senal_fuego = pyqtSignal(list)
    senal_victoria = pyqtSignal()
    senal_vidas_luigi = pyqtSignal(int)
    senal_muere_fantasma = pyqtSignal(str, int)
    senal_mover_fantasmas_ver = pyqtSignal(str, int, str)
    senal_fantasmas_verticales = pyqtSignal(int, str, int, int)
    senal_mover_fantasmas_hor = pyqtSignal(str, int, str)
    senal_fantasmas_horizontales = pyqtSignal(int, str, int, int)
    senal_mostrar_ventana = pyqtSignal()
    senal_reiniciar_labels = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.nombre_usuario = ''
        self.inicio = True
        self.musica_victoria = MusicaVictoria()
        self.musica_derrota = MusicaDerrota()
        self.tiempo = int(1 / uniform(P.MIN_VELOCIDAD, P.MAX_VELOCIDAD))
        self.fantasmas_ver = []
        self.fantasmas_hor = []
        self.INF_activo = False
        self.thread_fantasmas = FantasmasThread(self)
        self.thread_fantasmas.start()

    def reiniciar(self):
        self.senal_reiniciar_labels.emit()
        print(f'Reinicie {self.parametros_iniciales}')
        self.cargar_partida(self.parametros_iniciales)
        self.actualizar_tablero()

    def cargar_partida(self, dicc):
        self.parametros_iniciales = dict(dicc)
        print(f'Acabo de crear partida {self.parametros_iniciales}')
        self.diccionario_grilla = {}
        self.luigi = Luigi(dicc['Luigi'][0], dicc['Luigi'][1])
        self.estrella = dicc['Estrella']
        self.fantasmas_ver = []
        self.fantasmas_hor = []
        for x in dicc['FantasmaV']:
            self.fantasmas_ver.append(
                FantasmaVertical(self, x[0], x[1],
                                 senal_mover_fantasma=self.senal_mover_fantasmas_ver,  # type: ignore
                                 senal_muere_fantasma=self.senal_muere_fantasma))  # type: ignore
        for y in dicc['FantasmaH']:
            self.fantasmas_hor.append(
                FantasmaHorizontal(self, y[0], y[1],
                                   senal_mover_fantasma=self.senal_mover_fantasmas_hor,  # type: ignore
                                   senal_muere_fantasma=self.senal_muere_fantasma))  # type: ignore
        self.paredes = dicc["Pared"]
        self.rocas = dicc['Roca']
        self.fuegos = dicc['Fuego']
        self.crear_tablero_vacio()
        self.inicio = True
        self.senal_mostrar_ventana.emit()
        self.comenzar_partida()

    def comenzar_partida(self):
        if self.inicio:
            self.senal_enviar_coords_luigi.emit(
                self.luigi.posX, self.luigi.posY)
            self.senal_paredes.emit(self.paredes)
            self.senal_rocas.emit(self.rocas)
            self.senal_estrella.emit(self.estrella)
            self.senal_fuego.emit(self.fuegos)
            for fantasma in self.fantasmas_ver:
                self.senal_fantasmas_verticales.emit(
                    fantasma.id, 'V', fantasma.posX, fantasma.posY
                )
            for fantasma in self.fantasmas_hor:
                self.senal_fantasmas_horizontales.emit(
                    fantasma.id, 'H', fantasma.posX, fantasma.posY
                )

    def cambiar_nombre_usuario(self, nombre):
        self.nombre_usuario = nombre

    def activoINF(self):
        self.INF_activo = True

    def game_over(self, dato):
        if dato == "WIN":
            self.musica_victoria.comenzar()
        else:
            self.musica_derrota.comenzar()
        self.senal_game_over.emit(dato, self.luigi.vidas, self.nombre_usuario)

    def actualizar_tablero(self):
        self.vaciar_grilla()
        self.diccionario_grilla[(self.luigi.posX, self.luigi.posY)] = "L"
        for coord in self.paredes:
            self.diccionario_grilla[(coord[0], coord[1])] = 'P'
        for coord in self.rocas:
            self.diccionario_grilla[(coord[0], coord[1])] = 'R'
        self.senal_rocas.emit(self.rocas)
        self.diccionario_grilla[(self.estrella[0], self.estrella[1])] = 'S'
        for fantasma in self.fantasmas_ver:
            self.diccionario_grilla[(fantasma.posX, fantasma.posY)] = "V"
            if self.luigi.posX == fantasma.posX and self.luigi.posY == fantasma.posY:
                if fantasma.vivo:
                    if not self.INF_activo:
                        self.luigi.vidas -= 1
                        if self.luigi.vidas >= 1:
                            self.thread_fantasmas.exit()
                            self.senal_vidas_luigi.emit(self.luigi.vidas)
                        if self.luigi.vidas == 0:
                            print('Luigi tiene 0 vidas')
                            self.game_over('else')
                    self.reiniciar()

        for fantasma in self.fantasmas_hor:
            self.diccionario_grilla[(fantasma.posX, fantasma.posY)] = "H"
            if self.luigi.posX == fantasma.posX and self.luigi.posY == fantasma.posY:
                if fantasma.vivo:
                    if not self.INF_activo:
                        self.luigi.vidas -= 1
                        if self.luigi.vidas >= 1:
                            self.thread_fantasmas.exit()
                            self.senal_vidas_luigi.emit(self.luigi.vidas)
                        if self.luigi.vidas == 0:
                            print('Luigi tiene 0 vidas')
                            self.game_over('else')
                    self.reiniciar()

        for fuego in self.fuegos:
            self.diccionario_grilla[(fuego[0], fuego[1])] = 'F'

    def mover_luigi(self, event):
        """
        Encargado de mover a Luigi
        """
        direccion = event['direccion']
        posX = self.luigi.posX
        posY = self.luigi.posY
        nuevaposX = posX + dict_direcciones[direccion][1]
        nuevaposY = posY + dict_direcciones[direccion][0]

        if self.revisar_colisiones_luigi(direccion):
            self.luigi.posX = nuevaposX
            self.luigi.posY = nuevaposY
            self.senal_anim_luigi.emit(direccion)
            self.actualizar_tablero()
            for fuego in self.fuegos:
                if (fuego[0], fuego[1]) == (self.luigi.posX, self.luigi.posY):
                    if not self.INF_activo:
                        self.luigi.vidas -= 1
                        self.senal_vidas_luigi.emit(self.luigi.vidas)
                        self.thread_fantasmas.exit()
                        if self.luigi.vidas == 0:
                            self.game_over('else')
                    self.reiniciar()

    def revisar_colisiones_luigi(self, direccion) -> bool:
        """
        Revisa las colisiones de luigi en una direccion 
        """
        posX = self.luigi.posX
        posY = self.luigi.posY
        nuevaposX = posX + dict_direcciones[direccion][1]
        nuevaposY = posY + dict_direcciones[direccion][0]

        if not 0 <= nuevaposX < P.ANCHO_GRILLA - 2:
            return False
        elif not 0 <= nuevaposY < P.LARGO_GRILLA - 2:
            return False
        elif self.diccionario_grilla[(nuevaposX, nuevaposY)] == 'P':
            return False
        elif self.diccionario_grilla[((nuevaposX, nuevaposY))] == 'R':
            return self.mover_roca(direccion, nuevaposX, nuevaposY)
        return True

    def mover_roca(self, direccion, X, Y) -> bool:
        nuevaX = X + dict_direcciones[direccion][1]
        nuevaY = Y + dict_direcciones[direccion][0]
        if 0 <= nuevaX < P.ANCHO_GRILLA - 2:
            if 0 <= nuevaY < P.LARGO_GRILLA - 2:
                if self.diccionario_grilla[(nuevaX, nuevaY)] == '-':
                    for roca in self.rocas:
                        if roca == (X, Y):
                            self.rocas.remove(roca)

                            self.rocas.append((nuevaX, nuevaY))
                            self.senal_rocas.emit(self.rocas)
                            return True
        return False

    def checkear_win(self):
        star_posX = self.estrella[0]
        star_posY = self.estrella[1]
        luigi_posX = self.luigi.posX
        luigi_posY = self.luigi.posY
        if star_posX == luigi_posX and star_posY == luigi_posY:
            self.game_over("WIN")

    def crear_tablero_vacio(self):
        for fila in range(P.ANCHO_GRILLA - 2):
            for columna in range(P.LARGO_GRILLA - 2):
                self.diccionario_grilla[(fila, columna)] = '-'

    def vaciar_grilla(self):
        for key in self.diccionario_grilla.keys():
            self.diccionario_grilla[key] = '-'

    def eliminar_fanstasmas(self):
        for fantasma in self.fantasmas_hor + self.fantasmas_ver:
            fantasma.morir()
            fantasma.vivo = False


class MusicaVictoria(QObject):
    def __init__(self) -> None:
        super().__init__()

    def comenzar(self):
        self.cancion = QtMultimedia.QSound(
            os.path.join(*P.RUTA_MUSICA, 'stageClear.wav'))
        self.cancion.play()


class MusicaDerrota(QObject):
    def __init__(self) -> None:
        super().__init__()

    def comenzar(self):
        self.cancion = QtMultimedia.QSound(
            os.path.join(*P.RUTA_MUSICA, 'gameOver.wav'))
        self.cancion.play()


class Luigi(QObject):

    def __init__(self, posX, posY) -> None:
        self.posX = posX
        self.posY = posY
        self.vivo = True
        self.vidas = P.CANTIDAD_VIDAS


class FantasmaVertical(QObject):
    identificador = 1

    def __init__(self, parent, x, y, senal_muere_fantasma: pyqtSignal,
                 senal_mover_fantasma: pyqtSignal) -> None:
        super().__init__()
        self.posX = x
        self.posY = y
        self.id = FantasmaVertical.identificador
        FantasmaVertical.identificador += 1
        self.tipo = 'V'
        self.senal_muere_fantasma = senal_muere_fantasma
        self.senal_mover_fantasma = senal_mover_fantasma
        self.vivo = True
        self.subiendo = True
        self.juego = parent

    def mover(self):
        if self.vivo:
            if self.subiendo:
                if 0 <= self.posY - 1 < P.LARGO_GRILLA - 2:
                    if self.juego.diccionario_grilla[(self.posX, self.posY - 1)] not in ['P', 'R']:
                        self.posY = self.posY - 1
                        self.senal_mover_fantasma.emit(
                            self.tipo, self.id, 'arriba')  # type: ignore
                        self.juego.diccionario_grilla[(
                            self.posX, self.posY)] = 'V'
                        self.juego.actualizar_tablero()

                    else:
                        self.subiendo = False

                    if self.juego.diccionario_grilla[(self.posX, self.posY)] == 'F':
                        self.morir()
                else:
                    self.subiendo = False
            else:
                if 0 <= self.posY + 1 < P.LARGO_GRILLA - 2:
                    if self.juego.diccionario_grilla[(self.posX, self.posY + 1)] not in 'PR':
                        self.posY = self.posY + 1
                        self.senal_mover_fantasma.emit(
                            self.tipo, self.id, 'abajo')  # type: ignore
                        self.juego.actualizar_tablero()

                    else:
                        self.subiendo = True
                    if self.juego.diccionario_grilla[(self.posX, self.posY)] == 'F':
                        self.morir()
                else:
                    self.subiendo = True

    def morir(self):
        self.senal_muere_fantasma.emit(self.tipo, self.id)  # type: ignore
        self.vivo = False


class FantasmaHorizontal(QObject):
    identificador = 100

    def __init__(self, parent, x, y, senal_muere_fantasma: pyqtSignal,
                 senal_mover_fantasma: pyqtSignal) -> None:
        super().__init__()
        self.posX = x
        self.posY = y
        self.id = FantasmaHorizontal.identificador
        FantasmaVertical.identificador += 1
        self.tipo = 'H'
        self.senal_muere_fantasma = senal_muere_fantasma
        self.senal_mover_fantasma = senal_mover_fantasma
        self.vivo = True
        self.derecha = True
        self.juego = parent

    def mover(self):
        if self.vivo:
            if self.derecha:  # se mueve a la DER
                if 0 <= self.posX + 1 < P.ANCHO_GRILLA - 2:
                    if self.juego.diccionario_grilla[(self.posX + 1, self.posY)] not in ['P', 'R']:
                        self.posX = self.posX + 1
                        self.senal_mover_fantasma.emit(
                            self.tipo, self.id, 'derecha')  # type: ignore
                        self.juego.diccionario_grilla[(
                            self.posX, self.posY)] = 'V'
                        self.juego.actualizar_tablero()

                    else:
                        self.derecha = False
                    if self.juego.diccionario_grilla[(self.posX, self.posY)] == 'F':
                        self.morir()
                else:
                    self.derecha = False
            else:
                if 0 <= self.posX - 1 < P.ANCHO_GRILLA - 2:
                    if self.juego.diccionario_grilla[(self.posX - 1, self.posY)] not in 'PR':
                        self.posX = self.posX - 1
                        self.senal_mover_fantasma.emit(
                            self.tipo, self.id, 'izquierda')  # type: ignore
                        self.juego.actualizar_tablero()

                    else:
                        self.derecha = True
                    if self.juego.diccionario_grilla[(self.posX, self.posY)] == 'F':
                        self.morir()
                else:
                    self.derecha = True

    def morir(self):
        self.senal_muere_fantasma.emit(self.tipo, self.id)  # type: ignore
        self.vivo = False
