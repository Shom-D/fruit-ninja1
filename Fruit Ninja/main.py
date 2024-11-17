import pgzrun
import random
import time

WIDTH, HEIGHT = 800, 600
TITLE =  "Fruit Ninja"
current_level = 1
final_level = 8
isGameOver = False
isGameComplete = False
Centre = (WIDTH/2, HEIGHT/2)
ITEM = ["bomb", "chair"]
items = []
animations = []
start_time = time.time()
start_speed = 10


def define_items(level):
    items_to_create = choose_items(level)
    new_actors = createActors(items_to_create)    
    final_actors = layout_actors(new_actors)
    animate_items(final_actors)
    return final_actors

def choose_items(level):
    items_to_create =["banana"]
    for x in range(level):
        items_to_create.append(random.choice(ITEM))
    return items_to_create

def createActors(items_to_create):
    actor_list = []
    for x in items_to_create:
        x+="img"
        actor_list.append(Actor(x))
    return actor_list

def layout_actors(actor_list):
    num_gaps= len(actor_list)+1
    gap_size = WIDTH/num_gaps
    random.shuffle(actor_list)
    for i, item in enumerate(actor_list):
        item.x = (i+1)*gap_size
        item.y = 0
    return actor_list

def animate_items(actor_list):
    global animations, start_speed
    for item in actor_list:
        duration = start_speed - current_level
        item.anchor = ("center", "bottom")
        animation = animate(item, duration = duration, on_finished= gameOver, y = HEIGHT)
        animations.append(animation)

def stop_animations(animations):
    for x in animations:
        if x.running:
            x.stop()

def displayMessage(msg1, msg2):
    screen.draw.text(msg1, color = (255,255,255), center= Centre, fontsize= 50) #experiment using fontname as a property fonts/filename.ttf
    screen.draw.text(msg2, color = (255,255,255), center = (Centre[0], Centre[1]+100), fontsize = 25)

def update():
    global items
    if len(items)==0:
        items = define_items(current_level)

def handle_game_complete():
    global current_level, items, animations, isGameComplete
    stop_animations(animations)
    if current_level == final_level:
        isGameComplete=True
    else:
        current_level+=1
        items= []
        animations = []
    
def gameOver():
    global isGameOver
    isGameOver = True

def on_mouse_down(pos):
    global items,current_level
    for item in items:
        if item.collidepoint(pos):
            if "banana" in item.image:
                handle_game_complete()
            else:
                gameOver()

            
                

def draw():
    global current_level, isGameOver, isGameComplete, items, start_time,current_time
    screen.clear()
    screen.blit("backgroundimg", (0,0))
    if isGameOver:
        displayMessage("Game Over", f"You got to level {current_level} and survived for {int(current_time-start_time)} seconds")
    elif isGameComplete:
        displayMessage("You win!", f"You beat the game in {int(time.time()-start_time)} seconds")
    else:
        for item in items:
            item.draw()
        current_time= time.time()

pgzrun.go()