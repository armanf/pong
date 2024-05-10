import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 5
WIN_SCORE = 10

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([10, 100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, HEIGHT // 2)
        self.speed = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Create ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.speed_y = random.choice([-BALL_SPEED, BALL_SPEED])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

# Create sprites
all_sprites = pygame.sprite.Group()
paddle1 = Paddle(20)
paddle2 = Paddle(WIDTH - 20)
ball = Ball()
all_sprites.add(paddle1, paddle2, ball)

# Scores
score1 = 0
score2 = 0

clock = pygame.time.Clock()

# Game over screen
def show_game_over_screen(winner):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 64)
    text = font.render(f"Player {winner} wins!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    score_text = font.render("Press SPACE to play again", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1.speed = -PADDLE_SPEED
            elif event.key == pygame.K_s:
                paddle1.speed = PADDLE_SPEED
            elif event.key == pygame.K_UP:
                paddle2.speed = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle2.speed = PADDLE_SPEED
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1.speed = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2.speed = 0

    all_sprites.update()

    # Ball-paddle collision
    if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
        ball.speed_x *= -1

    # Ball-wall collision
    if ball.rect.left < 0:
        score2 += 1
        if score2 >= WIN_SCORE:
            show_game_over_screen(2)
            score1 = score2 = 0
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x = BALL_SPEED
        ball.speed_y = random.choice([-BALL_SPEED, BALL_SPEED])
    elif ball.rect.right > WIDTH:
        score1 += 1
        if score1 >= WIN_SCORE:
            show_game_over_screen(1)
            score1 = score2 = 0
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed_x = -BALL_SPEED
        ball.speed_y = random.choice([-BALL_SPEED, BALL_SPEED])

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text1 = font.render(f"Player 1: {score1}", True, WHITE)
    score_rect1 = score_text1.get_rect(topleft=(10, 10))
    screen.blit(score_text1, score_rect1)
    score_text2 = font.render(f"Player 2: {score2}", True, WHITE)
    score_rect2 = score_text2.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_text2, score_rect2)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()