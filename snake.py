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
import button_template as bt

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

font = pygame.font.SysFont('bigcaslonttf', 48)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
direction = 1

speed = 25


def destroy():
	global gameOn
	death_screen()
	gameOn = False


class SnakeHead(pygame.sprite.Sprite):
	def __init__(self):
		super(SnakeHead, self).__init__()
		self.surf = pygame.Surface((23, 23))
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
		elif pressed_keys[K_DOWN]:
			if not direction == 1:
				direction = 2
		elif pressed_keys[K_LEFT]:
			if not direction == 4:
				direction = 3
		elif pressed_keys[K_RIGHT]:
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
		self.surf = pygame.Surface((23, 23))
		self.surf.fill((168, 230, 29))
		self.rect = self.surf.get_rect()

	def update(self):
		screen.blit(self.surf, self.rect)


class Apple(pygame.sprite.Sprite):
	def __init__(self):
		super(Apple, self).__init__()
		self.surf = pygame.Surface((23, 23))
		self.surf.fill((255, 0, 0))
		self.rect = self.surf.get_rect()

	def update(self):
		global length
		global score
		if self.rect.colliderect(snake.rect):
			self.rect.x = (random.randint(0, int(SCREEN_WIDTH/25))*25)
			self.rect.y = (random.randint(0, int(SCREEN_HEIGHT/25))*25)
			if self.rect.x == SCREEN_WIDTH:
				self.rect.x -= 25
			if self.rect.y == SCREEN_WIDTH:
				self.rect.y -= 25
			length += 1
			score += 1

		if pygame.sprite.spritecollide(self, snake_body_parts, False):
			self.rect.x = (random.randint(0, int(SCREEN_WIDTH / 25)) * 25)
			self.rect.y = (random.randint(0, int(SCREEN_HEIGHT / 25)) * 25)
			if self.rect.x == SCREEN_WIDTH:
				self.rect.x -= 25
			if self.rect.y == SCREEN_WIDTH:
				self.rect.y -= 25

		screen.blit(self.surf, self.rect)


eazy_difficulty_image = pygame.image.load('eazy_difficulty_text.png')
normal_difficulty_image = pygame.image.load('normal_difficulty_text.png')
hard_difficulty_image = pygame.image.load('hard_difficulty_text.png')
difficulty_selection = bt.Button(10, 300, eazy_difficulty_image, 6)

difficulty = 0
difficulty_to_speed = {0: 6, 1: 9, 2: 11}

game_speed = difficulty_to_speed[difficulty]


begin_button_image = pygame.image.load('begin_button.png')
exit_button_image = pygame.image.load('exit_button.png')
back_to_menu_image = pygame.image.load('back_to_menu_button.png')

begin_button = bt.Button(10, 10, begin_button_image, 6)
exit_button = bt.Button(10, 110, exit_button_image, 6)
back_to_menu_button = bt.Button(10, 10, back_to_menu_image, 5)

menu_image = pygame.image.load('menu_screen.png')
menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

death_image = pygame.image.load('death_screen.png')
death_image = pygame.transform.scale(death_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
	global gameOn
	global score
	global game_speed
	screen.fill((0, 0, 0))
	achieved_length = 0
	score = 0
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
		clock.tick(game_speed)


def main_menu():
	global game_speed
	global difficulty
	screen.fill((0, 0, 0))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.blit(menu_image, (0, 0))
		if exit_button.update(screen):
			pygame.quit()
			sys.exit()
		if begin_button.update(screen):
			gameplay()
		if difficulty_selection.update(screen):
			difficulty = (difficulty+1) % 3
			print(difficulty)
			if difficulty == 0:
				difficulty_selection.swap_image(10, 300, eazy_difficulty_image, 6)
				game_speed = difficulty_to_speed[difficulty]
			elif difficulty == 1:
				difficulty_selection.swap_image(10, 300, normal_difficulty_image, 6)
				game_speed = difficulty_to_speed[difficulty]
			elif difficulty == 2:
				difficulty_selection.swap_image(10, 300, hard_difficulty_image, 6)
				game_speed = difficulty_to_speed[difficulty]
		pygame.display.flip()


def death_screen():
	global length
	global score
	img = font.render(str(score), True, (0, 0, 0))
	score = 0
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
		if back_to_menu_button.update(screen):
			main_menu()

		screen.blit(img, (372, 410))
		pygame.display.flip()


main_menu()
