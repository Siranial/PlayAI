import pygame
from paddle import Paddle
from ball import Ball
from keylogger import Keylogger
import time
pygame.init()
#frame shit
frame_time=.016
frame_count=0

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#window & misc
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pygame Pong")
carryOn = True
clock = pygame.time.Clock()

#paddles
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

#ball
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

#spritelist
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

#score
scoreA = 0
scoreB = 0

#keylogger
keylog = Keylogger("keys.txt")

#main
while carryOn:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carryOn = False

	#get keyboard input
	keys = pygame.key.get_pressed()
	#quit command query
	if keys[pygame.K_q]:
		carryOn = False
	#screenshot command
	if keys[pygame.K_e]:
		pygame.image.save(screen,"screenshot.jpg")
		keylog.update("keylog.txt","screenshot")
	if keys[pygame.K_r]:
		next_frame=time.time()+frame_time
		while True:
			while time.time()<next_frame:
				time.sleep(.001)
				if keys[pygame.K_w]:
					keylog.update("keylog2.txt","w")
				if keys[pygame.K_s]:
					keylog.update("keylog2.txt","s")
				if keys[pygame.K_UP]:
					keylog.update("keylog2.txt","up")
				if keys[pygame.K_DOWN]:
					keylog.update("keylog2.txt","down")
			frame_count+=1
			keylog.update("keylog.txt2",frame_count)
			next_frame+=frame_time


	#paddle movement
	if keys[pygame.K_w]:
		paddleA.moveUp(5)
		keylog.update("keylog.txt","w")
	if keys[pygame.K_s]:
		paddleA.moveDown(5)
		keylog.update("keylog.txt","s")
	if keys[pygame.K_UP]:
		paddleB.moveUp(5)
		keylog.update("keylog.txt","up")
	if keys[pygame.K_DOWN]:
		paddleB.moveDown(5)
		keylog.update("keylog.txt","down")

	all_sprites_list.update()

	#ball check
	if ball.rect.x >= 690:
		scoreA += 1
		ball.velocity[0] = -ball.velocity[0]
	if ball.rect.x <= 0:
		scoreB += 1
		ball.velocity[0] = -ball.velocity[0]
	if ball.rect.y > 490:
		ball.velocity[1] = -ball.velocity[1]
	if ball.rect.y < 0:
		ball.velocity[1] = -ball.velocity[1]

	if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
		ball.bounce()

	#drawing
	screen.fill(BLACK)
	pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
	all_sprites_list.draw(screen)

	#score display
	font = pygame.font.Font(None, 74)
	text = font.render(str(scoreA), 1, WHITE)
	screen.blit(text, (250, 10))
	text = font.render(str(scoreB), 1, WHITE)
	screen.blit(text, (420, 10))

	#screen update
	pygame.display.flip()
	clock.tick(60)

#quit
pygame.quit()
