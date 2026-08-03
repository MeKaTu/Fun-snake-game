import pygame
import random
import os

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 600

CELL = 30

START_SPEED = 4
speed = START_SPEED


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


BLACK = (20, 20, 20)
WHITE = (255, 255, 255)

GREEN = (0, 200, 0)
RED = (220, 40, 40)

GRAY = (70, 70, 70)


title_font = pygame.font.SysFont(
    "arial",
    60
)

font = pygame.font.SysFont(
    "arial",
    30
)

small_font = pygame.font.SysFont(
    "arial",
    20
)



eat_sound = None
gameover_sound = None


if os.path.exists("eat.wav"):
    eat_sound = pygame.mixer.Sound(
        "eat.wav"
    )


if os.path.exists("gameover.wav"):
    gameover_sound = pygame.mixer.Sound(
        "gameover.wav"
    )


def load_image(filename):

    if os.path.exists(filename):

        image = pygame.image.load(
            filename
        )

        image = pygame.transform.scale(
            image,
            (CELL, CELL)
        )

        return image

    return None



snake_head_img = load_image(
    "snake_head.png"
)

snake_body_img = load_image(
    "snake_body.png"
)

apple_img = load_image(
    "apple.png"
)



high_score = 0


if os.path.exists("highscore.txt"):

    with open(
        "highscore.txt",
        "r"
    ) as file:

        try:
            high_score = int(
                file.read()
            )

        except:
            high_score = 0



def draw_text(
        text,
        font_obj,
        color,
        x,
        y
):

    img = font_obj.render(
        text,
        True,
        color
    )

    screen.blit(
        img,
        (x, y)
    )

class Snake:

    def __init__(self):

        self.body = [
            (10, 10),
            (9, 10),
            (8, 10)
        ]

        self.direction = (1, 0)

        self.grow = False


    def move(self):

        head_x = self.body[0][0] + self.direction[0]
        head_y = self.body[0][1] + self.direction[1]

        new_head = (
            head_x,
            head_y
        )

        self.body.insert(
            0,
            new_head
        )


        if self.grow:

            self.grow = False

        else:

            self.body.pop()



    def change_direction(
            self,
            new_direction
    ):

        opposite = (
            -self.direction[0],
            -self.direction[1]
        )

        if new_direction != opposite:

            self.direction = new_direction



    def draw(self):

        for index, part in enumerate(self.body):

            x = part[0] * CELL
            y = part[1] * CELL


            if index == 0 and snake_head_img:

                screen.blit(
                    snake_head_img,
                    (x, y)
                )

            elif snake_body_img:

                screen.blit(
                    snake_body_img,
                    (x, y)
                )

            else:

                pygame.draw.rect(
                    screen,
                    GREEN,
                    (
                        x,
                        y,
                        CELL,
                        CELL
                    )
                )




class Food:


    def __init__(self):

        self.position = self.new_position()



    def new_position(self):

        return (
            random.randint(
                0,
                WIDTH // CELL - 1
            ),

            random.randint(
                0,
                HEIGHT // CELL - 1
            )
        )



    def draw(self):

        x = self.position[0] * CELL
        y = self.position[1] * CELL


        if apple_img:

            screen.blit(
                apple_img,
                (x, y)
            )

        else:

            pygame.draw.rect(
                screen,
                RED,
                (
                    x,
                    y,
                    CELL,
                    CELL
                )
            )




def draw_grid():

    for x in range(
        0,
        WIDTH,
        CELL
    ):

        pygame.draw.line(
            screen,
            GRAY,
            (x, 0),
            (x, HEIGHT)
        )


    for y in range(
        0,
        HEIGHT,
        CELL
    ):

        pygame.draw.line(
            screen,
            GRAY,
            (0, y),
            (WIDTH, y)
        )




def reset_game():

    global score
    global speed


    score = 0

    speed = START_SPEED


    snake.body = [
        (10, 10),
        (9, 10),
        (8, 10)
    ]

    snake.direction = (
        1,
        0
    )

    food.position = food.new_position()

snake = Snake()
food = Food()

score = 0

game_state = "MENU"



running = True


while running:

    clock.tick(speed)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False



        if event.type == pygame.KEYDOWN:


          

            if game_state == "MENU":

                if event.key == pygame.K_SPACE:

                    reset_game()

                    game_state = "PLAYING"



         

            elif game_state == "PLAYING":


                if event.key == pygame.K_UP:

                    snake.change_direction(
                        (0, -1)
                    )


                elif event.key == pygame.K_DOWN:

                    snake.change_direction(
                        (0, 1)
                    )


                elif event.key == pygame.K_LEFT:

                    snake.change_direction(
                        (-1, 0)
                    )


                elif event.key == pygame.K_RIGHT:

                    snake.change_direction(
                        (1, 0)
                    )



            

            elif game_state == "GAMEOVER":


                if event.key == pygame.K_r:

                    reset_game()

                    game_state = "PLAYING"



                elif event.key == pygame.K_ESCAPE:

                    running = False





    if game_state == "MENU":


        screen.fill(BLACK)


        draw_text(
            "SNAKE",
            title_font,
            GREEN,
            200,
            150
        )


        draw_text(
            "SPACE - Basla",
            font,
            WHITE,
            170,
            300
        )


        draw_text(
            "ESC - Cikis",
            font,
            WHITE,
            190,
            350
        )


        pygame.display.update()

        continue



  
    if game_state == "PLAYING":


        snake.move()



        head = snake.body[0]


    

        if (
            head[0] < 0 or
            head[0] >= WIDTH // CELL or
            head[1] < 0 or
            head[1] >= HEIGHT // CELL
        ):

            game_state = "GAMEOVER"



      

        if head in snake.body[1:]:

            game_state = "GAMEOVER"



      
        if head == food.position:


            score += 1

            snake.grow = True


            if eat_sound:

                eat_sound.play()


            food.position = food.new_position()


            speed += 1



   

    screen.fill(BLACK)


    draw_grid()


    if game_state == "PLAYING":

        snake.draw()

        food.draw()


        draw_text(
            f"Score: {score}",
            small_font,
            WHITE,
            10,
            10
        )



    elif game_state == "GAMEOVER":


        draw_text(
            "GAME OVER",
            title_font,
            RED,
            120,
            180
        )


        draw_text(
            f"Score: {score}",
            font,
            WHITE,
            230,
            280
        )


        draw_text(
            "R - Restart",
            font,
            GREEN,
            200,
            350
        )



    pygame.display.update()



pygame.quit()
