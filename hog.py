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
start_times = [0, 0, 0, 0]
thresholds = [160, 465, 500, 40]   # Speed, att, food, boost
direction = 'left'

# Logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
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
            elif i == 3:
                boost()
            start_times[i] = time.time()


# Takes screenshot and updates both character locations
def update_screenshot(state):
    global im, pixels, width, height, x, y, x2, y2, failure_count
    im = ImageGrab.grab(bbox=(0, 0, 1606, 998))
    pixels = im.load()
    width, height = im.size

    x, y = locate_self(29, 224, 167, 337)
    # Make sure game is still open
    if x != -1:
        failure_count = 0
    else:
        failure_count += 1
        logger.info(failure_count)
        if failure_count > 9:
            stop()
            close_app()
            sys.exit()

    if state == 1 or state == 2:
        x2, y2 = locate_character(0, 1606, 798, 871)
    if state == 3:
        x2, y2 = -1, -1
    if state == 4 or state == 5:
        x2, y2 = locate_character(330, 1100, 692, 820)
    if state == 6:
        x2, y2 = locate_character(110, 1100, 680, 910)
    if state == 7:
        x2, y2 = -1, -1

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
                    # Find monster1 or monster2 or monster3
                    if rgba[0] == 153 and rgba[1] == 136 and rgba[2] == 119 \
                            or rgba[0] == 221 and rgba[1] == 102 and rgba[2] == 0:
                        # or rgba[0] == 153 and rgba[1] == 102 and rgba[2] == 51:
                        return True

    elif direction == 'right':
        left_bound = x2+x_min_range
        right_bound = x2+x_max_range
        if left_bound > 0 and right_bound < width:
            for i in range(left_bound, right_bound):
                for j in range(y_min, y_max):
                    rgba = pixels[i, j]
                    # Find monster1 or monster2 or monster3
                    if rgba[0] == 153 and rgba[1] == 136 and rgba[2] == 119 \
                            or rgba[0] == 221 and rgba[1] == 102 and rgba[2] == 0:
                        # or rgba[0] == 153 and rgba[1] == 102 and rgba[2] == 51:
                        return True

    return False


# Killing monsters on ground level
def first_level():
    global x, y, x2, y2, direction
    laps = 0
    move_left()
    direction = 'left'
    
    # Do 2 lengths
    while laps <= 1:
        update_screenshot(1)
        logger.info(str(x) + ' ' + str(y) + ' ' + direction)

        # If you've reached the left boundary, turn around
        if x < 49 and direction == 'left':
            stop()
            turn_right()
            for i in range(3):
                att()
            move_right()
            direction = 'right'
            laps += 1
            logger.info('Done ' + str(laps) + ' laps')

        # If you've reached the right boundary, turn around
        elif x > 195 and direction == 'right':
            stop()
            turn_left()
            for i in range(3):
                att()
            move_left()
            direction = 'left'
            laps += 1
            logger.info('Done ' + str(laps) + ' laps')

        # Attack!
        else:
            # Check that the character was found
            if x2 != -1:
                if monsters_around(40, 400, 779, 792):
                    for i in range(2):
                        att()
    stop()


def climb_ladder():
    global x, y, x2, y2, direction
    on_ladder = False
    stop()

    while not on_ladder:
        update_screenshot(2)
        logger.info(str(x) + str(y))

        # Right of ladder and far away
        if x > 122:
            move_left()
            # update_screenshot updates x, so loop will stop when character is in range
            while x > 122:
                update_screenshot(2)
                logger.info(str(x) + str(y))
            jump()
            climb()

        # Left of ladder and far away
        elif x < 80:
            move_right()
            # update_screenshot updates x, so loop will stop when character is in range
            while x < 80:
                update_screenshot(2)
                logger.info(str(x) + str(y))
            jump()
            climb()

        # Right of ladder and close
        elif 100 < x <= 122:
            logger.info(str(x) + str(y))
            stop()
            move_left()
            time.sleep(.1)
            long_jump()
            climb()

        # Left of ladder and close
        elif 80 <= x <= 100:
            logger.info(str(x) + str(y))
            stop()
            move_right()
            time.sleep(.1)
            long_jump()
            climb()

        stop()
        climb()
        time.sleep(1)
        update_screenshot(2)

        if y < 277:
            on_ladder = True
            time.sleep(1.5)
        else:
            move_left()
            time.sleep(.15)

        stop()


def cross_platforms():
    global y
    stop()
    move_left()
    time.sleep(.6)
    for i in range(18):
        long_jump()
    stop()
    time.sleep(.5)
    jump()
    climb()
    time.sleep(.5)
    update_screenshot(3)
    logger.info(str(x) + str(y))

    # Successfully climbed ladder
    if y < 248:
        move_right()
        time.sleep(1.5)
        stop_climb()
        return True
    # On platform, but didn't climb ladder
    elif 258 <= y < 273:
        for i in range(10):
            jump()
            time.sleep(.1)
            move_left(.2)
            time.sleep(1)
            update_screenshot(3)
            logger.info(str(x) + str(y))
            # On ladder
            if y < 248:
                move_right()
                time.sleep(1.5)
                stop_climb()
                return True
            # Fell to ground
            elif y > 273:
                return False
        return False
    # On ground
    else:
        return False


def second_level():
    global x, y, x2, y2, direction
    stop()
    turn_right()
    direction = 'right'
    had_monsters = True
    attack_count = 0
    count = 0

    # If 2 screenshots in a row don't have monsters, you're done
    while count < 2:
        update_screenshot(4)
        logger.info(str(x) + str(y))
        logger.info(str(x2) + str(y2))

        # Failure if you fall off platform
        if y > 245:
            return False

        # Cap the number of attacks so you don't get stuck in a loop
        if attack_count > 9:
            stop()
            return True

        # Too far left, so move over
        elif x < 76:
            move_right(.8)
            direction = 'right'

        # Too far right, so move over
        elif x > 111:
            move_left(.8)
            direction = 'left'

        # If character tag is blocked, you can't find monsters
        elif x2 == -1:
            logger.info('Cannot find character')
            if had_monsters:
                for i in range(2):
                    att()
            move_left(.1)

        # If there are monsters in front
        elif monsters_around(0, 300, 658, 688):
            logger.info('Found monsters ahead')
            had_monsters = True
            attack_count += 1
            # Reset the count
            count = 0
            if direction == 'right':
                for i in range(3):
                    att()
                move_right(.2)
            else:
                for i in range(3):
                    att()
                move_left(.2)

        # If there are monsters behind
        elif monsters_around(-300, 0, 658, 688):
            logger.info('Found monsters behind')
            had_monsters = True
            attack_count += 1
            count = 0
            if direction == 'right':
                turn_left()
                direction = 'left'
                for i in range(3):
                    att()
                move_left(.2)
            else:
                turn_right()
                direction = 'right'
                for i in range(3):
                    att()
                move_right(.2)

        # If there are no monsters
        else:
            had_monsters = False
            count += 1
            logger.info('No monsters ' + str(count) + ' time(s)')

    stop()
    return True


def climb_ladder_2():
    global x, y, x2, y2, direction
    on_ladder = False
    stop()

    while not on_ladder:
        update_screenshot(5)
        logger.info(str(x) + str(y))

        # Failure if you fall off platform
        if y > 245:
            return False       

        # Right of ladder and far away
        if x > 114:
            move_left()
            # update_screenshot updates x, so loop will stop when character is in range
            while x > 114:
                update_screenshot(5)
                logger.info(str(x) + str(y))
            jump()
            climb()

        # Left of ladder and far away
        elif x < 74:
            move_right()
            # update_screenshot updates x, so loop will stop when character is in range
            while x < 74:
                update_screenshot(5)
                logger.info(str(x) + str(y))
            jump()
            climb()

        # Right of ladder and close
        elif 94 < x <= 114:
            logger.info(str(x) + str(y))
            stop()
            move_left()
            time.sleep(.1)
            long_jump()
            climb()

        # Left of ladder and close
        elif 74 <= x <= 94:
            logger.info(str(x) + str(y))
            stop()
            move_right()
            time.sleep(.1)
            long_jump()
            climb()

        stop()
        climb()
        time.sleep(1)
        update_screenshot(5)

        if y < 217:
            on_ladder = True
            time.sleep(1.5)
        else:
            move_left()
            time.sleep(.1)
        stop()
    return True


def third_level():
    global x, y, x2, y2, direction
    stop()
    turn_right()
    direction = 'right'

    had_monsters = True
    attack_count = 0
    count = 0

    # If 3 screenshots in a row don't have monsters, you're done
    while count < 3:
        update_screenshot(6)
        logger.info(str(x) + str(y))
        logger.info(str(x2) + str(y2))

        # Failure if you fall off platform
        if y > 203:
            return False

        # Cap the number of attacks so you don't get stuck in a loop
        if attack_count > 9:
            stop()
            return True

        # Too far left, so move over
        elif x < 70:
            move_right(1.1)
            direction = 'right'

        # Too far right, so move over
        elif x > 127:
            move_left(1.1)
            direction = 'left'

        # If character tag is blocked, you can't find monsters
        elif x2 == -1:
            logger.info('Cannot find character')
            if had_monsters:
                for i in range(2):
                    att()
            move_left(.1)

        # If there are monsters in front
        elif monsters_around(0, 300, 646, 820):
            logger.info('Found monsters ahead')
            had_monsters = True
            attack_count += 1
            # Reset the count
            count = 0
            if direction == 'right':
                for i in range(3):
                    att()
                move_right(.2)
            else:
                for i in range(3):
                    att()
                move_left(.2)

        # If there are monsters behind
        elif monsters_around(-300, 0, 646, 820):
            logger.info('Found monsters behind')
            had_monsters = True
            attack_count += 1
            count = 0
            if direction == 'right':
                turn_left()
                direction = 'left'
                for i in range(3):
                    att()
                move_left(.2)
            else:
                turn_right()
                direction = 'right'
                for i in range(3):
                    att()
                move_right(.2)

        # If there are no monsters
        else:
            had_monsters = False
            count += 1
            logger.info('No monsters ' + str(count) + ' time(s)')

    stop()
    return True


def drop_down():
    global x, y, x2, y2, direction
    stop()
    move_right()
    while x < 200 and y < 275:
        update_screenshot(7)
    stop()
    turn_left()
    direction = 'left'
    for i in range(4):
        att()


def main():
    global start_times
    start_times = [time.time(), time.time(), time.time(), time.time()]
    start = time.time()
    elapsed = 0

    while elapsed < 18000:
        first_level()
        # Tries to climb to next level 4 times
        success = False
        count = 0
        while not success and count < 4:
            climb_ladder()
            success = cross_platforms()
            if success:
                success = second_level()
            count += 1
        # If you've killed monsters on the second level
        if success:
            success = climb_ladder_2()
            if success:
                success = third_level()
                if success:
                    drop_down()

        elapsed = time.time() - start

    quit_game()
    close_app()
    logger.info('Exited nicely after 5 hours!')
    

if __name__ == '__main__':
    main()
