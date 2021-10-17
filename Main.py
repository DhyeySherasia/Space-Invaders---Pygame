import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.jpg')

# Background music
mixer.music.load('background_music.wav')
mixer.music.play(-3)

# Player
player_image = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_change = 0

# Multiple enemies
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

secure_random = random.SystemRandom()

# Enemy
for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(1, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(secure_random.uniform(0.3, 1))
    enemyY_change.append(random.randint(40, 50))

# Bullet
# ready - Can't see the bullet
# Fire - bullet is currently moving
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

score_value = 0
# Font(type, size)
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over font
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
end_score_font = pygame.font.Font('freesansbold.ttf', 50)

game_going = True


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def end_score():
    endscore = end_score_font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(endscore, (300, 290))


def game_over_text():
    over = game_over_font.render('GAME OVER', True, (255, 255, 255))
    end_score()
    screen.blit(over, (200, 200))


def enemy(x, y):
    screen.blit(enemy_image[i], (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def fire_bullet(x, y):
    global bullet_state

    screen.blit(bullet_image, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

    if dist < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Background colour RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Analysing keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2

            if event.key == pygame.K_RIGHT:
                playerX_change = 2

            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('gun_sound.wav')
                bullet_sound.play()
                bulletX = playerX
                bullet_state = "fire"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(len(enemyX)):

        # Game over
        if enemyY[i] >= 460:
            game_going = False

            for j in range(num_of_enemies):
                if enemyX[j] <= 376:
                    enemyX[j] = -1000
                elif enemyX[j] > 376:
                    enemyX[j] = 1800

                game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = secure_random.uniform(0.3, 1)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -secure_random.uniform(0.3, 1)
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 500
            bullet_state = "ready"
            score_value += 1
            if score_value % 5 == 0 and score_value != 0:
                enemy_image.append(pygame.image.load('enemy.png'))
                enemyX.append(random.randint(1, 735))
                enemyY.append(random.randint(200, 400))
                enemyX_change.append(secure_random.uniform(0.3, 1))
                enemyY_change.append(random.randint(40, 50))

            enemyX[i] = random.randint(1, 735)
            enemyY[i] = random.randint(40, 200)

        enemy(enemyX[i], enemyY[i])

    if bulletY <= -32:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Should be after screen.fill bcoz spaceship is over the screen
    player(playerX, playerY)

    if game_going:
        show_score(textX, textY)

    # Display will update throughout the game
    pygame.display.update()
