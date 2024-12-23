import pygame
import random
import sys
import os

pygame.init()

# Definir dimensiones y colores
ANCHO, ALTO = pygame.display.Info().current_w, pygame.display.Info().current_h
BLANCO = (255, 255, 255)
GRIS = (169, 169, 169)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Función para redimensionar imágenes según resolución
def redimensionar_imagen(ruta, ancho, alto):
    img = pygame.image.load(os.path.join(base_path, ruta))
    return pygame.transform.scale(img, (ancho, alto))

# Ruta base de recursos
base_path = os.path.dirname(os.path.abspath(__file__))

# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CHICHI SIMULATOR")

# Cargar recursos
fondo_menu = redimensionar_imagen('img/fondo.png', ANCHO, ALTO)
fondo_personaje = redimensionar_imagen('img/juego.png', ANCHO, ALTO)
logo_img = redimensionar_imagen('img/logo.png', 100, 100)
fondo_juego = redimensionar_imagen('img/juego.png', ANCHO, ALTO)
caca_imgs = [redimensionar_imagen(f'img/{i}.png', 50, 50) for i in range(1, 5)]
kevin_img = redimensionar_imagen('img/kevin.png', 150, 150)
vida_img = redimensionar_imagen('img/vida.png', 50, 50)

# Música y sonidos
pygame.mixer.music.load(os.path.join(base_path, 'audio/inicio.mp3'))
musica_juego = os.path.join(base_path, 'audio/juego.mp3')
musica_ganar = os.path.join(base_path, 'audio/chichi.mp3')
musica_perder = os.path.join(base_path, 'audio/chichi.mp3')
sonido_peo = pygame.mixer.Sound(os.path.join(base_path, 'audio/peo.mp3'))

# Fuente
fuente = pygame.font.SysFont('arial', 36)

# Función para mostrar mensaje de fin de juego
def mostrar_mensaje(texto, musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()
    pantalla.fill(NEGRO)
    mensaje = fuente.render(texto, True, BLANCO)
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Función para la pantalla inicial
def pantalla_inicial():
    pygame.mixer.music.play(-1)

    while True:
        pantalla.blit(fondo_menu, (0, 0))
        texto = fuente.render("¡Toca para Jugar!", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + 100))

        copyright_texto = pygame.font.SysFont('arial', 24).render("\u00a9 2024 CHICHI Simulator", True, GRIS)
        pantalla.blit(copyright_texto, (ANCHO // 2 - copyright_texto.get_width() // 2, ALTO - 50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                seleccionar_personaje()

        pygame.display.update()

# Función para seleccionar personaje
def seleccionar_personaje():
    personajes = [
        {"nombre": "inodoro", "imagen": redimensionar_imagen('img/inodoro.png', 150, 150)},
        {"nombre": "silla", "imagen": redimensionar_imagen('img/silla.png', 150, 150)},
        {"nombre": "saco", "imagen": redimensionar_imagen('img/saco.png', 150, 150)}
    ]
    posiciones = [(ANCHO // 4 - 75, ALTO // 2 - 75), (ANCHO // 2 - 75, ALTO // 2 - 75), (3 * ANCHO // 4 - 75, ALTO // 2 - 75)]

    while True:
        pantalla.blit(fondo_personaje, (0, 0))
        titulo = fuente.render("Selecciona tu personaje", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

        for i, personaje in enumerate(personajes):
            pantalla.blit(personaje["imagen"], posiciones[i])

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for i, (x, y) in enumerate(posiciones):
                    if x <= mouseX <= x + 150 and y <= mouseY <= y + 150:
                        juego(personajes[i]["nombre"])

        pygame.display.update()

# Función principal del juego
def juego(personaje):
    # Cargar la imagen del personaje según el parámetro
    if personaje == "inodoro":
        personaje_img = redimensionar_imagen('img/inodoro.png', 100, 100)
    elif personaje == "silla":
        personaje_img = redimensionar_imagen('img/silla.png', 100, 100)
    elif personaje == "saco":
        personaje_img = redimensionar_imagen('img/saco.png', 100, 100)

    pygame.mixer.music.load(musica_juego)
    pygame.mixer.music.play(-1)

    personaje_x = ANCHO // 2 - 50
    personaje_y = ALTO - 150

    velocidad = 10

    kevin_x = random.randint(0, ANCHO - 150)
    kevin_direccion = 5

    cacas = []

    reloj = pygame.time.Clock()
    puntaje = 0
    vidas = 3
    objetivo = random.randint(10, 20)

    corriendo = True
    while corriendo:
        pantalla.blit(fondo_juego, (0, 0))

        # Dibujar personaje
        pantalla.blit(personaje_img, (personaje_x, personaje_y))

        # Dibujar Kevin y moverlo de lado a lado
        pantalla.blit(kevin_img, (kevin_x, 0))
        kevin_x += kevin_direccion
        if kevin_x <= 0 or kevin_x >= ANCHO - 150:
            kevin_direccion *= -1

        # Generar cacas desde la posición de Kevin
        if random.randint(1, 50) == 1:
            cacas.append({
                "x": kevin_x + 50,
                "y": 50,
                "img": random.choice(caca_imgs),
            })
            sonido_peo.play()

        # Dibujar y mover cacas
        for caca in cacas[:]:
            pantalla.blit(caca["img"], (caca["x"], caca["y"]))
            caca["y"] += 7

            # Verificar colisión con el personaje
            if personaje_y < caca["y"] + 50 and personaje_y + 100 > caca["y"] and personaje_x < caca["x"] + 50 and personaje_x + 100 > caca["x"]:
                cacas.remove(caca)
                puntaje += 1
                if puntaje >= objetivo:
                    corriendo = False
                    mostrar_mensaje("¡Ganaste!", musica_ganar)

            # Verificar si la caca cae al suelo
            elif caca["y"] > ALTO:
                cacas.remove(caca)
                vidas -= 1
                if vidas <= 0:
                    corriendo = False
                    mostrar_mensaje("¡Perdiste!", musica_perder)

        # Dibujar vidas
        for i in range(vidas):
            pantalla.blit(vida_img, (20 + i * 60, 20))

        # Dibujar puntaje y objetivo
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        pantalla.blit(texto_puntaje, (20, 100))

        texto_objetivo = fuente.render(f"Objetivo: {objetivo}", True, BLANCO)
        pantalla.blit(texto_objetivo, (20, 150))

        # Eventos táctiles
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEMOTION:
                personaje_x = evento.pos[0] - 50

        # Asegurar que el personaje no salga de la pantalla
        personaje_x = max(0, min(ANCHO - 100, personaje_x))

        pygame.display.update()

    pygame.mixer.music.stop()

if __name__ == "__main__":
    pantalla_inicial()
