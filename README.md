# Sistema Clasificador de Monedas con ESP32

Este proyecto implementa un sistema automático de clasificación de monedas utilizando una ESP32 y sensores de peso HX711 junto con sensores infrarrojos para detectar y clasificar monedas de diferentes denominaciones (1000, 200 y 50).

Video funcionamiento: https://youtu.be/mhKJIaTK_bk?feature=shared

## Componentes Necesarios

- Placa ESP32
- 3 módulos HX711 (convertidor analógico-digital para celdas de carga)
- 3 celdas de carga
- 3 sensores infrarrojos
- Cables de conexión
- Software Thonny IDE

## Configuración del Hardware

### Conexiones de los Sensores HX711

Se utilizan tres módulos HX711 conectados a la ESP32:

1. **HX711 #1 (Monedas de 1000)**:
   - DOUT: GPIO17
   - SCK: GPIO18

2. **HX711 #2 (Monedas de 200)**:
   - DOUT: GPIO19
   - SCK: GPIO21

3. **HX711 #3 (Monedas de 50)**:
   - DOUT: GPIO22
   - SCK: GPIO23

### Conexiones de los Sensores Infrarrojos

1. **Sensor IR para monedas de 1000**: GPIO16
2. **Sensor IR para monedas de 200**: GPIO4
3. **Sensor IR para monedas de 50**: GPIO15

## Instalación del Firmware y Configuración del Software

### Paso 1: Configuración de Thonny IDE

1. Se instala Thonny IDE en la computadora.
2. Se conecta la ESP32 al ordenador mediante un cable USB.
3. En Thonny, se selecciona la opción "MicroPython (ESP32)" en el menú "Herramientas > Opciones > Intérprete".
4. Se asegura que el puerto COM correcto esté seleccionado.

### Paso 2: Instalación de MicroPython en la ESP32

1. En Thonny, se selecciona "Herramientas > Opciones > Intérprete > Instalar o actualizar firmware".
2. Se selecciona la versión más reciente de MicroPython para ESP32.
3. Se presiona el botón BOOT en la ESP32 mientras se inicia el proceso de flasheo.
4. Se espera a que finalice el proceso de instalación del firmware.

### Paso 3: Creación de la Estructura de Archivos

1. Se crea una carpeta llamada "lib" en el dispositivo ESP32:
   ```python
   # En la terminal REPL de Thonny:
   import os
   os.mkdir('lib')
   ```

2. Se crea el archivo "hx711.py" dentro de la carpeta "lib" con la implementación de la biblioteca para controlar los módulos HX711.

3. Se crea el archivo principal "ClasificadorMonedas.py" en la raíz del dispositivo.

## Implementación del Software

### Biblioteca HX711 (lib/hx711.py)

Esta biblioteca implementa la comunicación con los módulos HX711. Proporciona métodos para:

- Inicializar el sensor con la ganancia deseada
- Leer valores del sensor
- Realizar la tara (calibración a cero)
- Establecer la escala para convertir unidades brutas a unidades de peso
- Aplicar filtros para mejorar la precisión de las lecturas

La clase HX711 maneja la comunicación a bajo nivel con el convertidor analógico-digital, controlando los pines SCK y DOUT para obtener los valores de peso de las celdas de carga.

### Programa Principal (ClasificadorMonedas.py)

El programa principal inicializa tres instancias de HX711, cada una conectada a una celda de carga diferente para detectar monedas de 1000, 200 y 50. También configura tres sensores infrarrojos para detectar el paso de las monedas.

El funcionamiento es el siguiente:

1. Se inicializan los sensores HX711 y se realiza la tara inicial.
2. Se establecen las escalas apropiadas para cada sensor según la calibración.
3. Se configuran los pines para los sensores infrarrojos.
4. En un bucle infinito:
   - Se monitorea cada sensor infrarrojo para detectar cuando una moneda activa el sensor.
   - Cuando se detecta una moneda, se lee el peso correspondiente.
   - Se calcula el peso promedio por moneda y se determina su denominación según rangos predefinidos.
   - Se incrementa el contador correspondiente si la moneda se clasifica correctamente.
   - Se muestra la información en la consola.
5. Al interrumpir el programa, se muestra un resumen de las monedas contadas.

## Lógica de Clasificación

- **Monedas de 1000**: Peso entre 9g y 11g
- **Monedas de 200**: Peso entre 4.5g y 9g
- **Monedas de 50**: Peso entre 3g y 4.3g o entre 3g y 16g (según el sensor)

## Uso del Sistema

1. Asegurarse de que las celdas de carga estén sin peso al iniciar el sistema para una correcta tara.
2. Ejecutar el programa "ClasificadorMonedas.py" en la ESP32 mediante Thonny.
3. El sistema mostrará "Sistema listo. Inserta monedas."
4. Insertar monedas una por una, pasándolas por los sensores correspondientes.
5. El sistema detectará el paso de la moneda, medirá su peso y la clasificará según su denominación.
6. Para finalizar el programa, presionar Ctrl+C, lo que mostrará un resumen de las monedas contadas.

## Explicación del Código

### Inicialización de los sensores HX711

```python
hx_1 = HX711(dout=17, pd_sck=18)
hx_2 = HX711(dout=19, pd_sck=21)
hx_3 = HX711(dout=22, pd_sck=23)
```

Se crean tres instancias del sensor HX711, especificando los pines DOUT y SCK para cada uno.

### Calibración de los sensores

```python
hx_1.tare()
hx_2.tare()
hx_3.tare()
```

Se realiza la tara de los sensores para establecer el punto cero sin peso.

```python
hx_1.set_scale(200)  # Ajustar según calibración (200 unidades = 10 g)
hx_2.set_scale(200)
hx_3.set_scale(280)
```

Se establece la escala para convertir las unidades brutas del sensor a gramos.

### Detección y clasificación de monedas

El sistema utiliza sensores infrarrojos para detectar cuando una moneda pasa:

```python
if sensor_1000.value() == 0:
    print("Sensor de moneda 1000 activado.")
    # Resto del código para procesar monedas de 1000
```

Cuando se detecta una moneda, se lee su peso y se clasifica según rangos predefinidos:

```python
if 9 <= peso_1 <= 11:
    contador_1 += 1
    print("Moneda de 1000 registrada. Total: {}".format(contador_1))
```

### Manejo de errores y resumen

El programa incluye manejo de excepciones para las lecturas de peso y un bloque try-except para mostrar un resumen al finalizar:

```python
except KeyboardInterrupt:
    print("\nConteo")
    print("Total monedas de 1000 detectadas:", contador_1)
    print("Total monedas de 200 detectadas:", contador_2)
    print("Total monedas de 50 detectadas:", contador_3)
```

## Notas Adicionales

- Es importante calibrar correctamente los sensores HX711 para cada tipo de moneda.
- Los rangos de peso pueden necesitar ajustes según las monedas específicas que se utilicen.
- El sistema es sensible a variaciones en el peso, por lo que se recomienda un ambiente estable para su operación.
