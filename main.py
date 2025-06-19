import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400  # Move this up

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Move this up
pygame.display.set_caption("Click Dash")

# Load images
background_images = [    
    pygame.image.load("Night.png"), 
    pygame.image.load("Night.png"),
    pygame.image.load("Night.png ") 
]

background_idx = 0 
next_background_idx = 1
background_alpha = 0
background_x1 = 0
background_x2 = WIDTH
background_speed = 1

def draw_scrolling_background():
    global background_x1, background_x2, background_idx, next_background_idx, background_alpha

    background_x1 -= background_speed
    background_x2 -= background_speed

    if background_x1 <= -WIDTH:
        background_x1 = background_x2 + WIDTH
        background_idx = next_background_idx
        next_background_idx = (next_background_idx + 1) % len(background_images)
        background_alpha = 0

    if background_x2 <= -WIDTH:
        background_x2 = background_x1 + WIDTH
        background_idx = next_background_idx
        next_background_idx = (next_background_idx + 1) % len(background_images)
        background_alpha = 0

    if background_alpha < 255:
        background_alpha += 1

    bg1 = background_images[background_idx].copy()
    bg2 = background_images[next_background_idx].copy()
    bg2.set_alpha(background_alpha)

    screen.blit(bg1, (background_x1, 0))
    screen.blit(bg1, (background_x2, 0))
    screen.blit(bg2, (background_x1, 0))
    screen.blit(bg2, (background_x2, 0))

player_img = pygame.image.load("Cube.png")

obstacle_images = [
    pygame.image.load("SpikeOne.png"),
    pygame.image.load("SpikeTwo.png"),
    pygame.image.load("SpikeThree.png")
]

GREY = (255, 255, 255)  # Note: This is actually white, not grey
FPS = 60
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.size = 40
        self.x = 100
        self.y = HEIGHT - self.size - 10
        self.image = pygame.transform.scale(player_img, (self.size, self.size))
        self.jump = False
        self.velocity = 0
        self.gravity = 1
        self.jump_count = 0

    def update(self):
        if self.jump:
            self.velocity = -15
            self.jump = False

        self.y += self.velocity
        self.velocity += self.gravity

        if self.y > HEIGHT - self.size - 10:
            self.y = HEIGHT - self.size - 10
            self.velocity = 0
            self.jump_count = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = random.randint(40, 100)
        self.x = WIDTH
        self.y = HEIGHT - self.height - 10
        self.image = pygame.transform.scale(random.choice(obstacle_images), (self.width, self.height))
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x + self.width < 0

player = Player()
obstacles = []
spawn_timer = random.randint(30, 110)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 3:    
                player.jump = True
                player.jump_count += 1

    draw_scrolling_background()  # Use the background function

    player.update()

    if spawn_timer == 0:
        obstacles.append(Obstacle())
        spawn_timer = random.randint(30, 110)
    else:
        spawn_timer -= 1

    for obstacle in obstacles[:]:
        obstacle.update()
        if obstacle.off_screen():
            obstacles.remove(obstacle)

    for obstacle in obstacles:
        if pygame.Rect(player.x, player.y, player.size, player.size).colliderect(
           pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
            print("FIRE IN THE HOLE !!!!!!!!!")
            running = False

    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()