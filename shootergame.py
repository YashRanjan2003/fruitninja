import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Clock
clock = pygame.time.Clock()

# Load images
background = pygame.image.load('wooden_background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

fruit_images = [
    pygame.image.load('apple.png'),
    pygame.image.load('banana.png'),
    pygame.image.load('cherry.png'),
    pygame.image.load('mango.png'),
    pygame.image.load('orange.png'),
    pygame.image.load('pineapple.png'),
    pygame.image.load('strawberry.png'),
    pygame.image.load('watermelon.png')
]

# Resize fruit images
for i in range(len(fruit_images)):
    fruit_images[i] = pygame.transform.scale(fruit_images[i], (50, 50))

# Game variables
score = 0
high_score = 0
lives = 3
fruits = []
slices = []

# Load high score
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())

class Fruit:
    def __init__(self):
        self.image = random.choice(fruit_images)
        self.x = random.randint(0, WIDTH - 50)
        self.y = HEIGHT
        self.speed = random.randint(10, 15)  # Increased speed range
        self.angle = 0
        self.rotate_speed = random.randint(-5, 5)
        self.max_height = random.uniform(0.2 * HEIGHT, 0.5 * HEIGHT)  # Random height between 20% and 50% of screen height
        self.gravity = 0.3
        self.velocity = -math.sqrt(2 * self.gravity * (HEIGHT - self.max_height))  # Calculate initial velocity to reach max_height

    def move(self):
        self.y += self.velocity
        self.velocity += self.gravity
        self.angle += self.rotate_speed
        self.x += math.sin(math.radians(self.angle)) * 2

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(self.x + 25, self.y + 25))
        screen.blit(rotated_image, rect)

class Slice:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.life = 10

    def draw(self):
        pygame.draw.line(screen, WHITE, self.start, self.end, 2)
        self.life -= 1

def show_score():
    score_text = font.render(f'Score: {score}  High Score: {high_score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def show_lives():
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(lives_text, (WIDTH - 100, 10))

def game_over():
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))
    
    screen.fill(BLACK)
    go_text = large_font.render('GAME OVER', True, RED)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    restart_text = font.render('Click to restart', True, WHITE)
    
    screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//4))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 50))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT*3//4))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    global score, lives, fruits, slices

    running = True
    mouse_down = False
    slice_start = None

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                slice_start = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                if slice_start:
                    slices.append(Slice(slice_start, pygame.mouse.get_pos()))
                    slice_start = None

        if mouse_down and slice_start:
            current_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, WHITE, slice_start, current_pos, 2)

        if random.randint(1, 60) == 1:
            fruits.append(Fruit())

        for fruit in fruits[:]:
            fruit.move()
            fruit.draw()
            if fruit.y > HEIGHT + 50:
                fruits.remove(fruit)
                lives -= 1
                if lives <= 0:
                    game_over()
                    score = 0
                    lives = 3
                    fruits = []
                    slices = []

        for slice in slices[:]:
            slice.draw()
            if slice.life <= 0:
                slices.remove(slice)

        for fruit in fruits[:]:
            for slice in slices:
                if math.hypot(fruit.x - slice.start[0], fruit.y - slice.start[1]) < 50 or \
                   math.hypot(fruit.x - slice.end[0], fruit.y - slice.end[1]) < 50:
                    fruits.remove(fruit)
                    score += 1
                    break

        show_score()
        show_lives()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()