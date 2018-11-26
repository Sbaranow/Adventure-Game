# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.

import sys, pygame, math

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frame_counts

# The main loop handles most of the game
def main():

    # Initialize pygame
    pygame.init()

    screen_size = height, width = (700, 500)
    screen = pygame.display.set_mode(screen_size)

    # create the hero character
    hero = load_piskell_sprite("hero",21)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (350,250)

    # add in another character
    ghost = pygame.image.load("pacman_ghost.png").convert_alpha()
    ghost_rect = ghost.get_rect()
    ghost_rect.center = 100, 200

    # add in a treasure item
    treasure = pygame.image.load("treasurechest.png").convert_alpha()
    treasure_rect = treasure.get_rect()
    treasure_rect.center = 750,400

    # add in sword
    sword = pygame.image.load ("sword.png").convert_alpha()
    sword_rect = sword.get_rect()
    sword_rect.center = 550,300

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Mostly used to cycle the animation of sprites
    frame_count = 0;

    # variable to show if we are still playing the game
    playing = True

    # variable for hero direction
    is_facing_left = True

    # Variable to track text on the screen. If you set the dialog string to something and set the position and the
    # counter, the text will show on the screen for dialog_counter number of frames.
    dialog_counter = 0
    dialog = ''
    dialog_position = (0,0)

    # Load font
    pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)


    # create the inventory and make it empty
    inventory = {}

    # This list should hold all the sprite rectangles that get shifted with a key press.
    rect_list = [ghost_rect, treasure_rect, sword_rect]

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((170,190,190))

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        # check for keys that are pressed
        # Note the indent makes it part of the while playing but not part of the for event loop.
        keys = pygame.key.get_pressed()
        # check for specific keys
        # movement says how the world should shift. Pressing keys changes the value in the movement variables.
        movement_x = 0
        movement_y = 0
        if keys[pygame.K_LEFT]:
            is_facing_left = True
            movement_x += 5
        if keys[pygame.K_RIGHT]:
            is_facing_left = False
            movement_x -= 5
        if keys[pygame.K_UP]:
            movement_y += 5
        if keys[pygame.K_DOWN]:
            movement_y -= 5

        # Move all the sprites in the scene by movement amount.
        # You can still move the rect of an individual sprite to make
        # it move around the landscape.
        for rect in rect_list:
            rect.move_ip(movement_x, movement_y)

        # Check for touching ghost.
        if hero_rect.colliderect(ghost_rect):
            # Respond differently depending on gold status
            if "sword" and "gold" in inventory:
                dialog = "merchant?"
            elif "gold" in inventory:
                dialog = "Welcome rich friend!"
            elif 'sword' in inventory:
                dialog = "scary!!!"

            else:
                dialog = "Go away loser!"
            # These say where and for how long the dialog prints on the screen
            dialog_counter = 50
            dialog_position = (100, 100)

        # Check for touching the gold chest.
        if hero_rect.colliderect(treasure_rect) and "gold" not in inventory:
            inventory["gold"] = True
            dialog = "Gold added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(sword_rect) and "sword" not in inventory:
            inventory["sword"] = True
            dialog = "sword added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Draw the characters
        screen.blit(ghost, ghost_rect)
        pygame.draw.rect(screen, (0,255,0), ghost_rect, 3)

        # Draw the sword
#        screen.blit(sword, sword_rect)


        # Only draw the gold if it hasn't been picked up
        if "gold" not in inventory:
            screen.blit(treasure, treasure_rect)

        #only draw the sword if it hasnt been picked up
        if "sword" not in inventory:
            screen.blit (sword, sword_rect)

        # Pick the sprite frame to draw
        hero_sprite = hero[frame_count%len(hero)]
        # Flip the sprite depending on direction
        if not is_facing_left:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        screen.blit(hero_sprite, hero_rect)
        pygame.draw.rect(screen, (0,255,0), hero_rect, 3)

        # draw any dialog
        if dialog:
            pygame.draw.rect(screen, (220,220,220), [50, 425, 600,50])
            textsurface = myfont.render(dialog, False, (0,0,0))
            screen.blit (textsurface, (75,430))
            # textsurface = myfont.render(dialog, False, (0, 0, 0))
            # screen.blit(textsurface, dialog_position)
            # # Track how long the dialog is on screen
            # dialog_counter -= 1
            # if dialog_counter == 0:
            #     dialog = ''

        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

        # 30 fps
        clock.tick(30)

    # loop is over
    pygame.quit()
    sys.exit()

# Start the program
main()
