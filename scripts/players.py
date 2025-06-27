import pygame

class Player1:
    def __init__(self, sprite_data, spritesheet):
        self.posicionX = 100
        self.posicionY = 250
        self.velocidad = 6
        self.radio = 20
        self.rect = pygame.Rect(self.posicionX - 17, self.posicionY - 17, 35, 35)

        self.sprite_data = sprite_data["jugador1"]
        self.spritesheet = spritesheet
        self.direction = "abajo"
        self.frame_index = 0
        self.frame_delay = 10
        self.frame_counter = 0
    
    def crear(self, screen):
        self.draw(screen)
    
    def mover(self, keys, screen, joystick=None):
        eje_x, eje_y = 0, 0

        if joystick:
            eje_x = joystick.get_axis(0)
            eje_y = joystick.get_axis(1)

        movio = False

        if keys[pygame.K_w] or eje_y < -0.5:
            self.posicionY -= self.velocidad
            self.direction = "arriba"
            movio = True
        elif keys[pygame.K_s] or eje_y > 0.5:
            self.posicionY += self.velocidad
            self.direction = "abajo"
            movio = True
        elif keys[pygame.K_a] or eje_x < -0.5:
            self.posicionX -= self.velocidad
            self.direction = "izquierda"
            movio = True
        elif keys[pygame.K_d] or eje_x > 0.5:
            self.posicionX += self.velocidad
            self.direction = "derecha"
            movio = True

        self.rect.left = self.posicionX - 17
        self.rect.top = self.posicionY - 17

        if movio:
            self.animar()
        else:
            self.frame_index = 1

        self.draw(screen)
        self.limit()

    def draw(self, screen):
        frame = self.sprite_data[self.direction][self.frame_index]
        sprite = self.spritesheet.get_sprite(frame["x"], frame["y"], frame["w"], frame["h"])
        screen.blit(sprite, (self.rect.left, self.rect.top))

    def animar(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.sprite_data[self.direction])
            self.frame_counter = 0
    
    def limit(self):
        self.posicionX = max(0, min(self.posicionX, 800))
        self.posicionY = max(0, min(self.posicionY, 500))

class Player2(Player1):
    def __init__(self, sprite_data, spritesheet):
        super().__init__(sprite_data, spritesheet)
        self.posicionX = 60
        self.posicionY = 250
        self.radio = 20
        self.velocidad = 3
        self.boost_speed = 5
        self.rect = pygame.Rect(self.posicionX - 17, self.posicionY - 17, 35, 35)
        self.sprite_data = sprite_data["jugador2"]


    def crear(self, screen):
        self.draw(screen)

    def mover(self, keys, boost_activo, screen, joystick=None):

        if joystick:
            eje_x = joystick.get_axis(0)
            eje_y = joystick.get_axis(1)
        else:
            eje_x = 0
            eje_y = 0

        velocidad_actual = self.boost_speed if boost_activo else self.velocidad
        movio = False

        if keys[pygame.K_UP] or eje_y < -0.5:
            self.posicionY -= velocidad_actual
            self.direction = "arriba"
            movio = True
        elif keys[pygame.K_DOWN] or eje_y > 0.5:
            self.posicionY += velocidad_actual
            self.direction = "abajo"
            movio = True
        elif keys[pygame.K_LEFT] or eje_x < -0.5:
            self.posicionX -= velocidad_actual
            self.direction = "izquierda"
            movio = True
        elif keys[pygame.K_RIGHT] or eje_x > 0.5:
            self.posicionX += velocidad_actual
            self.direction = "derecha"
            movio = True

        if movio:
            self.animar()
        else:
            self.frame_index = 1

        self.rect.left = self.posicionX - 17
        self.rect.top = self.posicionY - 17
        self.draw(screen)
        self.limit()

    def boost(self, objeto):
        return self.rect.colliderect(objeto)