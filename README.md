Luigi's Mansion Maker👻🧱🔥

##### Bienvenido seas al README de elPochini, como es costumbre, abrochate los cinturones porque vas a presenciar codigo que ni yo se como funciona. Aún así mi lema de vida es ```if it's stupid and it works is not stupid```. Espero que te guste mi jueguito lo hice con mucho cariño y café, además de darle las gracias al ost de gran turismo y el profesor Layton.

## Consideraciones generales 🌏

Mi tarea en teoria cumple con la mayoría de las cosas dentro del enunciado pero hay algunos bugs que mi cuerpo rechaza a arreglar por falta de horas de sueño. Se creo otra Ventana para separar el Juego del Modo constructor. Hay animaciones. Se puede dejar mantenido el boton para avanzar, se siente raro pero funciona. Mi hermano mayor dijo que se parecía a los movimientos de los juegos del GBA. Ni idea lo que hablaba

### BUGS 🐛🦗
- No se si contarlo como bug pero las rocas no tienen animación, esto porque creo que en ninguna parte decía. Aún así siento que implementando las demás animaciones queda demostrado que entendí lo que había que hacer.
- Las Rocas tampoco se reinician cuando te pegan un hit.
- El Juego se cae si en el menu de creación no pones a un Luigi o a una Estrella  (¿Pero quién haría eso?)
- El juego no tiene pausa pero si los demás shortcuts
- 👀 No se si es bug pero le cambié el nombre a los sprites que tenían mal escrito el right 
- Si la velocidad de movimiento de los fantasmas es muy alta se desincronizan los sprites
- A veces Luigi se come 2 hits, no entendí muy bien cuando pasaba pero creo que se arregló. 



## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:

      
1. ```assets``` en ```/frontend```


##### La carpeta assets tiene la siguiente forma
- assets
    - sounds
        - gameOver.wav
        - stageClear.wav
    - sprites
       - Elementos
            - etc
       - Fondos
            - etc
       - Personajes
            - etc

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```
2. ```PyQt5```:  (debe instalarse)
    - No creo que deba poner todos los imports que hice, pero los más generales son: QWidgets, QMultimedia, QObject, QThread, Qtimer, pyqtSignal, etc
3. ```random```: ```uniform```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```botones.py```: Tiene las clases de los botones personalizados del Modo Constructor
2. ```misc.py```: Hecha para guardar algunos diccionarios de sprites y listas de sprites
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Suponemos que las rocas son entes que viajan a la velocidad de la luz y por lo tanto no tienen animacion
2. Suponemos que todos los fantasmas tienen la misma velocidad

2. Eso, no hice muchos supuestos esta vez




-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Para los QComboBox saqué codigo de [pythonguis](https://www.pythonguis.com/docs/qcombobox/).

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
