import pygame
pygame.init()

ventana = pygame.display.set_mode((640,480))
pygame.display.set_caption("Juego 1")
PEW_sound = pygame.mixer.Sound('PEW.wav')
loose_sound = pygame.mixer.Sound('loose.wav')

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
