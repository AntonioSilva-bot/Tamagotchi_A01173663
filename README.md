# Tamagotchi
Este es un codigo programado en Python y Arduino para el funcionamiento de un videojuego siendo en este caso un Tamagotchi, este es un prototipo de Tamagotchi en el cual se pueden seleccionar 3 opciones las cuales son alimentar, jugar y esperar, dependiendo de lo que se elige se suman o restan algunos punto y sise llega a 0 puntos el tamagotchi muere y acaba el juego.
Para el funcionamiento del juego es necesario contar con una placa arduino y una raspberry(En este caso utiliazmos la raspberry 3b+).

## Instalación

Instalación de pygames.
```sh
pip install pygames
```
Librería del display Oled.
```sh
sudo apt update
sudo apt upgrade
i2cdetect -y 1
Library installation
sudo apt install -y git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```
## Construcción del código

Importamos las siguientes librerías:
```python
import os
import sys
import time
import serial
import random
import pygame
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
```
Se inicializa la ejecución de la Oled para la transmisión de datos.
```python
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
#Se inicializa el display
disp.begin()
#Se limpia el display
disp.clear()
disp.display()
```
Se controla la comunicación por medio del UART.
```python
ser = serial.Serial(
port='/dev/ttyACM0',
baudrate = 115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,timeout=1)
counter=0
```
Se indica la presencia de leds declarando los pines de la Raspberry.
```python
LED1 = 17
LED2 = 27
LED3 = 22
```
Se crea la clase declarando cada una de las funciones que tendrá nuestro tamagotchi.
```python
class Tamagotchi:
    def __init__(self, nombre):
        genero = random.choice(["Masculino", "Femenino"])
        print("Tu Tamagotchi es " + genero)
        self.genero = genero
        self.nombre = nombre
        self.hambre = 10
        self.felicidad = 10
        self.salud = 0
```
Esta funcion se indica que el tamagotchi pasa a un estado de reposo hasta que se indique otra cosa, además se restarán dos puntos de los contadores de jugar y alimento.
Además se enciende el tercer led de nuestra protoboard por medio del GPIO ya que indicamos que los pines serán de salida y se indican que unicamente el tercer led se encuentra en un estado activo.
```python
    def evento(self, accion):
        self.hambre -= 1
        self.felicidad -= 1
        GPIO.setup(LED1, GPIO.OUT)
        GPIO.setup(LED2, GPIO.OUT)
        GPIO.setup(LED3, GPIO.OUT)
        GPIO.output (LED1, 0)
        GPIO.output (LED2, 0)
        GPIO.output (LED3, 1)
        image = Image.open('nada.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        disp.image(image)
        disp.display()
        print("-----------------")
        if accion == "alimentar":
            self.alimentar()
        elif accion == "jugar":
            self.jugar()
```
Se enciende el primer led de la protoboard y se suma uno en el contador del alimento
```python
    def alimentar(self):
        GPIO.setup(LED1, GPIO.OUT)
        GPIO.setup(LED2, GPIO.OUT)
        GPIO.setup(LED3, GPIO.OUT)
        GPIO.output (LED1, 1)
        GPIO.output (LED2, 0)
        GPIO.output (LED3, 0)
        print("Has alimentado a " + self.nombre)
        self.hambre += 2
        print("-----------------")
        image = Image.open('comer.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        disp.image(image)
        disp.display()
        if self.hambre > 10:
            # Sobrealimentado
            self.salud += 2
        pass

    def jugar(self):
        GPIO.setup(LED1, GPIO.OUT)
        GPIO.setup(LED2, GPIO.OUT)
        GPIO.setup(LED3, GPIO.OUT)
        GPIO.output (LED1, 0)
        GPIO.output (LED2, 1)
        GPIO.output (LED3, 0)
        print("Juegas con " + self.nombre)
        image = Image.open('star.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        disp.image(image)
        disp.display()
        exec(open("1.py").read())
        self.felicidad += 3
        print("-----------------")
        image = Image.open('jugar2.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
        disp.image(image)
        disp.display()
        # Evitar sobrepasar
        if self.felicidad > 10:
            self.felicidad = 10

    def muere(self):
        if self.salud >= 10 or self.felicidad <= 0 or self.hambre <= 0:
            image = Image.open('muerto.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
            disp.image(image)
            disp.display()
            GPIO.setup(LED1, GPIO.OUT)
            GPIO.setup(LED2, GPIO.OUT)
            GPIO.setup(LED3, GPIO.OUT)
            GPIO.output (LED1, 1)
            GPIO.output (LED2, 1)
            GPIO.output (LED3, 1)
            return True
        else:
            return False

    def imprimir_estado(self):
        print("Hambre: " + str(self.hambre))
        print("Felicidad: " + str(self.felicidad))
        print("Salud: " + str(self.salud))
```
