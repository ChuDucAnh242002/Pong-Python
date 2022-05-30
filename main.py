"""
"""

import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS =  60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BORDER_WIDTH, BORDER_HEIGHT = 10, 25
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 3

PADDLE_BLUE_IMAGE = pygame.image.load(os.path.join('asset', 'paddleBlue.png'))
PADDLE_BLUE_IMAGE = pygame.transform.rotate(PADDLE_BLUE_IMAGE, 90)
PADDLE_BLUE_IMAGE = pygame.transform.scale(PADDLE_BLUE_IMAGE, (PADDLE_WIDTH, PADDLE_HEIGHT))

PADDLE_RED_IMAGE = pygame.image.load(os.path.join('asset', 'paddleRed.png'))
PADDLE_RED_IMAGE = pygame.transform.rotate(PADDLE_RED_IMAGE, 90)
PADDLE_RED_IMAGE = pygame.transform.scale(PADDLE_RED_IMAGE, (PADDLE_WIDTH, PADDLE_HEIGHT))

BALL_BLUE_IMAGE = pygame.image.load(os.path.join('asset', 'ballBlue.png'))
BALL_BLUE_IMAGE = pygame.transform.scale(BALL_BLUE_IMAGE, (BALL_RADIUS*2, BALL_RADIUS*2))

BG_IMAGE = pygame.image.load(os.path.join('asset', 'background.png'))
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

class Paddle:
    """
        2 Paddle, one on the blue, one on the red
    """
    COLOR  = WHITE
    VEL = 4

    def __init__(self, x, y, width, height, image):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.image= image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def move(self, up= True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius, image):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball, blue_score, red_score):
    win.blit(BG_IMAGE, (0, 0))

    blue_score_text = SCORE_FONT.render(f"{blue_score}", 1, WHITE)
    red_score_text = SCORE_FONT.render(f"{red_score}", 1, WHITE)
    win.blit(blue_score_text, (WIDTH//4 - blue_score_text.get_width() // 2, 20))
    win.blit(red_score_text, (WIDTH * 3 //4 - red_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)
    pygame.display.update()

def handle_paddle_movement(keys, blue_paddle, red_paddle):
    if keys[pygame.K_w] and blue_paddle.y - blue_paddle.VEL >= 0:
        blue_paddle.move(up = True)
    if keys[pygame.K_s] and blue_paddle.y + blue_paddle.VEL + blue_paddle.height <= HEIGHT:
        blue_paddle.move(up = False)

    if keys[pygame.K_UP] and red_paddle.y - red_paddle.VEL >= 0:
        red_paddle.move(up = True)
    if keys[pygame.K_DOWN] and red_paddle.y + red_paddle.VEL + red_paddle.height <= HEIGHT :
        red_paddle.move(up = False)

def handle_collision(ball, blue_paddle, red_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= blue_paddle.y and ball.y <= blue_paddle.y + blue_paddle.height:
            if ball.x - ball.radius <= blue_paddle.x + blue_paddle.width:
                ball.x_vel *= -1

                middle_y = blue_paddle.y + blue_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (blue_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= red_paddle.y and ball.y <= red_paddle.y + red_paddle.height:
            if ball.x + ball.radius >= red_paddle.x:
                ball.x_vel *= -1

                middle_y = red_paddle.y + red_paddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (red_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def main():

    run = True
    clock = pygame.time.Clock()

    blue_paddle = Paddle(40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_BLUE_IMAGE)
    red_paddle = Paddle(WIDTH - 40 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_RED_IMAGE)
    paddles = [blue_paddle, red_paddle]

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_BLUE_IMAGE)

    blue_score = 0
    red_score = 0

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, blue_paddle, red_paddle)

        ball.move()
        handle_collision(ball, blue_paddle, red_paddle)

        if ball.x < 0:
            red_score += 1
            ball.reset()
        
        elif ball.x > WIDTH:
            blue_score += 1
            ball.reset()
        draw(WIN, paddles, ball, blue_score, red_score)
            
        won = False
        if blue_score >= WINNING_SCORE:
            won = True
            win_text = "Blue Player Won!"

        if red_score >= WINNING_SCORE:
            won = True
            win_text = "Red Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()// 2, HEIGHT//2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            ball.reset()
            blue_paddle.reset()
            red_paddle.reset()
            blue_score = 0
            red_score = 0

if __name__ == "__main__":
    while True:
        main()
