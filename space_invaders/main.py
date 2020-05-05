import pygame
import random
import math
from pygame import mixer

pygame.init()
#create the screen must be a tuple
screen = pygame.display.set_mode((800,600))

# title and icon
pygame.display.set_caption('space invaders')
icon = pygame.image.load('transport.png')
pygame.display.set_icon(icon)

#background img
background = pygame.image.load('space.png').convert()
mixer.music.load('background.wav')
mixer.music.play(-1)


#player
player_img = pygame.image.load('game.png')
playerX = 370
playerY = 480
def player(x,y):
	screen.blit(player_img, (x, y))


#enemy
mob_img = []
mobX = [] 
mobY = []
mobX_change = []
mobY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	mob_img.append(pygame.image.load('technology.png'))
	mobX.append(random.randint(0,735))
	mobY.append(random.randint(50,150))
	mobX_change.append(0.3)
	mobY_change.append(40)
def mob(x, y, i):
	screen.blit(mob_img[i],(x, y))

#bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = 'ready'

def fire_bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bullet_img, (x + 16,y + 10))

def isCollision(mobX, mobY, bulletX, bulletY):
	distance = math.sqrt((math.pow(mobX - bulletX, 2)) + (math.pow(mobY - bulletY,2)))
	if distance < 27:
		return True
	else:
		return False
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x,y):
	score = font.render('Score:' + str(score_value), True, (255,255,255))
	screen.blit(score,(x,y))
#game over text

over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
	over_text = over_font.render('GAME OVER', True, (255,255,255))
	screen.blit(over_text,(200,250))


#GAME LOOP
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
	screen.fill((0, 0, 0))
	screen.blit(background,(0,0))					
#PLAYER CONTROLLS 
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		playerX -= 1
	if key[pygame.K_RIGHT]:
		playerX += 1
	#if key[pygame.K_UP]:
		#playerY -= 0.3
	#if key[pygame.K_DOWN]:
		#playerY += 0.3		

	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX =  736
	#emeny movment
	
	for i in range(num_of_enemies):

		# game over

		if mobY[i] > 440:
			for j in range(num_of_enemies):
				mobY[j] = 2000
			game_over_text()
			break 

		mobX[i] += mobX_change[i]
		if mobX[i] <= 0:
			mobX_change[i] = 0.3
			mobY[i] += mobY_change[i]		
		elif mobX[i] >= 736:
			mobX_change[i] = -0.3
			mobY[i] += mobY_change[i]
		collision = isCollision(mobX[i], mobY[i], bulletX, bulletY)
		if collision:
			exp_sound = mixer.Sound('explosion.wav')
			exp_sound.play()
			bulletY = 480
			bullet_state = 'ready'
			score_value += 1
			mobX[i] = random.randint(0,735)
			mobY[i] = random.randint(50,150)
		mob(mobX[i], mobY[i], i)

	#bullet movment




	if bulletY <= 0:
		bulletY = 480
		bullet_state = 'ready'

	if bullet_state == 'fire':
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	#collision 

	

	player(playerX, playerY)
	show_score(textX, textY)
	
	
	pygame.display.update()		