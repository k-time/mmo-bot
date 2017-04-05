from PIL import ImageGrab
from motions import *
import logging
import sys

"""
I should have created a character class instead of using these global variables,
as well as modularized the code more. I was trying to create a working bot quickly
and didn't take enough time initially to think about code structure. If I were still 
developing this bot, I would restructure the code with better object-oriented design, 
but I don't use the bot anymore. That being said, the bot performs very well.
"""

im = None
pixels = None
width, height = 0, 0
failure_count = 0
x, y = 0, 0    # Character location on minimap
x2, y2 = 0, 0  # Character location on screen
last_x = 0
start_times = [0, 0, 0]
thresholds = [580, 465, 500]   # Speed, att, food
direction = 'left'

# Logger
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logger = logging.getLogger('BOT')


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
def update_screenshot():
    global im, pixels, width, height, x, y, x2, y2, failure_count, last_x
    im = ImageGrab.grab(bbox=(0, 0, 1606, 1008))
    pixels = im.load()
    width, height = im.size
    x, y = locate_self(22, 329, 199, 219)
    x2, y2 = locate_character(0, 1606, 958, 992)

    # Make sure game is still open
    if x != -1 and x != last_x:
        failure_count = 0
    else:
        failure_count += 1
        logger.info(failure_count)
        if failure_count > 25:
            stop()
            close_app()
            logger.info('App closed unexpectedly! Could not find character on minimap.')
            sys.exit()

    last_x = x
    check_potions()


# Locate yellow dot on minimap
def locate_self(x_min, x_max, y_min, y_max):
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i, j]
            # Found yourself
            if rgba[0] == 255 and rgba[1] == 255 and rgba[2] == 136:
                return i, j
    return -1, -1


# Locate actual character on screen
def locate_character(x_min, x_max, y_min, y_max):
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i, j]
            # Found character name tag
            if rgba[0] == 0 and rgba[1] == 136 and rgba[2] == 204:
                # Adjust to center of name, and at the character's mouth
                return i+48, j+25
    return -1, -1


# Locate monsters around you
def monsters_around(x_min_range, x_max_range, y_min, y_max):
    global x2, direction
    if direction == 'left':
        left_bound = x2-x_max_range
        right_bound = x2-x_min_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba = pixels[i, j]
                    # Find monster1 or monster2
                    if rgba[0] == 68 and rgba[1] == 119 and rgba[2] == 170 \
                            or rgba[0] == 0 and rgba[1] == 204 and rgba[2] == 85:
                        return True

    elif direction == 'right':
        left_bound = x2+x_min_range
        right_bound = x2+x_max_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba = pixels[i, j]
                    # Find monster1 or monster2
                    if rgba[0] == 68 and rgba[1] == 119 and rgba[2] == 170 \
                            or rgba[0] == 0 and rgba[1] == 204 and rgba[2] == 85:
                        return True
    return False


# Killing monsters on ground level
def first_level():
    global x, y, x2, y2, direction
    start = time.time()
    elapsed = 0
    move_right()
    direction = 'right'
    
    # Run for 6 hours
    while elapsed < 21600:
        elapsed = time.time() - start
        update_screenshot()
        logger.info(str(x) + ' ' + str(y) + ' ' + direction)

        # If you've reached the left boundary, turn around
        if x < 76 and direction == 'left':
            stop()
            att()
            time.sleep(.04)
            turn_right()
            time.sleep(.2)
            move_right(.3)
            direction = 'right'
            for i in range(1):
                att()

            # Removed due to increase in in-game skill level
            """
            for i in range(1):
                update_screenshot()
                if monsters_around(110,480,938,950):
                    move_right(.1)
                    for i in range(3): att()
                elif monsters_around(-300,-110,938,950):
                    logger.info('monsters behind'
                    turn_left()
                    for i in range(3): att()
            """

            """
            # Check if there are still monsters
            update_screenshot()
            logger.info(str(x) + ' ' + str(y) + ' ' + direction)
            attack_count = 0
            while attack_count < 3 and monsters_around(20,150,620,785):
                logger.info('Still see monsters'
                for i in range(3): att()
                attack_count += 1
                update_screenshot()
            """

            # Finished, hyper and move on
            move_right()
            jump()
            hyper()
            logger.info('Next lap')

        # If you've reached the right boundary, turn around
        elif x > 266 and direction == 'right':
            stop()
            att()
            time.sleep(.04)
            turn_left()
            time.sleep(.2)
            move_left(1.6)
            direction = 'left'
            for i in range(1):
                att()

            # Removed due to increase in in-game skill level
            """
            for i in range(1):
                update_screenshot()
                if monsters_around(110,450,938,950):
                    move_left(.1)
                    for i in range(4): att()
                elif monsters_around(-300,-110,938,950):
                    logger.info('monsters behind'
                    turn_right()
                    for i in range(4): att()
            """

            """
            # Check if there are still monsters
            update_screenshot()
            logger.info(str(x) + ' ' + str(y) + ' ' + direction)
            attack_count = 0
            while attack_count < 3 and monsters_around(20,150,620,785):
                logger.info('Still see monsters'
                for i in range(3): att()
                attack_count += 1
                update_screenshot()
            """

            # Finished, buff and move on
            boost()
            hyper()
            move_left()
            logger.info('Next lap')

        # Attack!
        else:
            # Check that the character was found
            if x2 != -1:
                if monsters_around(40, 520, 938, 950):
                    if 208 < x < 234:
                        jump_att()
                    else:
                        jump_att()
                        jump_att()

            else:
                logger.info('Character not found on screen')
    stop()


def main():
    global start_times
    start_times = [time.time(), time.time(), time.time()]
    first_level()
    quit_game()
    close_app()
    logger.info('Exited nicely after 6 hours!')
    

if __name__ == '__main__':
    main()
