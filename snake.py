import pygame,sys,random,shelve
from pygame.math import Vector2

class SNAKE:
	# Deals with drawing and creating the snake
	def __init__(self):
		# Initializes the snake vectors
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False
	# Loads all images and sound for snake
		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
	# Begins to draw the snake
	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()
		# Creates the snake and length
		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)
	# Changes the direction of the head
	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down
	# Changes the direction of the tail
	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
	# Moves the snake
	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
	# Adds blocks to the snake
	def add_block(self):
		self.new_block = True
	# Plays the sound for eating the apple
	def play_crunch_sound(self):
		self.crunch_sound.play()
	# Resets the snake when it dies
	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	# Initializes the fruit
	def __init__(self):
		self.randomize()
	# Draws the fruit
	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)
	# Randomizes the location
	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	# Initializes then snake and the fruit
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
	# Updates the graphics
	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()
	# Draws the elements
	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()
		self.draw_high()
	# Checks for the collision with the fruit
	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:

			if d['score'] <= int(score_text):
				d['score'] += 1

			hscore = d['score']
			if int(score_text) > hscore:
				hscore = int(score_text) + 1
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()
	# Checks for a collision with itself or the wall
	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				print("Self Collision Detected")
				self.game_over()
	# Resets the name
	def game_over(self):
		self.snake.reset()
	# Draws grass
	def draw_grass(self):
		grass_color = (0,102,255)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			
	# Draws the high score
	def draw_high(self):
		global d
		h_score_text = str(d['score'])
		h_score_surface = game_font.render(h_score_text, True, (0,255,0))
		h_score_x = int(cell_size * cell_number - 60)
		h_score_y = int(40)
		h_score_rect = h_score_surface.get_rect(center = (h_score_x, h_score_y))
		apple_rect = apple.get_rect(midright = (h_score_rect.left,h_score_rect.centery))
		h_bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + h_score_rect.width + 6, apple_rect.height)
		
		pygame.draw.rect(screen, (0,0,255),h_bg_rect)
		screen.blit(h_score_surface,h_score_rect)
		screen.blit(apple, apple_rect)
		pygame.draw.rect(screen, (0,255,0),h_bg_rect,2)
	# Draws the current score
	def draw_score(self):
		global score_text
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(0,255,0))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(0,0,255),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(0,255,0),bg_rect,2)
# Initializes the sound
pygame.mixer.pre_init(44100,-16,2,512)
# Initializes Pygame
pygame.init()
# Sets the top bar text
pygame.display.set_caption("Snake")
# Sets the size of the grid squares
cell_size = 35
# Sets the number of cells in the grid
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

d = shelve.open('score.txt')
if not 'score' in d:
	d['score'] = 0

main_game = MAIN()

while True:
	pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)
		# if pressed[pygame.K_UP] and not pressed[pygame.K_LEFT]:
		# 	if main_game.snake.direction.y != 1:
		# 		main_game.snake.direction = Vector2(0,-1)
		# if pressed[pygame.K_RIGHT]:
		# 	if main_game.snake.direction.x != -1:
		# 		main_game.snake.direction = Vector2(1,0)
		# if pressed[pygame.K_DOWN]:
		# 	if main_game.snake.direction.y != -1:
		# 		main_game.snake.direction = Vector2(0,1)
		# if pressed[pygame.K_LEFT] and not pressed[pygame.K_UP]:
		# 	if main_game.snake.direction.x != 1:
		# 		main_game.snake.direction = Vector2(-1,0)

	screen.fill((0,0,255))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)
else:
	pygame.quit()