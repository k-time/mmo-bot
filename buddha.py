from PIL import ImageGrab
from motions import *
from character import *
import sys

im = None
pixels = None
width, height = 0, 0
failure_count = 0
missing_count = 0
x, y = 0, 0    # Character location on minimap
x2, y2 = 0, 0  # Character location on screen
start_times = [0,0,0,0]
thresholds = [580,465,500,360]   # Speed, att, food, beholder
direction = 'left'

# To handle if another player is in the map
player_in_map = False
spoken = False
occupation_time = 0

# Close game and terminate program
def quit():
    save_image()
    quit_game()
    close_app()
    sys.exit()


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
                KeyPress('b')
                time.sleep(1)
                KeyPress('b')
            elif i == 3:
                b = 0
                time.sleep(1)
                behold()
            start_times[i] = time.time()


# Takes screenshot and updates both character locations
def update_screenshot(state=None):
    global im, pixels, width, height, x, y, failure_count, missing_count, player_in_map, spoken, occupation_time
    im=ImageGrab.grab(bbox=(0,0,1606,1145))
    pixels = im.load()
    width, height = im.size

    x,y = locate_self(36,385,214,215)

    # Make sure game is still open
    if x != -1:
        failure_count = 0
    else:
        failure_count += 1
        print 'Failure count starting'
        print failure_count
        if failure_count > 12:
            print 'App closed unexpectedly! Could not find character on minimap.'
            quit()

    check_death()
    check_potions()

    check_chat()
    if player_in_map:
        elapsed = time.time() - occupation_time
        logger.info(elapsed)
        if elapsed > 90:
            print 'Other player spoke and occupied map for 90 seconds, quitting.'
            quit()


def save_image():
    global im
    im.save('/Users/ktime/Downloads/temp.png')


def check_death():
    global pixels
    rgba = pixels[800,470]
    if rgba[0] == 68 and rgba[1] == 136 and rgba[2] == 187:
        print 'Died...'
        quit()


# Checks if there is white text in the chat
def check_chat():
    global pixels, player_in_map, spoken, occupation_time

    if player_in_map:
        if not others_around(36,385,200,226):
            logger.info('Player has left map')
            player_in_map = False
            spoken = False
        else:
            logger.info('Player is still in map')
    else:
        for i in range(14,26):
            for j in range(1052,1145):
                rgba = pixels[i,j]
                # There is white text
                if rgba[0] == 255 and rgba[1] == 255 and rgba[2] == 255:
                    # Check if there is another player
                    if not spoken and others_around(36,385,200,226):
                        logger.info('Another player has spoken to you, and you have responded')
                        stop()
                        say('sry no pt :)')
                        if direction == 'left':
                            move_left()
                        elif direction == 'right':
                            move_right()
                        player_in_map = True
                        spoken = True
                        occupation_time = time.time()
                        return                


# Locate yellow dot on minimap
def locate_self(x_min, x_max, y_min, y_max):
    global pixels
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i,j]
            # Found yourself
            if rgba[0] == 255 and rgba[1] == 255 and rgba[2] == 136:
               return i,j
    return -1,-1


# Check if another player is in the map
def others_around(x_min, x_max, y_min, y_max):
    global pixels
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            rgba = pixels[i,j]
            # Found yourself
            if rgba[0] == 238 and rgba[1] == 0 and rgba[2] == 0:
               return True
    return False


# Killing monsters on ground level
def first_level():
    global x, y, direction
    start = time.time()
    elapsed = 0

    update_screenshot()

    if x < 190:
        logger.info(x)
        move_right()
        direction = 'right'
        logger.info('moving right')
    else:
        move_left()
        direction = 'left'
        logger.info('moving left')
    
    # Run for 6 hours
    while elapsed < 21600:
        elapsed = time.time() - start
        update_screenshot()
        logger.info(str(x) + ' ' + str(y) + ' ' + direction)

        # If you've reached the left boundary, turn around
        if x < 40 and direction == 'left':
            stop()
            time.sleep(.04)
            turn_right()
            hyper()
            direction = 'right'

            for i in range(1):
                # Attack for a bit
                for j in range(5): att()

                # Check if you're still against the left boundary
                update_screenshot()
                logger.info('Checking if against boundary')
                if x > 43:
                    while x > 43:
                        move_left()
                        update_screenshot()
                    stop()
                    turn_right()

            # Attack for one more period
            for j in range(3): att()

            # Finished, hb and move on
            hyper()
            stance()
            move_right()
            logger.info('Next lap')

        # If you've reached the right boundary, turn around
        elif x > 380 and direction == 'right':
            stop()
            time.sleep(.04)
            turn_left()
            hyper()
            direction = 'left'

            for i in range(1):
                # Attack for a bit
                for j in range(5): att()

                # Check if you're still against the right boundary
                update_screenshot()
                logger.info('Checking if against boundary')
                if x < 377:
                    while x < 377:
                        move_right()
                        update_screenshot()
                    stop()
                    turn_left()

            # Attack for one more period
            for j in range(3): att()

            # Finished, booster and move on
            boost()
            hyper()
            stance()
            move_left()
            logger.info('Next lap')

        # Attack!
        else:
            if x > 90 and direction == 'left' or x < 340 and direction == 'right':
                jump_att()
                time.sleep(.1)
                jump_att()
                time.sleep(.1)
                jump_att()
                #jump_att()
                #time.sleep(.15)
            elif x > 65 and direction == 'left' or x < 360 and direction == 'right':
                jump_att()

    stop()


def main():
    global start_times
    start_times = [time.time(), time.time(), time.time(), time.time()]

    first_level()

    quit_game()
    close_app()
    print 'Exited nicely after 6 hours!'
    

if __name__ == '__main__':
    main()