import pygame
from enum import Enum
from settings import Settings
import time
import random

class GameState(Enum):
    MENU = 1
    PLAYING = 2

class DropItem:
    """Item dropado após colher uma planta"""
    def __init__(self, x, y, image, lifetime=2):
        self.x = x
        self.y = y
        self.image = image
        self.spawn_time = time.time()
        self.lifetime = lifetime  # segundos

    def is_alive(self):
        return time.time() - self.spawn_time < self.lifetime


class Field:
    def __init__(self, x, y, w=5, h=3):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.plants = [[0 for _ in range(w)] for _ in range(h)]
        self.spawn_times = [[None for _ in range(w)] for _ in range(h)]  # ⏱️ tempo de plantio de cada célula


class Game:
    def __init__(self, settings: Settings):
        self._settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self._settings.WIDTH, self._settings.HEIGHT)
        )
        pygame.display.set_caption("Butterfly's Garden 🌾")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.font_button = pygame.font.SysFont(None, 20)
        self.running = True
        self._gameState = GameState.MENU
        self.TILES_SIZE = 32

        self.map_data = [
            [0 for _ in range(settings.WIDTH // self.TILES_SIZE)]
            for _ in range(settings.HEIGHT // self.TILES_SIZE)
        ]

        self.fields = [
            Field(1, 1), Field(1, 5), Field(1, 9),
            Field(7, 1), Field(7, 9), Field(13, 1),
            Field(13, 5), Field(13, 9)
        ]

        # Carrega o tileset e redimensiona
        ground_img = pygame.image.load("assets/misc.png").convert_alpha()
        scale_factor = 2
        ground_img = pygame.transform.scale(
            ground_img,
            (ground_img.get_width() * scale_factor, ground_img.get_height() * scale_factor)
        )
        self._tiles = self.load_tiles(ground_img, self.TILES_SIZE)

        plant_img = pygame.image.load("assets/plant.png").convert_alpha()
        plant_img = pygame.transform.scale(
            plant_img,
            (plant_img.get_width() * scale_factor, plant_img.get_height() * scale_factor)
        )
        self._plants = self.load_tiles(plant_img, self.TILES_SIZE)

        # Botão plantar
        self.plant_mode = False
        self.plant_button_rect = pygame.Rect(10, 10, 55, 20)

        # Intervalos de crescimento (em segundos)
        self.stage_intervals = [0, 5, 10]  # tempo para passar do estágio 1→2→3

        # Itens dropados
        self.drops = []

    def load_tiles(self, tileset, tile_size):
        tiles = []
        for y in range(0, tileset.get_height(), tile_size):
            for x in range(0, tileset.get_width(), tile_size):
                rect = pygame.Rect(x, y, tile_size, tile_size)
                image = tileset.subsurface(rect)
                tiles.append(image)
        return tiles

    def run(self):
        while self.running:
            self.update()

    def update(self):
        if self._gameState == GameState.MENU:
            self.menu_events()
            self.draw_menu()
        elif self._gameState == GameState.PLAYING:
            self.game_events()
            self.update_growth()
            self.update_drops()
            self.draw_game()
        self.clock.tick(60)

    # === MENU ===
    def menu_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.start_rect = pygame.Rect(
            (self._settings.WIDTH // 2 - 100, self._settings.HEIGHT // 2 - 80), (200, 60)
        )
        self.quit_rect = pygame.Rect(
            (self._settings.WIDTH // 2 - 100, self._settings.HEIGHT // 2 + 20), (200, 60)
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(event.pos):
                    self._gameState = GameState.PLAYING
                elif self.quit_rect.collidepoint(event.pos):
                    self.running = False

    def draw_menu(self):
        button_color = (70, 130, 180)
        hover_color = (100, 180, 255)
        text_color = (255, 255, 255)
        self.screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()
        cursor_set = False

        if self.start_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, self.start_rect, border_radius=10)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_set = True
        else:
            pygame.draw.rect(self.screen, button_color, self.start_rect, border_radius=10)

        if self.quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, self.quit_rect, border_radius=10)
            if not cursor_set:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                cursor_set = True
        else:
            pygame.draw.rect(self.screen, button_color, self.quit_rect, border_radius=10)

        if not (self.start_rect.collidepoint(mouse_pos) or self.quit_rect.collidepoint(mouse_pos)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        start_text = self.font.render("Iniciar", True, text_color)
        quit_text = self.font.render("Sair", True, text_color)
        self.screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=self.quit_rect.center))
        pygame.display.flip()

    # === GAME ===
    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._gameState = GameState.MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.plant_button_rect.collidepoint(event.pos):
                    self.plant_mode = not self.plant_mode
                elif self.plant_mode:
                    self.handle_click(event.pos)
                else:
                    self.handle_harvest(event.pos)

    def handle_click(self, mouse_pos):
        """Planta uma muda com tempo próprio"""
        tile_x = mouse_pos[0] // self.TILES_SIZE
        tile_y = mouse_pos[1] // self.TILES_SIZE

        for field in self.fields:
            if field.x <= tile_x < field.x + field.w and field.y <= tile_y < field.y + field.h:
                lx = tile_x - field.x
                ly = tile_y - field.y
                if field.plants[ly][lx] == 0:
                    field.plants[ly][lx] = 1
                    field.spawn_times[ly][lx] = time.time()  # marca tempo de plantio
                break

    def handle_harvest(self, mouse_pos):
        """Colhe planta se estiver madura"""
        tile_x = mouse_pos[0] // self.TILES_SIZE
        tile_y = mouse_pos[1] // self.TILES_SIZE

        for field in self.fields:
            if field.x <= tile_x < field.x + field.w and field.y <= tile_y < field.y + field.h:
                lx = tile_x - field.x
                ly = tile_y - field.y
                if field.plants[ly][lx] == 3:
                    field.plants[ly][lx] = 0
                    field.spawn_times[ly][lx] = None
                    drop_img = self._plants[5]
                    self.drops.append(DropItem(tile_x, tile_y, drop_img))
                break

    def update_growth(self):
        """Cresce plantas baseado no tempo de plantio individual"""
        now = time.time()
        for field in self.fields:
            for y in range(field.h):
                for x in range(field.w):
                    stage = field.plants[y][x]
                    spawn_time = field.spawn_times[y][x]
                    if stage > 0 and spawn_time:
                        elapsed = now - spawn_time
                        # Define estágio baseado no tempo passado
                        if elapsed >= self.stage_intervals[2]:
                            field.plants[y][x] = 3
                        elif elapsed >= self.stage_intervals[1]:
                            field.plants[y][x] = 2
                        else:
                            field.plants[y][x] = 1

    def update_drops(self):
        self.drops = [drop for drop in self.drops if drop.is_alive()]

    def draw_map(self, map_data):
        for field in self.fields:
            for row in range(field.h):
                for col in range(field.w):
                    mx = field.x + col
                    my = field.y + row
                    if 0 <= mx < len(map_data[0]) and 0 <= my < len(map_data):
                        map_data[my][mx] = 1

        for y, row in enumerate(map_data):
            for x, tile_index in enumerate(row):
                tile = self._tiles[tile_index]
                if tile_index != 0:
                    self.screen.blit(tile, (x * self.TILES_SIZE, y * self.TILES_SIZE))

    def draw_game(self):
        self.screen.fill((20, 100, 40))
        self.draw_map(self.map_data)

        # 🌿 desenha plantas
        for field in self.fields:
            for row in range(field.h):
                for col in range(field.w):
                    stage = field.plants[row][col]
                    if stage > 0:
                        mx = field.x + col
                        my = field.y + row
                        img = self._plants[min(stage + 6, len(self._plants) - 1)]
                        self.screen.blit(img, (mx * self.TILES_SIZE, my * self.TILES_SIZE))

        # 💎 desenha drops
        for drop in self.drops:
            self.screen.blit(drop.image, (drop.x * self.TILES_SIZE, drop.y * self.TILES_SIZE))

        # Botão plantar
        color = (34, 139, 34) if not self.plant_mode else (125, 35, 35)
        pygame.draw.rect(self.screen, color, self.plant_button_rect, border_radius=8)
        text = self.font_button.render("Plantar" if not self.plant_mode else "Parar", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=self.plant_button_rect.center))

        pygame.display.flip()
