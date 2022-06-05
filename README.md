# Tamagotchi
Este es un codigo programado en Python y Arduino para el funcionamiento de un videojuego siendo en este caso un Tamagotchi, este es un prototipo de Tamagotchi en el cual se pueden seleccionar 3 opciones las cuales son alimentar, jugar y esperar, dependiendo de lo que se elige se suman o restan algunos punto y sise llega a 0 puntos el tamagotchi muere y acaba el juego.
Para el funcionamiento del juego es necesario contar con una placa arduino y una raspberry(En este caso utiliazmos la raspberry 3b+)

## Instalación

Instalación de pygames
```sh
pip install pygames
```
Librería del display Oled
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
Se inicializa la ejecución de la Oled para la transmisión de datos
```sh
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
Se controla la comunicación por medio del UART
```sh
ser = serial.Serial(
port='/dev/ttyACM0',
baudrate = 115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,timeout=1)
counter=0
```
Se indica la presencia de leds declarando los pines de la Raspberry
```sh
LED1 = 17
LED2 = 27
LED3 = 22
