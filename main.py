import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create a tuple to make windows width and height for screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
# Sets the coordinates for the player picture
playerX = 370
playerY = 480
# Sets the changed coordinates
playerX_change = 0
playerY_change = 0

# Sets lists for the enemies to create multiple
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    # Sets the coordinates for the enemy picture
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    # Sets the changed coordinates
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
# Sets the coordinates for the bullet picture
bulletX = 0
bulletY = 480
# Sets the changed coordinates
bulletX_change = 0
bulletY_change = 2
# Ready state means you can't see bullet, fire means it is moving
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    # Renders the score by getting the text, bool, and color
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    # Prints game over in middle of the screen
    screen.blit(over_text, (200, 250))

def player(x, y):
    # Blit means to draw, draws player picture on coordinates
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    # Draws enemy image on coordinates
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    # Make it global to use anywhere
    global bullet_state
    # Set the state as firing
    bullet_state = "fire"
    # Puts the bullet image in the top middle of the player image
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Uses the distance formula to see if the bullet hits the enemy image
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # Found by trial and error
    if distance < 27:
        return True
    else:
        return False

# The game is running
running = True
while running:
    # While in the loop, create a tuple of RGB to change background color
    screen.fill((0, 0, 0))
    # Adds background image
    screen.blit(background, (0, 0))
    # Checks all events in pygame
    for event in pygame.event.get():
        # Checks if the game has been quit
        if event.type == pygame.QUIT:
            # If it was quit, close the game
            running = False

        # Checks if a key was pressed
        if event.type == pygame.KEYDOWN:
            # Checks if key was a
            if event.key == pygame.K_a:
                # If key was a x -0.25
                playerX_change = -0.25
                # Checks if key was d
            if event.key == pygame.K_d:
                # If key was d x + 0.25
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Creates the bullet shooting sound
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        # Checks if key was released
        if event.type == pygame.KEYUP:
            # Checks if a or d key was released
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                # If a or d or s or w was released, position does not change
                playerX_change = 0
                playerY_change = 0

    # Updates players position based on key inputs
    playerX += playerX_change
    # Makes sure the player cannot go outside the screen
    if playerX <= 0:
        playerX = 0
    # Screen width 800 - player image 64bits
    elif playerX >= 736:
        playerX = 736
    # Updates players position based on key inputs
    playerY += playerY_change
    # Makes sure the player cannot go outside the screen
    if playerY <= 0:
        playerY = 0
    # Screen height 600 - player image 64 bits
    elif playerY >= 536:
        playerY = 536

    # Updates each enemies position
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # Updates enemy position based on key inputs
        enemyX[i] += enemyX_change[i]
        # Makes sure the enemy cannot go outside the screen
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        # Screen width 800 - enemy image 64bits
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            # If collision set bullet back to player and set state to ready
            bulletY = playerY
            bulletX = playerX
            bullet_state = "ready"
            score_value += 1
            # If enemy is hit reset it at a random location
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Puts the enemy on the screen after screen is filled
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Puts the player on the screen after screen is filled
    player(playerX, playerY)
    # Render the score
    show_score(textX, textY)
    # Updates your display to fill color
    pygame.display.update()
