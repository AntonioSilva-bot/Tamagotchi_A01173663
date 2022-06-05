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
### Codigo principal
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
Esta funcion se indica que el tamagotchi pasa a un estado de reposo hasta que se indique otra cosa, imprime una imagen en el display Oled y se restarán dos puntos de los contadores de jugar y alimento.
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
Se enciende el primer led de la protoboard, se manda el mensaje "Has alimentado a x" por la terminal, se imprime una imagen en el display Oled y se suma uno en el contador del alimento
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
        
```
La funcion jugar se encarga de enciende el segundo led de la protoboard, manda el mensaje "Juegas con x " a la terminal, suma uno al contador de juego y eejecuta el codigo "1.py" llevandonos al juego que se ha diseñado. Posteriormente cambia la imagen del diplay para esperar a la siguiente instrucción que se ejecute
```python
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
```
Esta función se ejecuta una vez que los puntos de alguno de los dos contadores llegue a cero y se encarga de finalizar el programa
```python
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
```
Imprime el valor de los contadores
```python
    def imprimir_estado(self):
        print("Hambre: " + str(self.hambre))
        print("Felicidad: " + str(self.felicidad))
        print("Salud: " + str(self.salud))
```
Dentro del main se encuentra el menu en donde se escogerá la acción del usuario así como se encuentra la función de nombrar a nuestro tamagotchi y habilitarnos el envio de imagenes a la oled
```python
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
```
### 1.py (Juego)

SSe importa la librería pygames y se inicializa
```python
import pygame
pygame.init()
```
Se crea el display en donde se ejecutará el juego y se importan los elementos de sonido para el juego
```python
ventana = pygame.display.set_mode((640,480))
pygame.display.set_caption("Juego 1")
PEW_sound = pygame.mixer.Sound('PEW.wav')
loose_sound = pygame.mixer.Sound('loose.wav')
```
Se realiza la creación de los elementos que se utilizarán para la ejecución del juego  
```python
# Crea el objeto pelota
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
speed = [4,4]
ballrect.move_ip(0,0)

# Crea el objeto bate, y obtengo su rectángulo
base = pygame.image.load("base.png")
baserect = base.get_rect()
baserect.move_ip(240,450)

# Esta es la fuente que usaremos para el texto que aparecerá en pantalla (tamaño 36)
fuente = pygame.font.Font(None, 36)
```
Se inicializa el juego realizando un chequeo de la pulsación ed teclas y detecta si exite alguna colición entere los elementos
```python
# Bucle principal del juego
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

# Compruebo si se ha pulsado alguna tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        baserect = baserect.move(-6,0)
    if keys[pygame.K_RIGHT]:
        baserect = baserect.move(6,0)

# Compruebo si hay colisión
    if baserect.colliderect(ballrect):
        PEW_sound.play() #connect
        speed[1] = -speed[1]
```
Se realizan las acciones de los elementos que se imprimen en pantalla, siendo que si en algun momento la pelota llega a tocar el borde el juego se toma por terminado y nos retorna al programa principal
```python
# Muevo la pelota
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]

    if ballrect.top < 0:
        speed[1] = -speed[1]
    # Si la pelota toca el border inferior, has perdido ("Game Over")
    if ballrect.bottom > ventana.get_height():
        loose_sound.play() #miss
        texto = fuente.render("Game Over", True, (125,125,125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
        pygame.time.delay(800)
        jugando = False

    else:
        ventana.fill((234, 212, 252))
 # Dibujo la pelota
        ventana.blit(ball, ballrect)
# Dibujo el bate
        ventana.blit(base, baserect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
```
### Codigo de arduino

```arduino
#define PIN_BOT1 3
#define PIN_BOT2 4
#define PIN_BOT3 5
int val1 = 0;
int val2 = 0;
int val3 = 0; 

void setup() {
  Serial.begin(115200);
  delay(30);
  pinMode(PIN_BOT1, INPUT);
  pinMode(PIN_BOT2, INPUT);
  pinMode(PIN_BOT3, INPUT);
}
 
void loop(){
  val1 = digitalRead(PIN_BOT1);  //lectura digital de pin
  val2 = digitalRead(PIN_BOT2);  //lectura digital de pin
  val3 = digitalRead(PIN_BOT3);  //lectura digital de pin
  if (val1 == HIGH) {
      Serial.println("uno");
  }
  if (val2 == HIGH) {
      Serial.println("dos");
  }
  if (val3 == HIGH) {
      Serial.println("tres");
  }  
  delay(250);
}
```

## Ejecutar el código
```sh
Python Tamagotchi.py
```

## Conclusiones

