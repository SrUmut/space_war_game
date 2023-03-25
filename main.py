import sys
import time

from screen import Screen

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, y_pos):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(center=(screen.width/2, y_pos))
        self.velocity = screen.width / 3
        self.health = 10
        
    def player_input(self, pressed_keys):
        # if player is the host
        if self.rect.center[1] == HOST_Y_POS:
            if pressed_keys[pygame.K_a]:
                self.rect.x -= self.velocity * dt
            elif pressed_keys[pygame.K_d]:
                self.rect.x += self.velocity * dt
        # if player is the opponent
        else:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.x -= self.velocity * dt
            elif pressed_keys[pygame.K_RIGHT]:
                self.rect.x += self.velocity * dt

    def in_border(self):
        # putting player inside the borders if it is out
        if self.rect.right > screen.width:
            self.rect.right = screen.width
        if self.rect.left < 0:
            self.rect.left = 0

    # checking if player got hit
    def hit(self):
        if self.rect.centery == HOST_Y_POS:
            if pygame.sprite.spritecollide(self, opponent_bullet, True):
                self.health -= 1
        else:
            if pygame.sprite.spritecollide(self, host_bullet, True):
                self.health -= 1

    def display_health(self):
        rate = self.health/10
        if self.rect.centery == HOST_Y_POS:
            health_bar_rect = pygame.rect.Rect(self.rect.left-10, self.rect.bottom+10, int(rate*(self.rect.width+20)), 20)
            health_bar_border_rect = pygame.rect.Rect(self.rect.left-10, self.rect.bottom+10, self.rect.width+20, 20)
        else:
            health_bar_rect = pygame.rect.Rect(self.rect.left-10, self.rect.top-30, int(rate*(self.rect.width+20)), 20)
            health_bar_border_rect = pygame.rect.Rect(self.rect.left-10, self.rect.top-30, self.rect.width+20, 20)
        pygame.draw.rect(screen.surf, "red", health_bar_rect, border_radius=5)
        pygame.draw.rect(screen.surf, "white", health_bar_border_rect, width=2, border_radius=5)

    def check_health(self):
        global game_active
        if self.health <= 0:
            if self.rect.centery == HOST_Y_POS:
                game_over("opponent")
            else:
                game_over("host")

    def update(self, pressed_keys):
        self.player_input(pressed_keys)
        self.in_border()
        self.hit()
        self.display_health()
        self.check_health()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner, pos):
        super().__init__()
        v = screen.height
        if owner == "host":
            self.image = host_bullet_surf
            self.velocity = -v
            self.rect = self.image.get_rect(midbottom=pos)
        else:
            self.image = opponent_bullet_surf
            self.velocity = v
            self.rect = self.image.get_rect(midtop=pos)

    def update(self):
        self.rect.y += self.velocity * dt
        if self.rect.bottom < 0 or self.rect.top > screen.height:
            self.kill()


def bullet_collision():
    for h_bullet in host_bullet.sprites():
        if pygame.sprite.spritecollide(h_bullet, opponent_bullet, True):
            h_bullet.kill()


def game_over(winner):
    global game_active, game_over_time, game_over_surf
    game_active = False
    for bullet in host_bullet.sprites() + opponent_bullet.sprites():
        bullet.kill()

    game_over_text = game_over_font.render("Game Over!", True, "white")
    game_over_text = pygame.transform.rotozoom(game_over_text, 0, 0.7)
    game_over_text_rect = game_over_text.get_rect(center=(screen.width/2, 200))

    if winner == "host":
        winner_text = game_over_font.render("Blue won", True, "blue")
    else:
        winner_text = game_over_font.render("Red won", True, "red")
    winner_text_rect = winner_text.get_rect(center=(screen.width/2, screen.height/2))

    restart_text = game_over_font.render("Press SPACE to restart", True, "white")
    restart_text = pygame.transform.rotozoom(restart_text, 0, 0.6)
    restart_text_rect = restart_text.get_rect(center=(screen.width/2, 520))

    game_over_surf = pygame.image.load("background.png").convert()
    game_over_surf.blit(game_over_text, game_over_text_rect)
    game_over_surf.blit(winner_text, winner_text_rect)
    game_over_surf.blit(restart_text, restart_text_rect)

    game_over_time = time.time()


def restart():
    global game_active
    game_active = True
    host.sprite.kill()
    opponent.sprite.kill()
    host.add(Player(surface=player_surf_1, y_pos=HOST_Y_POS))
    opponent.add(Player(surface=player_surf_2, y_pos=OPPONENT_Y_POS))

FPS = 60
HOST_Y_POS = 620
OPPONENT_Y_POS = 100
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

pygame.init()
screen = Screen()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 80)
game_active = True
game_over_time = -1  # time the game is over

# player surfaces
player_surf_1 = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_surf_1.fill("blue")
player_surf_2 = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_surf_2.fill("red")

player_surf_1 = pygame.image.load("blue_ship.png").convert_alpha()
player_surf_1 = pygame.transform.rotozoom(player_surf_1, 0, 0.3)
player_surf_2 = pygame.image.load("red_ship.png").convert_alpha()
player_surf_2 = pygame.transform.rotozoom(player_surf_2, 180, 0.3)
# bullet surfaces
host_bullet_surf = pygame.surface.Surface((10,30))
host_bullet_surf.fill("blue")
opponent_bullet_surf = pygame.surface.Surface((10,30))
opponent_bullet_surf.fill("red")

# background surface
bg = pygame.image.load("background.png").convert()

# game over surface
game_over_surf = pygame.image.load("background.png").convert()

# player groups
host = pygame.sprite.GroupSingle()
host.add(Player(surface=player_surf_1, y_pos=HOST_Y_POS))

opponent = pygame.sprite.GroupSingle()
opponent.add(Player(surface=player_surf_2, y_pos=OPPONENT_Y_POS))

# bullet groups
host_bullet = pygame.sprite.Group()
opponent_bullet = pygame.sprite.Group()


prev_time = time.time() - 1/60
while True:
    # delta time
    dt = time.time() - prev_time
    prev_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    host_bullet.add(Bullet("host", host.sprite.rect.midtop))
                if event.key == pygame.K_m:
                    opponent_bullet.add(Bullet("opponent", opponent.sprite.rect.midbottom))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # checking if game is over at least for 3 seconds
                    if time.time() - game_over_time > 3:
                        restart()

    if game_active:
        screen.surf.blit(bg, (0, 0))

        keys = pygame.key.get_pressed()

        # updating then drawing bullets
        host.update(keys)
        opponent.update(keys)
        host.draw(screen.surf)
        opponent.draw(screen.surf)

        # updating then drawing bullets
        host_bullet.update()
        opponent_bullet.update()
        host_bullet.draw(screen.surf)
        opponent_bullet.draw(screen.surf)

        # checking bullet collisions
        bullet_collision()
    else:
        screen.surf.blit(game_over_surf, (0,0))


    pygame.display.update()
    clock.tick(FPS)