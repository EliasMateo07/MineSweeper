import pygame
import sys
import random


class Square(pygame.sprite.Sprite):
 def __init__(self, square_rect):
     super().__init__()
     self.image = pygame.Surface(square_rect)
 
     self.value = 0
     if (row % 2) == (column % 2):
         self.image.fill(GREEN)
         self.color = GREEN
     else:
         self.image.fill(DARKGREEN)
         self.color = DARKGREEN
     self.rect = self.image.get_rect()
     self.is_bomb = False
     self.revealed = False
     self.flagged = False
 def update(self):
      if self.revealed and self.value != 0:
         font = pygame.font.SysFont("arial", 30)
         text_surface = font.render(str(square.value), True, BLACK)
         text_rect = text_surface.get_rect(center=square.rect.center)
         screen.blit(text_surface, text_rect)
      elif self.flagged:
           screen.blit(Flag.image, (square.rect.x + 4, square.rect.y+1))


class Sprite(pygame.sprite.Sprite):
   def __init__(self, image, position):
       super().__init__()
       self.image = image
       self.rect = self.image.get_rect()
       self.rect.topleft = position
       sprite_group.add(self)


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, position, color):
        super().__init__()
        self.font = font
        self.color = color
        self.update_text(text)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    def update_text(self, text):
        self.image = self.font.render(text, True, self.color)


class BlockSprite(pygame.sprite.Sprite):
   def __init__(self, surface_size, color, position):
       super().__init__()
       self.image = pygame.Surface(surface_size)
       self.rect = pause_button.image.get_rect()
       self.image.fill(color)
       self.rect.x, self.rect.y = position[0], position[1]


def surroundings(main_square, all_squares):
 square_coords = main_square.rect.x, main_square.rect.y
 list = []
 for square in all_squares:
     if square != main_square:
         if (abs(square.rect.x - square_coords[0]) <= 50 and
             abs(square.rect.y - square_coords[1]) <= 50):
             list.append(square)
 return list


def reveal_zero_squares(square, all_squares):
  square.revealed = True
  square.image.fill(WHITE)
  surrounding_squares = surroundings(square, all_squares)
  for adjacent_square in surrounding_squares:
      if not adjacent_square.revealed and adjacent_square.value == 0:
          reveal_zero_squares(adjacent_square, all_squares)
      elif not adjacent_square.is_bomb and not adjacent_square.revealed:
          adjacent_square.revealed = True
          adjacent_square.image.fill(WHITE)
def win(all_squares):
    for square in all_squares:
      if square.is_bomb or square.revealed:
          continue
      else:
          return False
    border = BlockSprite(surface_size=(520, 145), color=(168, 139, 20), position=(140, 90))
    win_menu = BlockSprite(surface_size=(500, 125), color=(214, 176, 19), position=(150, 100))
    win_text = TextSprite("YOU WIN", title, (win_menu.rect.centerx+125, win_menu.rect.centery), BLACK)
    sprites.add(border, win_menu, win_text)
    return True
def pause(surface, paused):
  if not paused:
       border = BlockSprite(surface_size=(520, 145), color=(173, 59, 17), position=(140, 90))
       pause_menu = BlockSprite(surface_size=(500, 125), color=(212, 160, 108), position=(150, 100))
       pause_text = TextSprite("PAUSED", title, (pause_menu.rect.centerx+125, pause_menu.rect.centery), BLACK)
       sprites.add(border, pause_menu, pause_text)
       surface.fill(transparent)
       print("pause")
       pause_button.image = sprite_images[1]
       paused = True
  elif paused:
      sprites.empty()
      print("unpause")
      pause_button.image = sprite_images[0]
      paused = False
  return surface, paused


def difficulty_dropdown(dropdown_border=None, dropdown=None, list=[]):
    global diff_menu
    if not diff_menu:
        arrow.update_text("▲")
        dropdown_border = BlockSprite((137, 77), BLACK, (149, 44))
        dropdown = BlockSprite((135, 76), WHITE, (150, 44))
        for index, item in enumerate(diff_text):
            text = TextSprite(diff_text[index], small_font, (158, (44+ (40*index if index != 2 else 40))), BLACK)
            text.text = diff_text[index]
            list.append(text)
        sprite_group.add(dropdown_border, dropdown, (text for text in list))
        return dropdown, dropdown_border, list
    if diff_menu:
        arrow.update_text("▼")
        for text in list:  # Remove all text sprites from the list
            sprite_group.remove(text)
        list.clear()  # Clear the list
        sprite_group.remove(dropdown_border, dropdown)
       
def explode(dead, border=None, lose_menu=None, lose_text=None, reset_border=None, reset_button=None, reset_text=None):
    if not dead:
        border = BlockSprite(surface_size=(520, 265), color=(173, 59, 17), position=(140, 90))
        lose_menu = BlockSprite(surface_size=(500, 245), color=(212, 160, 108), position=(150, 100))
        lose_text = TextSprite("YOU LOSE", title, (lose_menu.rect.centerx+100, lose_menu.rect.centery), BLACK)


        reset_border = BlockSprite(surface_size=(240, 110), color=(166, 22, 22), position=(280, 215))
        reset_button = BlockSprite(surface_size=(230, 100), color=(245, 15, 15), position=(285, 220))
        reset_text = TextSprite("RESET", title, (reset_button.rect.centerx+5, reset_button.rect.centery-10), BLACK)


        sprites.add(border, lose_menu, lose_text, reset_border, reset_button, reset_text)


        dead = True
        return dead, border, lose_menu, lose_text, reset_border, reset_button, reset_text


    if dead:
        sprites.remove(border, lose_menu, lose_text, reset_border, reset_button, reset_text)


# Initialize Pygame
pygame.init()
GREEN = (32,223,81)
DARKGREEN = (79, 176, 89)
BLACK = (0,0,0)

WHITE = (255, 255, 255)
RED = (255,0,0)
transparent = (0,0,0,128)


### SCREEN
SCREEN_WIDTH, SCREEN_HEIGHT = 16, 16
screen = pygame.display.set_mode((SCREEN_WIDTH*50, (SCREEN_HEIGHT*50)+50))
pygame.display.set_caption("MineSweeper")




### GROUPS
all_squares = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()
sprites = pygame.sprite.Group()


### FONTS
font = pygame.font.SysFont("arial", 48)
small_font = pygame.font.SysFont("arial", 30, bold=True)
title = pygame.font.SysFont("arial", 60, bold=True)


#### GAME GRID
difficulties= {1: (10,10,"Easy",10), 2: (16,16, "Medium",40), 3: (30,16,"Hard",99)}
diff_text = ["Easy", "Hard"]
difficulty = difficulties[2][2]
squares = []
grid = difficulties[2][:2]
square_rect = (50, 50)
for column in range(grid[0]):
 for row in range(grid[1]):
      square = Square(square_rect)
      square.rect.x = (column * 50)
      square.rect.y = 50+(row * 50)
      squares.append(square)
all_squares.add(squares)
mode_change = False




### BOMBS
bombs = 40
bomb_list = random.sample(squares, bombs)
for bomb in bomb_list:
 bomb.is_bomb = True
for bomb in bomb_list:
 surrounding_squares = surroundings(bomb, squares)
 for square in surrounding_squares:
     if not square.is_bomb:
         square.value += 1




### SPRITES
surface = pygame.Surface((SCREEN_WIDTH*50, SCREEN_HEIGHT*50), pygame.SRCALPHA)
pause_button = pygame.sprite.Sprite()
pngs = ["Pause_sprite.png", "Resume_sprite.png", "Clock_sprite.png", "Flag.png"]
sprite_images = []
for index, item in enumerate(pngs):
   sprite = pygame.image.load(f"sprites/{item}")
   sprite = pygame.transform.scale(sprite, (square_rect[0], square_rect[1]))
   sprite_images.append(sprite)
 
pause_button = Sprite(sprite_images[0], ((SCREEN_WIDTH*50)-180,0))
Flag = Sprite(sprite_images[3], ((SCREEN_WIDTH*50)-110,1))
Timer = Sprite(sprite_images[2], (0,0))
flag_num = 40
difference = 0
dead = False


### MENU
menu_border = BlockSprite((137, 40), BLACK, (149, 4))
menu = BlockSprite((135, 38), WHITE, (150, 5))
menu_text = TextSprite(difficulty, small_font, (158, 5), BLACK)
arrow = TextSprite("▼", small_font, (258, 5), BLACK)
sprite_group.add(menu_border, menu, menu_text, arrow)
time_mode_difference = 0


### MAIN LOOP ###
running = True
paused = False
diff_menu = False
dead = False
while running:


    ### TIME AND FLAGS
   time = (pygame.time.get_ticks()//1000) - difference - time_mode_difference
   if not paused and not dead:
      time_surface = font.render(str(time), True, BLACK)
      flag_surf = font.render(": " + str(flag_num), True, BLACK)
   screen.fill(GREEN)


   if mode_change:
        #### SCREEN AND SPRITES
        screen = pygame.display.set_mode((SCREEN_WIDTH*50, (SCREEN_HEIGHT*50)+50))
        surface = pygame.Surface((SCREEN_WIDTH*50, (SCREEN_HEIGHT*50)+50), pygame.SRCALPHA)
        pause_button.kill()
        pause_button = Sprite(sprite_images[0], ((SCREEN_WIDTH*50)-180,0))
        Flag.kill()
        Flag = Sprite(sprite_images[3], ((SCREEN_WIDTH*50)-110,1))
        time_mode_difference += time


        ## GAME GRID
        all_squares.empty()
        squares = []
        for column in range(grid[0]):
            for row in range(grid[1]):
                square = Square(square_rect)
                square.rect.x = (column * 50)
                square.rect.y = 50+(row * 50)
                squares.append(square)
        all_squares.add(squares)


        ### BOMBS
        bomb_list = random.sample(squares, bombs)
        for bomb in bomb_list:
            bomb.is_bomb = True
        for bomb in bomb_list:
            surrounding_squares = surroundings(bomb, squares)
            for square in surrounding_squares:
                if not square.is_bomb:
                    square.value += 1
        flag_num = bombs




        ### MENU
        menu_text.kill()
        menu_text = TextSprite(difficulty, small_font, (158, 5), BLACK)
        sprite_group.add(menu_text)
        mode_change = False
       
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
         running = False
       elif event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1:
                if dead:
                    if reset_border.rect.collidepoint(event.pos)\
                    or reset_button.rect.collidepoint(event.pos) or reset_text.rect.collidepoint(event.pos):
                        explode(dead, border, lose_menu, lose_text, reset_border, reset_button, reset_text)
                        mode_change = True
                        dead = False
                elif not paused and not diff_menu and not dead:
                    for square in all_squares:
                        if square.rect.collidepoint(event.pos):
                            clicked_square = square
                            if square.is_bomb:
                                dead, border, lose_menu, lose_text, reset_border, reset_button, reset_text = explode(dead)
                                square.image.fill(RED)
                                   
                            elif not square.is_bomb and not square.flagged:
                                square.image.fill(WHITE)
                                square.revealed = True
                                if square.value == 0:
                                    # If the clicked square has a value of zero, reveal all adjacent squares recursively
                                        reveal_zero_squares(clicked_square, all_squares)
                   
                if pause_button.rect.collidepoint(event.pos):
                    if not paused:
                        time_start = time
                    surface, paused = pause(surface, paused)
                    difference = time - time_start      
                elif menu.rect.collidepoint(event.pos) or menu_text.rect.collidepoint(event.pos)\
                    or arrow.rect.collidepoint(event.pos):
                    if not diff_menu:
                        dropdown, dropdown_border, dropdown_list = difficulty_dropdown()
                        diff_menu =True
                    elif diff_menu:
                        difficulty_dropdown(dropdown_border,dropdown, dropdown_list)
                        diff_menu =False
                       
                elif diff_menu:
                    for index, text in enumerate(dropdown_list):
                        if text.rect.collidepoint(event.pos):
                            if text.text == "Hard":
                                # Update difficulty settings for hard mode
                                diff_text = ["Easy", "Medium"]
                                grid = difficulties[3][:2]
                                difficulty = difficulties[3][2]
                                SCREEN_WIDTH, SCREEN_HEIGHT = difficulties[3][:2]
                                bombs = difficulties[3][3]
                                mode_change = True
                               


                            elif text.text == "Easy":
                                # Update difficulty settings for easy mode
                                for text in dropdown_list:
                                    sprite_group.remove(text)
                                diff_text = ["Medium", "Hard"]
                                grid = difficulties[1][:2]
                                difficulty = difficulties[1][2]
                                SCREEN_WIDTH, SCREEN_HEIGHT = difficulties[1][:2]
                                bombs = difficulties[1][3]
                                mode_change = True
                            elif text.text == "Medium":
                               
                                # Update difficulty settings for medium mode
                                for text in dropdown_list:
                                    sprite_group.remove(text)
                                diff_text = ["Easy", "Hard"]
                                grid = difficulties[2][:2]
                                difficulty = difficulties[2][2]
                                SCREEN_WIDTH, SCREEN_HEIGHT = difficulties[2][:2]
                                bombs = difficulties[2][3]
                                mode_change = True


                            # Close the dropdown menu
                           
                            difficulty_dropdown(dropdown_border, dropdown, dropdown_list)
                            diff_menu = False
               
           elif event.button == 3:
               if not paused:
                   for square in all_squares:
                       if square.rect.collidepoint(event.pos):
                           if not square.revealed:
                               if not square.flagged:
                                   square.flagged = True
                                   flag_num -= 1
                               else:
                                   square.image.fill(square.color)
                                   square.flagged = False
                                   flag_num += 1


   if win(all_squares):
       paused = True
       
   all_squares.draw(screen)
   for square in all_squares:
       square.update()
   screen.blit(time_surface, (49, -3))
   if paused:
       screen.blit(surface, (0, 0))
   if not paused:
       for sprite in sprite_group:
           sprite.image.set_alpha(255)
       sprite_group.draw(screen)
   else:
       for sprite in sprite_group:
           sprite.image.set_alpha(90)
       sprite_group.draw(screen)
   sprites.draw(screen)
   screen.blit(flag_surf, ((SCREEN_WIDTH*50)-70, 0))
   pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
