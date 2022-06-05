#Librerias
import os
import sys
import time
import serial
import random
import pygame
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
#Importa el module PIL
from PIL import Image

#Se encarga de la ejecución de la oled
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
#Se inicializa pygame
pygame.init()
#Se inicializa el display
disp.begin()

# Clear display.
disp.clear()
disp.display()

#Controla la comunicación con el UART
ser = serial.Serial(
port='/dev/ttyACM0',
baudrate = 115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,timeout=1)
counter=0

#Se declaran los pines de la Raspberry para los leds
LED1 = 17
LED2 = 27
LED3 = 22

#Se crea la clase tyamagotchi en donde se declaran las funciones
class Tamagotchi:
    def __init__(self, nombre):
        genero = random.choice(["Masculino", "Femenino"])
        print("Tu Tamagotchi es " + genero)
        self.genero = genero
        self.nombre = nombre
        self.hambre = 10
        self.felicidad = 10
        self.salud = 0

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

def main():
     image = Image.open('huevo.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
     disp.image(image)
     disp.display()
     nombre = input("Ingresa el nombre de tu Tamagotchi: ")
     tamagotchi = Tamagotchi(nombre)
     print("""
     1. Alimentar
     2. Jugar
     3. Nada""")
     image = Image.open('Inicio.bmp').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
     disp.image(image)
     disp.display()
     GPIO.setmode(GPIO.BCM)
     GPIO.setwarnings(False)

     while not tamagotchi.muere():
         x=ser.readline()
         if (x==b'uno\r\n' or x== b'dos\r\n' or x== b'tres\r\n'):
             GPIO.setup(LED1, GPIO.OUT)
             GPIO.setup(LED2, GPIO.OUT)
             GPIO.setup(LED3, GPIO.OUT)
             GPIO.output (LED1, 0)
             GPIO.output (LED2, 0)
             GPIO.output (LED3, 0)
             tamagotchi.imprimir_estado()
             if (x== b'uno\r\n'):
                 tamagotchi.evento("alimentar")
             elif (x== b'dos\r\n'):
                 tamagotchi.evento("jugar")
             elif (x== b'tres\r\n'):
                 tamagotchi.evento("")
     print(tamagotchi.nombre + " ha muerto")
main()
