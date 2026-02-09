import pygame
import string

pygame.init()

class GUI:
    BACKGROUND_COLOUR = (39, 170, 13)
    SECONDARY_COLOUR = (255, 247, 234)
    PRIMARY_COLOUR = (10, 10, 10)


    def __init__(self, game):
        self.game = game

        self.screen = pygame.display.set_mode((500, 500))
        self.font = pygame.font.SysFont("JetBrains Mono", 20)

        self.multiplier_lookup = {
            (2, False): (0, 255, 255),  # CYAN
            (3, False): (0, 0, 255),    # BLUE
            (2, True): (255, 0, 255),   # MAGENTA
            (3, True): (255, 0, 0),     # RED
        }

        self.character_lookup = {}
        self.generate_characters()

        self.board_surface = None
        self.generate_board()

    def generate_characters(self):
        targets = list(string.ascii_lowercase + "? ")

        for target in targets:
            surface = pygame.Surface((24, 24))
            surface.fill(self.SECONDARY_COLOUR)

            pygame.draw.rect(
                surface,
                self.PRIMARY_COLOUR,
                (0, 0, 24, 24),
                width=1
            )

            text_surface = self.font.render(target.upper(), True, self.PRIMARY_COLOUR)
            surface.blit(text_surface, (12 - (text_surface.get_width() / 2), 12 - (text_surface.get_height() / 2)))

            self.character_lookup[target] = surface

    def generate_board(self):
        tile_size = 24
        tile_spacing = 1

        surface_size = (tile_size + tile_spacing) * 15
        surface = pygame.Surface((surface_size, surface_size))

        for x in range(15):
            for y in range(15):
                px = x * (tile_size + tile_spacing)
                py = y * (tile_size + tile_spacing)

                tile = self.game.board.get(x, y)
                search = (tile.multiplier, tile.is_word_multiplier)

                colour = self.BACKGROUND_COLOUR
                if search in self.multiplier_lookup:
                    colour = self.multiplier_lookup[search]

                pygame.draw.rect(
                    surface,
                    colour,
                    (px, py, tile_size, tile_size),
                )

                pygame.draw.rect(
                    surface,
                    self.SECONDARY_COLOUR,
                    (px, py, tile_size+1, tile_size+1),
                    width=1
                )

        self.board_surface = surface

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(-1)

        self.screen.fill((250, 250, 250))

        offset_x = (self.screen.get_width() - self.board_surface.get_width()) / 2
        offset_y = (self.screen.get_height() - self.board_surface.get_height()) / 2
        self.screen.blit(self.board_surface, (offset_x, offset_y))

        tile_size = 24
        tile_spacing = 1
        for x in range(15):
            for y in range(15):
                px = x * (tile_size + tile_spacing) + offset_x
                py = y * (tile_size + tile_spacing) + offset_y

                tile = self.game.board.get(x, y)

                if tile.letter:
                    surf = self.character_lookup[tile.letter]
                    self.screen.blit(surf, (px, py))



        pygame.display.flip()

