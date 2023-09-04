import sys
from PyQt5.QtWidgets import QApplication


# VENTANA INICIO #
from backend.logica_ventana_inicio import VentanaInicioBackend
from frontend.ventana_inicio import VentanaInicio

# VENTANA MODO CONSTRUCTOR #
from backend.logica_modo_constructor import VentanaModoConstructorBackend
from frontend.ventana_modo_constructor import VentanaModoConstructor

# VENTANA GAME #
from backend.logica_juego import Juego
from frontend.ventana_juego import VentanaJuego


def hook(type, value, traceback):
    print(type)
    print(traceback)


if __name__ == "__main__":

    app = QApplication([])

# VENTANA DE INICIO
    ventana_inicio = VentanaInicio()
    logica_inicio = VentanaInicioBackend()

# VENTANA CONSTRUCTOR
    ventana_constructor = VentanaModoConstructor()
    logica_constructor = VentanaModoConstructorBackend()

# VENTANA JUEGO
    logica_juego = Juego()
    ventana_juego = VentanaJuego()

# CONECTAMOS TODAs LAS SENALES D:

    ventana_inicio.senal_verificar_usuario.connect(
        logica_inicio.verificar_usuario)
    logica_inicio.senal_mensaje_error.connect(
        ventana_inicio.mostrar_error_usuario)
    logica_inicio.senal_empezar_juego.connect(
        ventana_inicio.seleccionar_tipo_juego)
    ventana_inicio.senal_tipo_juego.connect(logica_inicio.selector_tipo_juego)

# SI ELEGIMOS UN MAPA

    logica_inicio.senal_mostrar_juego.connect(ventana_juego.mostrar_ventana)
    logica_inicio.senal_cargar_juego.connect(logica_juego.cargar_partida)

# MODO CONSTRUCTOR

    logica_inicio.senal_modo_constructor.connect(
        ventana_constructor.mostrar_ventana)
    logica_constructor.senal_parametros_Constructor.connect(
        logica_juego.cargar_partida)
    ventana_constructor.senal_boton_jugar.connect(
        logica_constructor.generar_partida)

# Hippity hoppity it's a mystery how it works so properly!"

    logica_juego.senal_mostrar_ventana.connect(ventana_juego.mostrar_ventana)
    ventana_juego.senal_teclas.connect(logica_juego.mover_luigi)
    logica_juego.senal_anim_luigi.connect(ventana_juego.animar_luigi)
    logica_juego.senal_enviar_coords_luigi.connect(ventana_juego.crear_luigi)
    logica_juego.senal_paredes.connect(ventana_juego.crear_paredes)
    logica_juego.senal_rocas.connect(ventana_juego.crear_rocas)
    logica_juego.senal_estrella.connect(ventana_juego.crear_label_estrella)
    logica_juego.senal_fuego.connect(ventana_juego.crear_label_fuego)
    ventana_juego.senal_check_win.connect(logica_juego.checkear_win)
    logica_juego.senal_fantasmas_verticales.connect(
        ventana_juego.crear_labels_fantasmas)
    logica_juego.senal_mover_fantasmas_ver.connect(
        ventana_juego.animar_fantasma)
    logica_juego.senal_fantasmas_horizontales.connect(
        ventana_juego.crear_labels_fantasmas)
    logica_juego.senal_mover_fantasmas_hor.connect(
        ventana_juego.animar_fantasma)
    logica_juego.senal_muere_fantasma.connect(ventana_juego.remover_fantasma)
    ventana_juego.senal_KIL.connect(logica_juego.eliminar_fanstasmas)
    logica_juego.senal_vidas_luigi.connect(ventana_juego.actualizar_vida_luigi)
    logica_juego.senal_game_over.connect(ventana_juego.finalizar_partida)
    logica_juego.senal_reiniciar_labels.connect(ventana_juego.reiniciar_labels)
    ventana_juego.senal_INF.connect(logica_juego.activoINF)
    logica_inicio.senal_nombre_usuario.connect(
        logica_juego.cambiar_nombre_usuario)

    sys.exit(app.exec())
