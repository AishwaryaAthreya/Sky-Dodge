import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_KP_ENTER,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2, 6)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    #move and remove cloud
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            #self.display("GAMEOVER")
            self.kill()

#soundeffect
pygame.mixer.init()
pygame.init()

#speed setup - clock
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#load music
#Music credits : Chris Bailey
pygame.mixer.music.load("sounds/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.3)

#load sound files
# sound source: Chris Bailey
move_up_sound = pygame.mixer.Sound("sounds/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sounds/Boom.ogg")

#adjust volume
move_up_sound.set_volume(0.2)
move_down_sound.set_volume(0.2)
collision_sound.set_volume(1.0)

running = True

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                running = False
        
        elif event.type == QUIT:
            running = False
        
        elif event.type == K_KP_ENTER:
            running = True

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        
            


    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))
    screen_center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    #check collision
    if pygame.sprite.spritecollideany(player, enemies):
        
       # gameover = "GAME OVER"
       # pygame.display.gameover
        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(3000)
        
        

      
        running = False

    pygame.display.flip()
    clock.tick(70)

pygame.mixer.music.stop()
pygame.mixer.quit()