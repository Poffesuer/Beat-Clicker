"""
Harry Kwok
Beat Clicker
"""

import pygame, random

# Import all pygame functions
from pygame.locals import *

# Set the width and height of the screen [width, height]
WIDTH = 1000 
HEIGHT = 700

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Beat Clicker")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load music and play it
def song_play(directory, loop=1, start_time=0.0):
    pygame.mixer.music.load(directory)
    pygame.mixer.music.play(loop, start_time)

# Create font
def create_font(font_type, size, text, COLOR, alpha=255):
    font = pygame.font.Font(font_type, size) 
    display_font = font.render(text, True, COLOR)
    display_font.set_alpha(alpha)
    return display_font

# Creates the glow surface for the particle
def particle_outline(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

# Change/set brightness
def brightness_change(intensity):
    shade = pygame.Surface((WIDTH, HEIGHT))
    shade.set_alpha(intensity)
    shade.fill(BLACK)
    screen.blit(shade, (0,0))

# Removes all target attributes
def remove_target(num):
    targets.pop(num)
    target_time.pop(num)
    window.pop(num)
    indicator.pop(num)
    target_alpha.pop(num)
    target_number.pop(num)

# Load sound effects
target_hit = pygame.mixer.Sound("Sound effects/target_hit.mp3")
target_hit.set_volume(0.5)
level_select = pygame.mixer.Sound("Sound effects/level select.mp3")

# Load backgrounds
title_background = pygame.image.load("Assets/Background/Title screen.png").convert_alpha()
background_1 = pygame.image.load("Assets/Background/Hikaru nara.jpeg").convert_alpha()
background_2 = pygame.image.load("Assets/Background/The Whole Rest.png").convert_alpha()

# Load Buttons
selection_button_norm = pygame.image.load("Assets/Buttons/Back to selection screen.png").convert_alpha()
continue_button_norm = pygame.image.load("Assets/Buttons/Continue.png").convert_alpha()
retry_button_norm = pygame.image.load("Assets/Buttons/Retry.png").convert_alpha()

# Load larger buttons
selection_button_big = pygame.image.load("Assets/Buttons/Back to selection screen big.png").convert_alpha()
continue_button_big = pygame.image.load("Assets/Buttons/Continue big.png").convert_alpha()
retry_button_big = pygame.image.load("Assets/Buttons/Retry big.png").convert_alpha()

# Load selection bars
song_1_bar = pygame.image.load("Assets/Song_bar/song_1_bar.png").convert_alpha()
song_2_bar = pygame.image.load("Assets/Song_bar/song_2_bar.png").convert_alpha()

# Define some colors
PURPLE = (20, 20, 60)
BLUE = (41, 89, 186)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (28, 201, 46)
YELLOW = (219, 188, 15)

# Attributes of particles for cursor = location, size
particles = []

# Keeps track of highest score player gets = (high_score, rank)
leaderboard = [[0, "F"], [0, "F"]]

# Stores the time for each target to determine the window in which the target can be pressed
window = []

# Stores each targets colour which is used to change when window for pressing is open
indicator = []

# Attrubutes of target
targets = [] # Stores bounding boxes of each target
target_alpha = [] # Stores opacity of each target
target_time = [] # Stores the time for each target to determine when the target will disappear (total target time)
target_number = [] # Stores the numbers that appear on target to ensure that player knows what target appeared first
target_height = 100
target_width = 100

# Store index of corresponding for name of accuracy on timing of beats
perfect = 0
early = 1
late = 2
miss = 3

# Stores all backgrounds in game
back = [title_background, background_1, background_2]

# Define song 1's basic attributes
song_1 = "Music/Hikaru Nara.mp3" # Directory of song
duration_1 = 88 # Length of song
intro_1 = 14 # Length of song introduction

# Define song 1's basic attributes
song_2 = "Music/The Whole Rest.mp3" # Directory of song
duration_2 = 140 # Length of song
intro_2 = 16 # Length of song introduction

# Used to determine which song and its attributes are chosen
select = 1

# Time of beginning of song when selected
start_time = 0

# Time of spawning
spawning_time = 0

# Game states
title_screen = True
selection_screen = False
in_menu = False
in_game = False
evaluation_screen = False
reset = True

# Declares if title screen is transitioning
title_transition = False

# Keep track of when mouse is clicked
click_down = False
click_up = False
click = False

#"Font/Amatic-Bold.ttf" "Font/Electrolize.ttf" "Font/dogicabold.ttf"
game_font = "Font/Electrolize.ttf"

# y values of selection screen rectangles
song_1_y = 315
song_2_y = 395

# list of y values of rectangles(songs) in selection screen
song_y = [song_1_y, song_2_y]

# Make dimensions of big button
continue_rect_big = pygame.Rect((WIDTH/2) - 342/2, 175-2.5, 342, 80)
retry_rect_big = pygame.Rect((WIDTH/2) - 342/2, 320-2.5, 342, 80)
selection_rect_big = pygame.Rect((WIDTH/2) - 342/2, 475-2.5, 342, 80)

# Play title song
title_song = "Music/Title Screen.mp3"
song_play(title_song, -1)

# Make mouse invisible
pygame.mouse.set_visible(0)

done = False

# Main Game Loop
while not done:
    
    current_time = pygame.time.get_ticks()/1000

    click = False

    mouse_X, mouse_Y = pygame.mouse.get_pos()
    sword = pygame.Rect(mouse_X, mouse_Y, 1, 1)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            
            # Sets game state to menu
            if event.key == pygame.K_m and in_game:
                in_menu = not in_menu
                
                # Resumes game
                if in_menu == False:
                    new_time += add_timey # Updates clock
                    pygame.mixer.music.unpause() # Resume song

                # Triggers beginning of calculation for time in menu
                else:
                    menu_start = True 

            shift_value = 0 # Ensure that the selection screen rectanges not move when not pressing down or up buttons

            # Changes values of movement for the selection screen rectangles for different key inputs and sets new select value
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and selection_screen:
                shift_value = -80
                if select < 2:
                    start_preview = False  # Reactivate loading song code when selection screen rectangle changes
                    select += 1
            elif (event.key == pygame.K_w or event.key == pygame.K_UP) and selection_screen:
                shift_value = 80
                if select > 1:
                    start_preview = False  # Reactivate loading song code when selection screen rectangle changes
                    select -= 1
            
            # Changes to game state
            elif (event.key == pygame.K_RETURN) and selection_screen:
                level_select.play()
                selection_screen = False
                in_game = True

            if selection_screen:
                
                # Changes y value of selection screen rectangles
                for i in range(len(song_y)):
                    song_y[i] += shift_value
               
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            click_up = True

    keys = pygame.key.get_pressed()
        
    # Ensures click only registered once (cannot hold down mouse button: must click)
    if click_down == True and click_up == True:
        click = True
        click_down = False
        click_up = False

    # Song selection
    if select == 1:

        # Sets song values to song 1's
        intro_time = intro_1
        song_time = duration_1
        song_num = 1
        song = song_1
        bpm = 0.75

        # Set health change variables
        health_gain = 10
        health_loss = 40

        # Changes target timing attributes based on conditions
        if 0 < start_time < 53:

            # Sets timing attributes of targets
            spawn_interval = bpm
            total_target_time = bpm*2 + bpm/2
            window_init = bpm
            window_final = bpm*2

            # Set starting brightness of background
            if not in_menu:
                back_brightness = 127

        elif 53 < start_time <= song_time:

            # Sets speed of attributes of targets
            spawn_interval = bpm/2
            total_target_time = (bpm*2 + bpm/2)/2
            window_init = bpm/2
            window_final = (bpm*2)/2

            # Set lighter brightness of background
            back_brightness = 50

    elif select == 2:

         # Sets song values to song 2's
        intro_time = intro_2
        song_time = duration_2
        song_num = 2
        song = song_2
        bpm = 0.7643

        # Set health change variables
        health_gain = 10
        health_loss = 40

        # Changes target timing attributes based on conditions
        if (0 < start_time <= 24.5) or (49 < start_time <= 58) or (61 < start_time <= 66) or (73 < start_time <= 76) or (79 < start_time <= 85) or (88 < start_time <= 97) or (109 < start_time <= 119) or (132 < start_time <=  song_time):

            # Timing attributes of targets
            spawn_interval = bpm
            total_target_time = bpm*2 + bpm/2
            window_init =  bpm
            window_final = bpm*2

            # Set starting brightness of background
            if not in_menu:
                back_brightness = 127

        elif (24.5 < start_time <= 49) or (58 < start_time <= 61) or (66 < start_time <= 73) or (76 < start_time <= 79)  or (85 < start_time <= 88) or (97 < start_time <= 109) or (119 < start_time <= 132):

            # Timing attributes of targets
            spawn_interval = bpm/2
            total_target_time = (bpm*2 + bpm/2)/2
            window_init = bpm/2
            window_final = (bpm*2)/2

            # Set lighter brightness of background
            back_brightness = 50

    # Resets all gameplay variables
    if reset:

        # Define what values the variables/lists/tuples are going to store 

        number_circle = 0 # Keep track of targets' spawn order
        start_time = 0 # Starting time of game level
        spawning_time = 0 # Time of spawn
        add_timey = 0 # Time in menu
        health = 400 # Health of player
        health_point = 0 # Value that is used to gradually change to health value
        multiplier = 1 # Multiplier for points in game_level
        points = 0 # Points gained
        point = 0 # Value that is used to gradually change to points value
        accuracy = 0 # Accuracy based on how many hit from total spawned
        current_target_hit = 0 # Total targets hit
        current_targets = 0 # Total targets spawned
        screen_cover = 255 # Brightness of all main screens(every game state except menu)
        cover = 255 # Brightness of background
        dead = False # Player state
        in_menu = False # Menu state
        highest_combo = 0 # Highest combo in game
        mult_size = 25 # Size of multplier in game level
        
        mult_effect = [] # Records how many times the multplier is changing and creates the same effect for each one
        total_acc = [[0, "Perfect"], [0, "Early"], [0, "Late"], [0, "Miss"]] # Records total perfects, misses, lates and earlys

        # Creates bounding boxes for buttons of menu
        continue_rect_norm = pygame.Rect((WIDTH/2) - 320/2, 175, 320, 75)
        retry_rect_norm = pygame.Rect((WIDTH/2) - 320/2, 320, 320, 75)
        selection_rect_norm = pygame.Rect((WIDTH/2) - 320/2, 470, 347, 75)

        # Used to make music only play once 
        song_start = True
        start_preview = False

        # Remove all target attributes
        for i in range(len(targets)-1, -1, -1):
            remove_target(i)

        reset = False

    # Display background of song
    if selection_screen or in_game or evaluation_screen:
        screen.blit(back[song_num], (0,0))
    
    # Sets brightness depending on game state
    if title_transition:
        brightness = 255
        back_brightness = 255

    elif title_screen:
        brightness = 125
        back_brightness = 0

    elif selection_screen:
        brightness = 0
        back_brightness = 100

    elif in_menu:
        brightness = 150

    elif evaluation_screen:
        brightness = 0
        back_brightness = 200

    else:
        brightness = 0

    # Gradually increase brightness of main screens
    if screen_cover > brightness:
        screen_cover -= 2
        if screen_cover < brightness:
            screen_cover = brightness
    elif screen_cover < brightness:
        screen_cover += 2
        if screen_cover > brightness:
            screen_cover = brightness

    # Gradually increase brightness of background
    if cover > back_brightness:
        cover -= 2
        if cover < back_brightness:
            cover = back_brightness
    elif cover < back_brightness:
        cover += 2
        if cover > back_brightness:
            cover = back_brightness
        
    brightness_change(cover) # Change background screen's brightness

    # Starting screen
    if title_screen == True:

        # Render the font for title
        title = create_font(game_font, 75, "Beat Clicker", WHITE)
        title_press = create_font(game_font, 15, "PRESS SCREEN TO START", WHITE)

        # Display background
        screen.blit(back[0], (0,0))

        # Display title name
        screen.blit(title, (300, 300))
        screen.blit(title_press, (400, 400))

        # When screen is clicked, switch to song selection menu
        if click:
            title_transition = True

        if title_transition:

            # Switch to selection screen
            if screen_cover == 255:
                title_screen = False
                selection_screen = True
                title_transition = False

    # Screen to select song
    elif selection_screen:
        
        # Play song 
        if not start_preview:
            start_preview = True
            if start_preview and (select == 1 or select == 2): # Only play available songs
                song_play(song, -1, 15)

        # Ensure selection boxed within window
        if song_y[0]< 235:
            still_y = 235
            for i in range(len(song_rects)):
                song_y[i] = still_y
                still_y += 80
        elif song_y[1] > 395:
            still_y = 395
            for i in range(len(song_rects)-1, -1, -1):
                song_y[i] = still_y
                still_y -= 80

        # Dimensions of sound rectangles
        song_1_rect = pygame.Rect(550, song_y[0], 450, 70)
        song_2_rect = pygame.Rect(550, song_y[1], 450, 70)
        song_rects = [song_1_rect, song_2_rect]
        song_rect_colour = [WHITE, WHITE]

        # Create font for highscore values
        high_score_word_font = create_font(game_font, 25, "HIGH SCORE", WHITE)
        high_score_font = create_font(game_font, 40, str(leaderboard[song_num-1][0]), WHITE)
        high_rank_font = create_font(game_font, 250, str(leaderboard[song_num-1][1]), WHITE)

        # Displays selection boxes
        for i in range(len(song_rects)):
            if song_y[i] == 315:
                song_rect_colour[i] = BLACK
            else:
                song_rect_colour[i] = BLUE

            pygame.draw.rect(screen, song_rect_colour[i], song_rects[i])
        
        # Displays description of song
        screen.blit(song_1_bar, (song_rects[0].x, song_rects[0].y))
        screen.blit(song_2_bar, (song_rects[1].x, song_rects[1].y))

        # Displays high scores
        screen.blit(high_score_word_font, (30, 100)) #(200, 150)
        screen.blit(high_score_font, (30, 130)) #(200, 180)
        screen.blit(high_rank_font, (200, 225))
        
    # Displays evaluation screen
    elif evaluation_screen:

        # Calculates rank given to player
        if accuracy == 100 and total_acc[perfect] == current_targets:
            rank = "SS"
        if 90 <= accuracy < 100  and current_targets*0.9 <= total_acc[perfect][0] < current_targets:
            rank = "S"
        if 80 <= accuracy < 90 and current_targets*0.8 <= total_acc[perfect][0] < current_targets*0.9:
            rank = "A"
        if 70 <= accuracy < 80 and current_targets*0.7 <= total_acc[perfect][0] < current_targets*0.8:
            rank = "B"
        if 60 <= accuracy < 70 and current_targets*0.6 <= total_acc[perfect][0] < current_targets*0.7:
            rank = "C"
        if 50 <= accuracy < 60 and current_targets*0.5 <= total_acc[perfect][0] < current_targets*0.6:
            rank = "D"
        if accuracy < 50 or dead == True:
            rank = "F"

        # Determines if new high score is found
        if points > leaderboard[song_num-1][0]:
            leaderboard[song_num-1] = [points, rank]

        # Creates fonts required for the screen
        rank_font = create_font(game_font, 250, rank, WHITE)
        total_score_font = create_font(game_font, 50, str(points), WHITE)
        accuracy_font = create_font(game_font, 35, f"Acc  {accuracy}%", WHITE)
        combo_font = create_font(game_font, 30, f"Combo  {highest_combo}x", WHITE)

        # Text and font for the end screen stats
        for i in range (len(total_acc)):
            
            # Different colours fo each word
            if i == 0:
                COLOUR = BLUE
            if i == 1:
                COLOUR = GREEN
            if i == 2:
                COLOUR = YELLOW
            if i == 3:
                COLOUR = RED

            # Create accuracy fonts
            accuracy_stats = create_font(game_font, 30, str(total_acc[i][0]), WHITE)
            accuracy_names = create_font(game_font, 15, str(total_acc[i][1]), COLOUR)

            # Display accuracy values
            screen.blit(accuracy_stats, (25, 275 + 75*i))
            screen.blit(accuracy_names, (25, 250 + 75*i))
        
        # Display rank, total score, accuracy and max combo
        screen.blit(rank_font, (400, 200))
        screen.blit(total_score_font, (20, 175))
        screen.blit(accuracy_font, (20, 550)) 
        screen.blit(combo_font, (20, 600))

    # When health is reduced to zero or start time is greater than song_time, switches evaluation screen 
    if health <= 0:
        in_game = False
        dead = True
        evaluation_screen = True  
    
    if start_time > song_time:
        in_game = False
        evaluation_screen = True  

    # In game
    if in_game:

        # Stores highest combo of song level
        if highest_combo < multiplier:
            highest_combo = multiplier

        if not in_menu:
            menu_start = True

            # Start the song
            if song_start == True:
                new_time = current_time
                song_play(song)
            song_start = False

            start_time = current_time - new_time # Stopwatch for song being played
        
        if start_time > intro_time:

            # Gets position and speed for the targets until the target amount limit based on bpm and rhythm of song
            if start_time >= spawning_time and start_time < song_time-2:
                target_X = random.randint(target_width, (WIDTH - target_width*2))
                target_Y = random.randint(target_height + 50, (HEIGHT - target_height*2))

                check = True

                # Checks if targets are overlapping with already spawned in targets on screen
                if len(targets) >= 1:
                    while check == True:
                        spawn_target = pygame.Rect(target_X, target_Y, target_width, target_height)
                        found_bad = False
                        for initial_target in targets:
                            if spawn_target.colliderect(initial_target):
                                found_bad = True
                                break
                        if found_bad == True:
                            target_X = random.randint(target_width, (WIDTH - target_width*2))
                            target_Y = random.randint(target_height, (HEIGHT - target_height*2)) 
                        else:
                            check = False
                        
                # Ensures numbers on the circle don't exceed 10 for clarity
                number_circle += 1
                if number_circle > 9:
                    number_circle = 1
                
                # Appends dimenstions and location for the target
                targets.append(pygame.Rect(target_X, target_Y, target_height, target_width))

                # Appends all attributes for target
                window.append(start_time)
                target_time.append(start_time)
                indicator.append(WHITE)
                target_alpha.append(0)
                target_number.append(number_circle)

                # resets spawining time
                spawning_time = start_time + spawn_interval
            
            # Collisions, animations and movement of targets
            for i in range(len(targets)-1, -1, -1):

                # Starts as transparent and becomes opaque based on interval
                if target_alpha[i] < 255:
                    target_alpha[i] += 255/(60*(window_init/2))
                    if target_alpha[i] > 225:
                        target_alpha[i] = 225

                # Only allow target to be hit for a window of time
                if (window_init < start_time - window[i] < window_final):
                    indicator[i] = RED

                    # Collision of sword (cursor) to object will delete the target, grant points, change values for on screen numeric values
                    if sword.colliderect(targets[i]) and click == True:
                        target_hit.play()
                        remove_target(i)
                        current_targets += 1 
                        current_target_hit += 1
                        multiplier += 1
                        mult_effect.append(50)
                        total_acc[perfect][0] += 1
                        points += 300*multiplier

                        # Add health per target perfect
                        if health < 400:
                            health += health_gain
                        else:
                            health = 400
                
                # Make player get less points for going too early and multiplier resets
                elif start_time - target_time[i] < window_init:
                    if sword.colliderect(targets[i]) and click == True:
                        remove_target(i)
                        points += 100*multiplier
                        current_targets += 1
                        total_acc[early][0] += 1
                        multiplier = 1
                
                # Make player get less points for going too late and multiplier resets
                elif start_time - target_time[i] > window_init and start_time - target_time[i] < total_target_time:
                    indicator[i] = WHITE
                    if sword.colliderect(targets[i]) and click == True:
                        remove_target(i)
                        points += 100*multiplier
                        current_targets += 1
                        total_acc[late][0] += 1
                        multiplier = 1

                # Deletes the attributes of the target and makes player take damage if target damage window was missed
                elif start_time - target_time[i] >= total_target_time:
                    remove_target(i)
                    current_targets += 1
                    multiplier = 1
                    total_acc[miss][0] += 1
                    health -= health_loss

            # Calculates accuracy      
            if current_targets > 0:
                accuracy = round(((current_target_hit/current_targets)*100), 2)

            # Makes points increase to the total points to give an effect for the points on the game screen
            if point != points:
                point += 100*multiplier
                if point > points:
                    point = points

        if start_time > intro_time:
            
            # Displays target
            for i, target in enumerate(targets):

                target_radius = target_width/2
                target_border_radius = target_width/1.85

                # Displays border of target
                target_border_surface = pygame.Surface((target.width*1.8, target.height*1.8), pygame.SRCALPHA)
                pygame.draw.circle(target_border_surface, (*indicator[i], target_alpha[i]), (target_border_radius,target_border_radius), target_border_radius)
                screen.blit(target_border_surface, (target.x - (target_border_radius - target_radius) + 1, target.y - (target_border_radius - target_radius) + 1)) 

                # Displays center of target
                target_surface = pygame.Surface((target.width, target.height), pygame.SRCALPHA)
                pygame.draw.circle(target_surface, (*(41, 89, 186), target_alpha[i]), (target_radius,target_radius), target_radius)
                screen.blit(target_surface, (target.x, target.y))   
                    
                # Displays order of target spawning in number on the targets
                target_font = create_font(game_font, 30, str(target_number[i]), WHITE)
                screen.blit(target_font, (target.x + target.width/2 - 10 , target.y + target.height/2 - 17))
            
            # Displays the effect for the multplier
            for i in range(len(mult_effect) -1, -1, -1):

                # Shrinks the effect of multiplier
                if mult_effect[i] > 25:
                    mult_effect[i] -= 1.5

                # Slowly increases the multiplier size
                else:
                    while mult_size != 40:
                        mult_size += 1
                    mult_effect.pop(i)
                    continue
                
                # Makes mult effect font and the regular mult font
                mult_font = create_font(game_font, mult_size, f"{multiplier}x", WHITE)
                mult_effect_font = create_font(game_font, int(mult_effect[i]), f"{multiplier}x", WHITE, 127)

                # Displays multiplier and its effect
                screen.blit(mult_font, (10, HEIGHT - (15 + int(mult_size))))
                screen.blit(mult_effect_font, (10, HEIGHT - ( 15 + int(mult_effect[i]))))
        
        # Render the font with point system features
        score_font = create_font(game_font, 40, str(point), WHITE)
        acc_font = create_font(game_font, 20, f"{accuracy}%", WHITE)

        # Display point system features on screen
        screen.blit(score_font, (10, 5))
        screen.blit(acc_font, (10, 45))

        # Gradual change value of health bar
        if health_point > health:
            health_point -= 2
        elif health_point < health:
            health_point += 2

        # Display health bar
        healthbar_rect = pygame.Rect(990 - health_point, 15 , health_point, 10)
        pygame.draw.rect(screen, WHITE, healthbar_rect)
        
        # Makes the multplier icon shrink back when it gets enlarged to produce an effect
        if mult_size != 25 : 
            multplier_true = multiplier
            mult_size -= 1
            mult_font = create_font(game_font, mult_size, f"{multiplier}x", WHITE)
            screen.blit(mult_font, (10, HEIGHT - 40))

        # Displays the multplier icon when static
        else:
            mult_font = create_font(game_font, mult_size, f"{multiplier}x", WHITE)
            screen.blit(mult_font, (10, HEIGHT - 40))

    brightness_change(screen_cover) # Brightness of surface

    if in_menu or evaluation_screen:
        
        pygame.mixer.music.pause()

        # Changes location of bounding box when in evaluation screen
        if evaluation_screen:
            retry_rect_norm.x, retry_rect_big.x = 625, 625 - 2.5
            retry_rect_norm.y,retry_rect_big.y = 460, 460 - 2.5
            selection_rect_norm.x, selection_rect_big.x = 625, 625 - 2.5
            selection_rect_norm.y, selection_rect_big.y = 560, 560 - 2.5
        else:
            continue_rect_big = pygame.Rect((WIDTH/2) - 342/2, 175-2.5, 342, 80)
            retry_rect_big = pygame.Rect((WIDTH/2) - 342/2, 320-2.5, 342, 80)
            selection_rect_big = pygame.Rect((WIDTH/2) - 342/2, 475-2.5, 342, 80)

        # Calculate time in menu
        if in_menu:
            if menu_start == True:
                time_in_menu = current_time
            add_timey = current_time - time_in_menu
            menu_start = False
            
        # Sets all menu buttons to regular size
        retry_button = retry_button_norm
        retry_rect = retry_rect_norm
        continue_button = continue_button_norm
        continue_rect = continue_rect_norm
        selection_button = selection_button_norm
        selection_rect = selection_rect_norm

        # Enlarges buttons when hovering on to buttons and operate the functions that are displayed on them (all collide lines of code)
        if in_menu:
            if sword.colliderect(continue_rect_norm):
                continue_button = continue_button_big
                continue_rect = continue_rect_big

                # Resume game level
                if click == True:
                    in_menu = False
                    new_time += add_timey # Updates clock
                    pygame.mixer.music.unpause() # Resume song

        if sword.colliderect(retry_rect_norm):
            retry_button = retry_button_big
            retry_rect = retry_rect_big

            # Restart game level
            if click == True:
                evaluation_screen = False
                reset = True
                in_game = True
        
        if sword.colliderect(selection_rect_norm):
            selection_button = selection_button_big
            selection_rect = selection_rect_big

            # Goes to back to selection menu
            if click == True:
                in_game = False
                evaluation_screen = False
                reset = True
                selection_screen = True
        
        # Displays buttons
        if in_menu:
            screen.blit(continue_button, (continue_rect.x, continue_rect.y))
        screen.blit(retry_button, (retry_rect.x, retry_rect.y))
        screen.blit(selection_button, (selection_rect.x, selection_rect.y))
    
    # Display cursor in a form of particles
    particles.append([[mouse_X, mouse_Y], random.randint(8,9)])
    for particle in particles:
        particle[1] -= 0.4 # Reduce particle radius

        # Display center of particle
        pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[1]))

        particle_radius = particle[1] * 2

        # Display glow of particle
        screen.blit(particle_outline(particle_radius, PURPLE), (int(particle[0][0] - particle_radius), int(particle[0][1] - particle_radius)), special_flags=BLEND_RGB_ADD)
        
        if particle[1] <= 0:
            particles.remove(particle)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
