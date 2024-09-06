from tkinter import *
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 70
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    
    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOR, tag= "Snake")
            self.squares.append(square)


class Food:
    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR,tag="Food")


def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #Updating the Snake's head co-ordinates.
    snake.coordinates.insert(0, (x, y)) 

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        score_label.config(text= f'Score : {score}')

        canvas.delete("Food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    #For continuing the game .
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    
    global direction

    #Avoiding a 180 degree turn XD
    if new_direction == "left":
        if direction != 'right':
            direction = new_direction
    elif new_direction == "right":
        if direction != 'left':
            direction = new_direction
    elif new_direction == "up":
        if direction != 'down':
            direction = new_direction
    elif new_direction == "down":
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:] : 
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2 , canvas.winfo_height()/2, 
    font= ("Ink Free", 70), text= "GAME OVER", fill= "red", tag= "Game Over"
    )

window = Tk()
window.resizable(False, False)
window.title("Snake Game")

score = 0
direction = "down"

score_label = Label(window, text= f'Score : {score}', font=('Consolas',40), bg="black", fg='#34ebdb')
score_label.pack()

canvas = Canvas(window, bg= BACKGROUND_COLOR, width= GAME_WIDTH, height= GAME_HEIGHT)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width / 2) - int(window_width / 2)
y = int(screen_height / 2) - int(window_height / 2)

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.bind("<Left>", lambda event : change_direction('left'))
window.bind("<Right>", lambda event : change_direction('right'))
window.bind("<Up>", lambda event : change_direction('up'))
window.bind("<Down>", lambda event : change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()