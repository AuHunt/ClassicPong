import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
speed = 8
LEFT = False
RIGHT = True
#Ball variables
ball_pos = [300, 200]
ball_vel = [0, 0]
#paddle 1 variables
paddle1_pos = [HALF_PAD_WIDTH, 200]
paddle1_vel = [0, 0]
#paddle 2 variables
paddle2_pos = [(WIDTH - HALF_PAD_WIDTH), 200]
paddle2_vel = [0, 0]
score1 = 0
score2 = 0


def random_direction():
    rand_number = random.randrange(0, 2)
    if bool(rand_number) == False:
        return LEFT
    elif bool(rand_number) == True:
        return RIGHT
    
def speed_up():
    ball_vel[0] = ball_vel[0] * 1.2
    if ball_vel[0] > 20:
        ball_vel[0] = 20    
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == LEFT:
        ball_vel[0] = random.randrange(-6, -2)
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 6)
    ball_vel[1] = random.randrange(-6, 0)    
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    ball_pos[0] = 300
    ball_pos[1] = 200
    spawn_ball(random_direction())

def restart():
    global score1, score2
    score1 = 0
    score2 = 0
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    #Check for wall collision for paddle 1
    if (paddle1_pos[1] <= HEIGHT - (HEIGHT - HALF_PAD_HEIGHT)) or (paddle1_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT) ):
        paddle1_vel[1] = 0
        
    #Check for wall collision for paddle 2    
    if (paddle2_pos[1] <= HEIGHT - (HEIGHT - HALF_PAD_HEIGHT)) or (paddle2_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT) ):
        paddle2_vel[1] = 0
    
    # draw paddles
    #paddle 1
    canvas.draw_line([paddle1_pos[0], (paddle1_pos[1] - 40)],[paddle1_pos[0], (paddle1_pos[1] + 40)] , PAD_WIDTH, "white")
    #paddle 2
    canvas.draw_line([paddle2_pos[0], (paddle2_pos[1] - 40)], [paddle2_pos[0], (paddle2_pos[1] + 40)] , PAD_WIDTH, "white")    
    
    #Bounces off of top and bottom walls
    
    if ((ball_pos[1] - BALL_RADIUS) <= 0) or ((ball_pos[1] + BALL_RADIUS) >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
       
    
    if (paddle1_pos[1] >= 360) or (paddle1_pos[1] <= 40):
        paddle1_vel[1] = 0
    if (paddle2_pos[1] >= 360) or (paddle2_pos[1] <= 40):
        paddle2_vel[1] = 0
        
    #Bounces off of paddles
    if ((ball_pos[0] - BALL_RADIUS) <= 8) and (ball_pos[1] >= (paddle1_pos[1] - 40)) and (ball_pos[1] <= (paddle1_pos[1] + 40)):
        speed_up()
        ball_vel[0] = -ball_vel[0]
        
    elif ((ball_pos[0] + BALL_RADIUS) >= 592) and (ball_pos[1] >= (paddle2_pos[1] - 40)) and (ball_pos[1] <= (paddle2_pos[1] + 40)):
        speed_up()
        ball_vel[0] = -ball_vel[0]
        
    elif ((ball_pos[0] + BALL_RADIUS) >= 592) and ((ball_pos[1] < (paddle2_pos[1] - 40)) or (ball_pos[1] > (paddle2_pos[1] + 40))):
        new_game()
        score1 += 1
        
    elif ((ball_pos[0] - BALL_RADIUS) <= 8) and ((ball_pos[1] < (paddle1_pos[1] - 40)) or (ball_pos[1] > (paddle1_pos[1] + 40))):
        new_game()
        score2 += 1
        
    # draw scores
    
    canvas.draw_text(str(score1), [140, 100], 80, "White")
    canvas.draw_text(str(score2), [440, 100], 80, "White")
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    #paddle 1 controls
    if key == (simplegui.KEY_MAP["w"]) and (paddle1_pos[1] != HALF_PAD_HEIGHT):
        paddle1_vel[1] -= speed
    elif key == (simplegui.KEY_MAP["s"]) and (paddle1_pos[1] != (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_vel[1] += speed
    #paddle 2 controls    
    if key == (simplegui.KEY_MAP["up"]) and (paddle2_pos[1] != HALF_PAD_HEIGHT):
        paddle2_vel[1] -= speed
    elif key == (simplegui.KEY_MAP["down"]) and (paddle2_pos[1] != (HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_vel[1] += speed
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    #paddle 1 controls
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    #paddle 2 controls
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
        


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", restart, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
