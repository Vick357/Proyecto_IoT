from hx711 import HX711
from machine import Pin
import utime

# Configuración del sensor de peso HX711 
hx_1 = HX711(dout=17, pd_sck=18)
hx_2 = HX711(dout=19, pd_sck=21)
hx_3 = HX711(dout=22, pd_sck=23)

print("Realizando tara, asegúrate de que la celda esté sin carga...")
hx_1.tare()
hx_2.tare()
hx_3.tare()

print("Tara completada.")
hx_1.set_scale(200)  # Ajustar según calibración (200 unidades = 10 g)
hx_2.set_scale(200)
hx_3.set_scale(280)

# Configuración del sensor infrarrojo para moneda de 1000 
sensor_1000 = Pin(16, Pin.IN)  # GPIO16
sensor_200 = Pin(4, Pin.IN)  # GPIO16
sensor_50 = Pin(15, Pin.IN)  # GPIO16

# Contador de monedas de 1000 
contador_1 = 0
moneda_1 = 0
peso_1 = 0

# Contador de monedas de 200 
contador_2 = 0
moneda_2 = 0
peso_2 = 0

# Contador de monedas de 50 
contador_3 = 0
moneda_3 = 0
peso_3 = 0

# Función para leer peso en moneda 1000
def leer_peso_1000():
    try:
        peso = hx_1.get_units(times=3)
        return peso
    except Exception as e:
        print("Error al leer el sensor de peso:", e)
        return 0
    
# Función para leer peso en moneda 200
def leer_peso_200():
    try:
        peso = hx_2.get_units(times=3)
        return peso
    except Exception as e:
        print("Error al leer el sensor de peso:", e)
        return 0

# Función para leer peso en moneda 50
def leer_peso_50():
    try:
        peso = hx_3.get_units(times=3)
        return peso
    except Exception as e:
        print("Error al leer el sensor de peso:", e)
        return 0

# Bucle principal
print("\nSistema listo. Inserta monedas.\n")

try:
    while True:
        
        if sensor_1000.value() == 0:
            print("Sensor de moneda 1000 activado.")
            moneda_1 += 1
            utime.sleep(1)
            peso = leer_peso_1000()
            peso_1 = peso/moneda_1
            print("Peso promedio por moneda:", peso_1, "g")
            
            if 9 <= peso_1 <= 11:
                contador_1 += 1
                print("Moneda de 1000 registrada. Total: {}".format(contador_1))
            else:
                moneda_1 -= 1
                print("Moneda rechazada.")
        
        if sensor_200.value() == 0:
            print("Sensor de moneda 200 activado.")
            moneda_2 += 1
            utime.sleep(1)
            peso = leer_peso_200()
            peso_2 = peso/moneda_2
            print("Peso promedio por moneda:", peso_2, "g")
            
            if 4.5 <= peso_2 <= 9:
                contador_2 += 1
                print("Moneda de 200 registrada. Total: {}".format(contador_2))
                
            if 3 <= peso_2 <= 4.3:
                contador_3 += 1
                print("Moneda de 50 registrada. Total: {}".format(contador_3))
                
            else:
                moneda_2 -= 1
                print("Moneda rechazada.")
                
        if sensor_50.value() == 0:
            print("Sensor de moneda 50 activado.")
            moneda_3 += 1
            utime.sleep(1)
            peso = leer_peso_50()
            peso_3 = peso/moneda_3
            print("Peso promedio por moneda:", peso_3, "g")
            
            if 3 <= peso_3 <= 16:
                contador_3 += 1
                print("Moneda de 50 registrada. Total: {}".format(contador_3))
            else:
                moneda_3 -= 1
                print("Moneda rechazada.")           

        utime.sleep(0.005)  # Lee el sensor cada 50 ms

except KeyboardInterrupt:
    print("\nConteo")
    print("Total monedas de 1000 detectadas:", contador_1)
    print("Total monedas de 200 detectadas:", contador_2)
    print("Total monedas de 50 detectadas:", contador_3)

