from PIL import ImageGrab
from motions import *
import sys

im = None
pixels = None
width, height = 0, 0
failure_count = 0
missing_count = 0
x, y = 0, 0    # Character location on minimap
x2, y2 = 0, 0  # Character location on screen
start_times = [0,0,0]
thresholds = [580,465,500]   # Speed, att, food
direction = 'left'
debug = False

def check_potions():
    global start_times, thresholds
    for i in range(len(start_times)):
        elapsed = time.time() - start_times[i]
        if elapsed > thresholds[i]:
            if i == 0:
                speed_pot()
            elif i == 1:
                att_pot()
            elif i == 2:
                feed()
            start_times[i] = time.time()


# Takes screenshot and updates both character locations
def update_screenshot(state=None):
    global im, pixels, width, height, x, y, x2, y2, failure_count, missing_count
    im=ImageGrab.grab(bbox=(0,0,1606,870))
    pixels = im.load()
    width, height = im.size

    x,y = locate_self(21,433,190,210)
    x2,y2 = locate_character(0,1606,625,870)

    # Make sure game is still open
    if x != -1:
        failure_count = 0
    else:
        failure_count += 1
        if failure_count > 9:
            stop()
            close_app()
            print 'App closed unexpectedly! Could not find character on minimap.'
            sys.exit()

    if x2 != -1:
         missing_count = 0
    else:
        missing_count += 1
        if missing_count > 19:
            stop()
            close_app()
            print 'App closed unexpectedly! Could not find character on screen.'
            sys.exit()
                   
    check_potions()


# Locate yellow dot on minimap
def locate_self(x_min, x_max, y_min, y_max):
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i,j]
            # Found yourself
            if rgba[0] == 255 and rgba[1] == 255 and rgba[2] == 136:
               return i,j
    return -1,-1


# Locate actual character on screen
def locate_character(x_min, x_max, y_min, y_max):
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i,j]
            # Found character name tag
            if rgba[0] == 0 and rgba[1] == 136 and rgba[2] == 204:
                # Adjust to center of name, and at the character's mouth
                return i+48,j+25
    return -1,-1


# Locate monsters around you
def monsters_around(x_min_range, x_max_range, y_min, y_max):
    global x2, direction

    if direction == 'left':
        left_bound = x2-x_max_range
        right_bound = x2-x_min_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba=pixels[i,j]
                    # Find monster1 or monster2
                    if rgba[0] == 153 and rgba[1] == 17 and rgba[2] == 255 \
                    or rgba[0] == 102 and rgba[1] == 34 and rgba[2] == 170 \
                    or rgba[0] == 255 and rgba[1] == 34 and rgba[2] == 255:
                        return True

    elif direction == 'right':
        left_bound = x2+x_min_range
        right_bound = x2+x_max_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba=pixels[i,j]
                    # Find monster1 or monster2
                    if rgba[0] == 153 and rgba[1] == 17 and rgba[2] == 255 \
                    or rgba[0] == 102 and rgba[1] == 34 and rgba[2] == 170 \
                    or rgba[0] == 255 and rgba[1] == 34 and rgba[2] == 255:
                        return True

    return False


# Killing monsters on ground level
def first_level():
    global x, y, x2, y2, direction, debug
    start = time.time()
    elapsed = 0

    move_right()
    direction = 'right'
    
    # Run for 5 hours
    while elapsed < 21600:
        elapsed = time.time() - start
        update_screenshot()
        if debug: print x, y, direction

        # If you've reached the left boundary, turn around
        if x < 45 and direction == 'left':
            stop()
            time.sleep(.05)
            turn_right()
            time.sleep(.6)
            direction = 'right'
            for i in range(5): att()

            # Check if there are still monsters
            update_screenshot()
            if debug: print x, y, direction
            attack_count = 0
            while attack_count < 3 and monsters_around(20,150,620,785):
                print 'Still see monsters'
                for i in range(3): att()
                attack_count += 1
                update_screenshot()

            # Finished, booster and move on
            boost()
            move_right()
            if debug: print 'Next lap'

        # If you've reached the right boundary, turn around
        elif x > 400 and direction == 'right':
            stop()
            time.sleep(.05)
            turn_left()
            time.sleep(.6)
            direction = 'left'
            for i in range(5): att()

            # Check if there are still monsters
            update_screenshot()
            if debug: print x, y, direction
            attack_count = 0
            while attack_count < 3 and monsters_around(20,150,620,785):
                print 'Still see monsters'
                for i in range(3): att()
                attack_count += 1
                update_screenshot()

            # Finished, booster and move on
            boost()
            move_left()
            if debug: print 'Next lap'

        # Attack!
        else:
            # Check that the character was found
            if x2 != -1:
                if monsters_around(110,500,660,773):
                    if random.random() > .08:
                        jump_att()
                        if random.random() < .15: att()
                    else:
                        jump_att2()
                        if random.random() < .15: att()

            else:
                print 'Character not found on screen'
    stop()


def main():
    global start_times
    start_times = [time.time(), time.time(), time.time()]

    first_level()

    quit_game()
    close_app()
    print 'Exited nicely after 6 hours!'
    

if __name__ == '__main__':
    main()