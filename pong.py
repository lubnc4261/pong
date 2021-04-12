
# Imports

import pygame
pygame.init()

# Necessary

RESOLUTION = (800, 600)
FPS = 60
UP, DOWN = "UP", "DOWN"

# Colors

BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255,255,0)

# pause menu


def pause():

    timer = pygame.time.Clock()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_SPACE:
                    #screen.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        # screen.fill((0, 0, 0))
        timer.tick(60)

# Ball Class

class Ball(pygame.sprite.Sprite):
    def __init__(self, field_rect, color):
        pygame.sprite.Sprite.__init__(self)
        self.field_rect = field_rect
        self.image = pygame.Surface((15, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.field_rect.center
        self.x_speed = 5
        self.y_speed = 3

    # is_out_left

    @property
    def is_out_left(self):
        return self.rect.left <= self.field_rect.left

    # is_out_right

    @property
    def is_out_right(self):
        return self.rect.right >= self.field_rect.right

    # is_within_sidelines

    @property
    def is_within_sidelines(self):
        return (
            self.rect.top > self.field_rect.top
            and self.rect.bottom < self.field_rect.bottom
            )

    # move

    def move(self):
        self.rect = self.rect.move(self.x_speed, self.y_speed)

    # update if outside

    def update(self):
        if not self.is_within_sidelines:
            self.y_speed = -self.y_speed

    # reset

    def reset(self):
        self.rect.center = self.field_rect.center

# Paddle class


class Paddle(pygame.sprite.Sprite):
    def __init__(self, field_rect, margin, color):
        pygame.sprite.Sprite.__init__(self)
        self.field_rect = field_rect
        self.image = pygame.Surface((15, 150))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 0
        self.max_speed = 10
        self.rect.centery = self.field_rect.centery
        if margin < 0:
            self.rect.right = self.field_rect.right + margin
        else:
            self.rect.left = self.field_rect.left + margin

    def set_direction(self, direction):
        if direction == UP:
            self.speed = -self.max_speed
        elif direction == DOWN:
            self.speed = self.max_speed
        elif direction == None:
            self.speed = 0

    def move(self):
        self.rect.y += self.speed
        self.rect = self.rect.clamp(self.field_rect)

    update = move

# ScoreBoard Class

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, field_rect, side_margin, top_margin=20):
        self.field_rect = field_rect
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.label = self.font.render(str(self.score), 1, WHITE)
        self.rect = self.label.get_rect()
        self.rect.top = self.field_rect.top + top_margin
        if side_margin < 0:
            self.rect.right = self.field_rect.right + side_margin
        else:
            self.rect.left = self.field_rect.left + side_margin

    def increase_score(self, step=1):
        self.score += step
        #pygame.mixer.music.load('assets/sounds/score_up.mp3')
        #pygame.mixer.music.play(0)
        #pygame.mixer.music.set_volume(.5)

    def update(self):
        """ Event on score """
        self.label = self.font.render(str(self.score), 1, YELLOW)           
            
            
def main():
    """ Creator of everything """
    #pygame.init()

    # Title

    pygame.display.set_caption("Pong")


    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode(RESOLUTION)
    timer = pygame.time.Clock()
    ball = Ball(screen.get_rect(), GREEN)
    paddles = [
        Paddle(screen.get_rect(), 10, RED), Paddle(screen.get_rect(), -10, BLUE)
        ]
    scores = [
        ScoreBoard(screen.get_rect(), 40), ScoreBoard(screen.get_rect(), -40)
        ]
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE)
            ):
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddles[0].set_direction(UP)
                elif event.key == pygame.K_s:
                    paddles[0].set_direction(DOWN)
                elif event.key == pygame.K_UP:
                    paddles[1].set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    paddles[1].set_direction(DOWN)
                elif event.key == pygame.K_SPACE:
                    pause()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddles[0].set_direction(None)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddles[1].set_direction(None)

        if ball.rect.collidelist([p.rect for p in paddles]) != -1:
            ball.x_speed = -ball.x_speed
        
        if ball.is_out_left:
            scores[1].increase_score()
            scores[1].update()
            ball.reset()
        if ball.is_out_right:
            scores[0].increase_score()
            scores[0].update()
            ball.reset()

        ball.move()
        ball.update()

        for paddle in paddles:
            paddle.update()

        screen.blit(ball.image, ball.rect)
        for paddle in paddles:
            screen.blit(paddle.image, paddle.rect)
        for score in scores:
            screen.blit(score.label, score.rect)

        pygame.display.update()
        timer.tick(FPS)


if __name__ == "__main__":
    main()
