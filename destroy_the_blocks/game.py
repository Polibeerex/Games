import pygame

# initializing "PyGame" library
pygame.init()


class Game:
    """ Destroy the Blocks

    """
    finish = False
    lose = False
    win = False
    menu = True

    def __init__(self, bg_size, bg_color, pl_rect, pl_color,
                 pl_speed, ball_size, ball_color, ball_speed,
                 block_size, block_color, number_of_cols):

        self.bg_size = bg_size
        self.bg_color = bg_color
        self.pl_rect = pygame.Rect(pl_rect)
        self.pl_color = pl_color
        self.pl_speed = pl_speed
        self.ball_size = ball_size
        self.ball_color = ball_color
        self.ball_speed = ball_speed
        self.ball_pos = [int(bg_size[0] / 2), int(bg_size[1] / 2)]
        self.block_size = block_size
        self.block_color = block_color
        self.number_of_cols = number_of_cols
        self.screen = pygame.display.set_mode(self.bg_size)

    def background(self):
        self.screen.fill(self.bg_color)

    def platform(self):
        pygame.draw.rect(self.screen, self.pl_color, self.pl_rect)

    def platform_move(self, direction: bool):
        if direction:
            if self.pl_rect[0] < self.bg_size[0] - self.pl_rect[2]:
                # self.pl_rect[0] += self.pl_speed[0]
                self.pl_rect.move_ip(self.pl_speed[0], self.pl_speed[1])

        else:
            if self.pl_rect[0] > 0:
                # self.pl_rect[0] -= self.pl_speed[0]
                self.pl_rect.move_ip(-self.pl_speed[0],
                                     -self.pl_speed[1])

    def ball(self):
        pygame.draw.circle(self.screen, self.ball_color, self.ball_pos,
                           self.ball_size)

    def ball_move(self):
        if self.ball_pos[0] < 0 or self.ball_pos[0] > (
                self.bg_size[0] - self.ball_size):
            self.ball_speed[0] = -self.ball_speed[0]
        if self.ball_pos[1] < 0 or self.ball_pos[1] > (
                self.bg_size[1] - self.ball_size):
            self.ball_speed[1] = -self.ball_speed[1]
        if (self.ball_pos[1] + self.ball_size) == self.bg_size[1]:
            Game.finish = True
            Game.lose = True

        self.ball_pos[0] += self.ball_speed[0]
        self.ball_pos[1] += self.ball_speed[1]

    def block(self, size):
        x_pos = 0
        y_pos = 0

        # print(size)

        number_of_blocks_in_row = self.bg_size[0] / size

        number_of_blocks = int(
            number_of_blocks_in_row * self.number_of_cols)

        # print(number_of_blocks_in_row, number_of_cols)

        blocks = []

        for block in range(1, number_of_blocks + 1):
            blocks.append([x_pos, y_pos])
            x_pos += size
            if block % number_of_blocks_in_row == 0:
                y_pos += size
                x_pos = 0

        # print(blocks)

        return blocks

    def blocks_logic(self, blocks, size, color):
        delete = False

        for pos in blocks:
            x_pos = pos[0]
            y_pos = pos[1]
            pygame.draw.rect(self.screen, color,
                             (x_pos, y_pos, size, size), 3)

            if (self.ball_pos[1] == y_pos + self.block_size) and (
                    self.ball_pos[0] + self.ball_size / 2) in range(
                x_pos, x_pos + self.block_size):

                if pos in blocks:
                    del blocks[blocks.index(pos)]
                    delete = True

        if self.ball_pos[1] == self.pl_rect[1]:
            if self.ball_pos[0] in range(self.pl_rect[0],
                                         self.pl_rect[0] + self.pl_rect[
                                             2]):
                self.ball_speed[1] = -self.ball_speed[1]

        if delete:
            self.ball_speed[1] = -self.ball_speed[1]

        # if self.ball_pos[1] >= self.pl_rect[1] + self.pl_rect[3]:
        #   c1 = random.randint(100, 255)
        #   c2 = random.randint(100, 255)
        #   c3 = random.randint(100, 255)
        #   self.ball_color = (c1, c2, c3)

        if not blocks:
            Game.finish = True
            Game.win = True


class Menu:

    def __init__(self, bg_size, bg_color):
        self.bg_size = bg_size
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode(self.bg_size)
        self.font_button = pygame.font.SysFont('timesnewroman', 30)
        self.font_result = pygame.font.SysFont('comicsansms', 60)
        self.button_text = "START"
        self.lose_text = "You lose!"
        self.win_text = "You win!"

    def background(self):
        bg = self.screen
        return bg

    def button(self, check):
        color = (255, 255, 255)
        x_pos = self.bg_size[0] / 2 - 50
        y_pos = self.bg_size[1] / 2 - 25
        size = (100, 50)
        pygame.draw.rect(self.screen, color,
                         (x_pos, y_pos, size[0], size[1]))

        if check == "rect":
            return x_pos, y_pos, size
        if check == "text":
            text = self.font_button.render(self.button_text, False,
                                           (0, 0, 0))
            blit = self.screen.blit(text, (x_pos + 5, y_pos + 5))
            return blit

    def result(self):

        if Game.lose:
            text = self.font_result.render(self.lose_text, False,
                                           (255, 0, 0))
            text_width = text.get_width()
            text_height = text.get_height()
            x_pos = (self.bg_size[0] / 2) - (text_width / 2)
            y_pos = (self.bg_size[1] / 2 - 200) - (text_height / 2)

            blit = self.screen.blit(text, (x_pos + 5, y_pos + 5))
            return blit
        elif Game.win:
            text = self.font_result.render(self.win_text, False,
                                           (0, 255, 0))

            text_width = text.get_width()
            text_height = text.get_height()

            x_pos = (self.bg_size[0] / 2) - (text_width / 2)
            y_pos = (self.bg_size[1] / 2 - 200) - (text_height / 2)

            blit = self.screen.blit(text, (x_pos + 5, y_pos + 5))
            return blit

    def click(self):
        clicked = False
        x, y = pygame.mouse.get_pos()
        x_pos, y_pos, size = Menu.button(self, "rect")
        if x in range(int(x_pos), int(x_pos) + size[0]) and y in range(
                int(y_pos), int(y_pos) + size[1]):
            clicked = True
            Game.menu = False
        return clicked
