import pygame
import os
import sys

pygame.init()
pygame.key.set_repeat(200, 70)

screen_size = (1000, 635)
screen = pygame.display.set_mode(screen_size)
FPS = 120

player = None
all_sprites = pygame.sprite.Group()
map_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(startscreen_image, screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


startscreen_image = load_image('startscreen.png')
room_image = load_image('room_test.png')
player_image = load_image('hero.png', color_key=-1)
cellsizew = 125
cellsizeh = 127


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(self.pos)


class Room(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(map_group, all_sprites)
        self.image = room_image
        self.rect = self.image.get_rect().move(0, 0)
        self.abs_pos = (self.rect.x, self.rect.y)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])


start_screen()
bg = Room()
debug_mode = False
hero = generate_level(player)
player = Player(470, 257)
room_coords = {'x': 0, 'y': 0}
objective_rooms = [(8, 2), (8, 5), (-1, 3), (6, 9)]
obj_count = 0
pygame.font.init()
font = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if debug_mode == True:
                print(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RALT:
                if debug_mode == False:
                    debug_mode = True
                    print('debug_mode enabled')
                    font = 'serif'
                elif debug_mode == True:
                    debug_mode = False
                    print('debug_mode disabled')
                    font = None
            elif event.key == pygame.K_a:
                if player.rect.x >= 100:
                    player.rect.x -= 15
            elif event.key == pygame.K_d:
                if player.rect.x <= 871:
                    player.rect.x += 15
            elif event.key == pygame.K_w:
                if player.rect.y >= 75:
                    player.rect.y -= 15
            elif event.key == pygame.K_s:
                if player.rect.y <= 471:
                    player.rect.y += 15
        if player.rect.y in range(260, 300) and player.rect.x in range(80, 110):
            player.rect.x = 840
            player.rect.y = 280
            room_coords['x'] -= 1
            if debug_mode == True:
                print(room_coords)
        elif player.rect.y in range(269, 310) and player.rect.x in range(868, 886):
            player.rect.x = 131
            player.rect.y = 281
            room_coords['x'] += 1
            if debug_mode == True:
                print(room_coords)
        elif player.rect.y in range(68, 81) and player.rect.x in range(468, 500):
            player.rect.x = 475
            player.rect.y = 445
            room_coords['y'] += 1
            if debug_mode == True:
                print(room_coords)
        elif player.rect.y in range(475, 496) and player.rect.x in range(451, 487):
            player.rect.x = 481
            player.rect.y = 118
            room_coords['y'] -= 1
            if debug_mode == True:
                print(room_coords)
        elif room_coords['x'] == objective_rooms[obj_count][0] and room_coords['y'] == objective_rooms[obj_count][1]:
            obj_count += 1
        if room_coords['x'] == 6 and room_coords['y'] == 9:
            room_coords['x'] = 'you'
            room_coords['y'] = 'win'
    screen.fill(pygame.Color(0, 0, 0))
    map_group.draw(screen)
    player_group.draw(screen)
    f1 = pygame.font.Font(None, 32)
    text1 = f1.render('Room: {} - {}'.format(room_coords['x'], room_coords['y']), True,
                      (255, 255, 255))
    text2 = f1.render('Objective: {} - {}'.format(objective_rooms[obj_count][0], objective_rooms[obj_count][1]), True,
                      (255, 255, 255))
    screen.blit(text1, (730, 35))
    screen.blit(text2, (120, 35))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
