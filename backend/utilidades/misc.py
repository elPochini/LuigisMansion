import os
import parametros as P


sprites_luigi_derecha = [os.path.join(*P.RUTA_PERSONAJES, 'luigi_right_1.png'),
                         os.path.join(*P.RUTA_PERSONAJES, 'luigi_right_2.png'),
                         os.path.join(*P.RUTA_PERSONAJES, 'luigi_right_3.png')]

sprites_luigi_izquierda = [os.path.join(*P.RUTA_PERSONAJES, 'luigi_left_1.png'),
                           os.path.join(*P.RUTA_PERSONAJES,
                                        'luigi_left_2.png'),
                           os.path.join(*P.RUTA_PERSONAJES, 'luigi_left_3.png')]

sprites_luigi_abajo = [os.path.join(*P.RUTA_PERSONAJES, 'luigi_down_1.png'),
                       os.path.join(*P.RUTA_PERSONAJES, 'luigi_down_2.png'),
                       os.path.join(*P.RUTA_PERSONAJES, 'luigi_down_3.png')]

sprites_luigi_arriba = [os.path.join(*P.RUTA_PERSONAJES, 'luigi_up_1.png'),
                        os.path.join(*P.RUTA_PERSONAJES, 'luigi_up_2.png'),
                        os.path.join(*P.RUTA_PERSONAJES, 'luigi_up_3.png')]


sprites_fantasmaV = [os.path.join(*P.RUTA_PERSONAJES, 'red_ghost_vertical_1.png'),
                     os.path.join(*P.RUTA_PERSONAJES,
                                  'red_ghost_vertical_2.png'),
                     os.path.join(*P.RUTA_PERSONAJES, 'red_ghost_vertical_3.png')]

sprites_fantasmaH_der = [os.path.join(*P.RUTA_PERSONAJES, 'white_ghost_right_1.png'),
                         os.path.join(*P.RUTA_PERSONAJES,
                                      'white_ghost_right_2.png'),
                         os.path.join(*P.RUTA_PERSONAJES, 'white_ghost_right_3.png'),]

sprites_fantasmaH_izq = [os.path.join(*P.RUTA_PERSONAJES, 'white_ghost_left_1.png'),
                         os.path.join(*P.RUTA_PERSONAJES,
                                      'white_ghost_left_2.png'),
                         os.path.join(*P.RUTA_PERSONAJES, 'white_ghost_left_3.png'),]

dict_luigi = {'derecha': sprites_luigi_derecha, 'izquierda': sprites_luigi_izquierda,
              'arriba': sprites_luigi_arriba, 'abajo': sprites_luigi_abajo
              }

dict_fantasma_hor = {'derecha': sprites_fantasmaH_der,
                     'izquierda': sprites_fantasmaH_izq}
