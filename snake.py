import sys
import pygame
from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)
import random

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
direction = 1

speed = 25


def destroy():
	global gameOn
	death_screen()
	gameOn = False


class Button:
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def update(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		screen.blit(self.image, self.rect)
		return action


class SnakeHead(pygame.sprite.Sprite):
	def __init__(self):
		super(SnakeHead, self).__init__()
		self.surf = pygame.Surface((25, 25))
		self.surf.fill((168, 230, 29))
		self.rect = self.surf.get_rect()

	def update(self, pressed_keys):
		global direction
		global speed
		global length
		global gameOn
		if pressed_keys[K_UP]:
			if not direction == 2:
				direction = 1
		if pressed_keys[K_DOWN]:
			if not direction == 1:
				direction = 2
		if pressed_keys[K_LEFT]:
			if not direction == 4:
				direction = 3
		if pressed_keys[K_RIGHT]:
			if not direction == 3:
				direction = 4

		if direction == 1:
			self.rect.move_ip(0, speed*-1)
		if direction == 2:
			self.rect.move_ip(0, speed)
		if direction == 3:
			self.rect.move_ip(speed*-1, 0)
		if direction == 4:
			self.rect.move_ip(speed, 0)

		if self.rect.left < 0:
			self.kill()
			destroy()
		if self.rect.right > SCREEN_WIDTH:
			self.kill()
			destroy()
		if self.rect.top < 0:
			self.kill()
			destroy()
		if self.rect.bottom > SCREEN_HEIGHT:
			self.kill()
			destroy()

		if pygame.sprite.spritecollide(self, snake_body_parts, False):
			destroy()

		screen.blit(self.surf, self.rect)


class SnakeBodyPart(pygame.sprite.Sprite):
	def __init__(self):
		super(SnakeBodyPart, self).__init__()
		self.surf = pygame.Surface((25, 25))
		self.surf.fill((168, 230, 29))
		self.rect = self.surf.get_rect()

	def update(self):
		screen.blit(self.surf, self.rect)


class Apple(pygame.sprite.Sprite):
	def __init__(self):
		super(Apple, self).__init__()
		self.surf = pygame.Surface((25, 25))
		self.surf.fill((255, 0, 0))
		self.rect = self.surf.get_rect()

	def update(self):
		global length
		if self.rect.colliderect(snake.rect):
			self.rect.x = (random.randint(0, int(SCREEN_WIDTH/25))*25)
			self.rect.y = (random.randint(0, int(SCREEN_HEIGHT/25))*25)
			if self.rect.x == SCREEN_WIDTH:
				self.rect.x -= 25
			if self.rect.y == SCREEN_WIDTH:
				self.rect.y -= 25
			length += 10

		if pygame.sprite.spritecollide(self, snake_body_parts, False):
			self.rect.x = (random.randint(0, int(SCREEN_WIDTH / 25)) * 25)
			self.rect.y = (random.randint(0, int(SCREEN_HEIGHT / 25)) * 25)
			if self.rect.x == SCREEN_WIDTH:
				self.rect.x -= 25
			if self.rect.y == SCREEN_WIDTH:
				self.rect.y -= 25

		screen.blit(self.surf, self.rect)


begin_button_image = pygame.image.load('begin_button.png')
exit_button_image = pygame.image.load('exit_button.png')
back_to_menu_image = pygame.image.load('back_to_menu_button.png')

begin_button = Button(10, 10, begin_button_image, 8)
exit_button = Button(10, 110, exit_button_image, 8)
back_to_menu_button = Button(10, 10, back_to_menu_image, 8)

menu_image = pygame.image.load('menu_screen.png')
menu_image = pygame.transform.scale(menu_image, (750, 750))

death_image = pygame.image.load('death_screen.png')
death_image = pygame.transform.scale(death_image, (750, 750))

snake_body_parts = pygame.sprite.Group()
snake = SnakeHead()
snake.rect.move_ip(300, 300)

apple = Apple()

apple.rect.x = (random.randint(0, int(SCREEN_WIDTH/25))*25)
apple.rect.y = (random.randint(0, int(SCREEN_HEIGHT/25))*25)
if apple.rect.x == SCREEN_WIDTH:
	apple.rect.x -= 25
if apple.rect.y == SCREEN_WIDTH:
	apple.rect.y -= 25

length = 3

clock = pygame.time.Clock()
game_phase = 0
gameOn = True


def gameplay():
	screen.fill((0, 0, 0))
	global gameOn
	achieved_length = 0
	while gameOn:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		keys = pygame.key.get_pressed()

		screen.fill((0, 0, 0))

		if achieved_length == length:
			list(snake_body_parts)[0].kill()
			achieved_length -= 1

		new_snake_body_part = SnakeBodyPart()
		snake_body_parts.add(new_snake_body_part)
		achieved_length += 1
		screen.blit(list(snake_body_parts)[-1].surf, snake.rect)
		list(snake_body_parts)[-1].rect.move_ip(snake.rect.x, snake.rect.y)

		for s in snake_body_parts:
			s.update()
		apple.update()
		snake.update(keys)
		pygame.display.flip()
		clock.tick(5)


def main_menu():
	screen.fill((0, 0, 0))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.blit(menu_image, (0, 0))
		if exit_button.update():
			pygame.quit()
			sys.exit()
		if begin_button.update():
			gameplay()
		pygame.display.flip()


def death_screen():
	global length
	screen.fill((0, 0, 0))
	snake.rect.x = 300
	snake.rect.y = 300
	length = 3
	for s in snake_body_parts:
		s.kill()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.blit(death_image, (0, 0))
		if back_to_menu_button.update():
			main_menu()
		pygame.display.flip()


main_menu()
