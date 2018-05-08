#--------------------------------------------------------------------#
#
#  RANDOM PACMAN
#
#  In this task you will create a simple simulation using the PyGame
#  package.  The program will animate the characters from the
#  popular video arcade game Pacman.  There will be four ghosts and
#  Pacman himself.  All of the characters randomly bounce around the
#  screen in the same way as the supplied bouncing ball demonstration
#  program.  The ghosts do not interact and pass through each other.
#  However, if Pacman collides with a ghost one of two actions
#  occurs depending on the game's mode.  In the initial, default mode
#  Pacman is scared of ghosts, so in this case Pacman should bounce
#  off in a random direction and the ghost should continue on its
#  original course.  In the second mode the ghosts are scared of
#  Pacman, so the ghost should be deflected and Pacman should
#  continue moving straight.  The mode can be toggled by clicking the
#  mouse in the window.  Different images for the ghosts should
#  be displayed depending on the mode.  See the instructions
#  accompanying this file for illustrations.
#  
#--------------------------------------------------------------------#

import pygame
from random import randint
from random import randrange

pygame.init()

#Assigning image and sound files names in the program.
GHOST_BLUE_IMAGE_LEFT = 'images/blue-left.png'
GHOST_BLUE_IMAGE_RIGHT = 'images/blue-right.png'
GHOST_RED_IMAGE_LEFT = 'images/red-left.png'
GHOST_RED_IMAGE_RIGHT = 'images/red-right.png'
GHOST_PINK_IMAGE_LEFT = 'images/pink-left.png'
GHOST_PINK_IMAGE_RIGHT = 'images/pink-right.png'
GHOST_ORANGE_IMAGE_LEFT = 'images/orange-left.png'
GHOST_ORANGE_IMAGE_RIGHT = 'images/orange-right.png'
GHOST_VULNERABLE_IMAGE = 'images/vulnerable.png'
PACMAN_IMAGE_LEFT = 'images/pacman-left.png'
PACMAN_IMAGE_RIGHT = 'images/pacman-right.png'
BOUNCE_WAV = 'sounds/bounce.wav'
WAKKA_WAV = 'sounds/pacman_wakka.wav'
MODE_CHANGE_WAV = 'sounds/change_mode.wav'

#Setting up the screen and resources.
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOUR = 0, 0, 0
CAPTION = 'PacMan and Friends'
frame = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)
timer = pygame.time.Clock()
BOUNCE_SOUND = pygame.mixer.Sound(BOUNCE_WAV)
WAKKA_SOUND = pygame.mixer.Sound(WAKKA_WAV)
MODE_CHANGE_SOUND = pygame.mixer.Sound(MODE_CHANGE_WAV)

#Creating a creature class, for ease of use, and setting up our ghosts and pacman
class Creature:
    def __init__(self):
        self.image = ()
        self.frame = ()
        self.boundary = ()
        self.velocity = ()

#Create our creatures using our class and put them in a list for future use.
ghost_blue = Creature()
ghost_red = Creature()
ghost_pink = Creature()
ghost_orange = Creature()
pacman = Creature()
creature_list = [ghost_blue, ghost_red, ghost_pink, ghost_orange, pacman]
ghost_list =[ghost_blue, ghost_red, ghost_pink, ghost_orange]

#Assigning possible images (frames) to our little monsters and loading them with their transparent space intact.
ghost_blue.frame = [pygame.image.load(GHOST_BLUE_IMAGE_LEFT).convert_alpha(), pygame.image.load(GHOST_BLUE_IMAGE_RIGHT).convert_alpha()]
ghost_red.frame = [pygame.image.load(GHOST_RED_IMAGE_LEFT).convert_alpha(), pygame.image.load(GHOST_RED_IMAGE_RIGHT).convert_alpha()]
ghost_pink.frame = [pygame.image.load(GHOST_PINK_IMAGE_LEFT).convert_alpha(), pygame.image.load(GHOST_PINK_IMAGE_RIGHT).convert_alpha()]
ghost_orange.frame = [pygame.image.load(GHOST_ORANGE_IMAGE_LEFT).convert_alpha(), pygame.image.load(GHOST_ORANGE_IMAGE_RIGHT).convert_alpha()]
pacman.frame = [pygame.image.load(PACMAN_IMAGE_LEFT).convert_alpha(), pygame.image.load(PACMAN_IMAGE_RIGHT).convert_alpha()]
ghost_vulnerable = pygame.image.load(GHOST_VULNERABLE_IMAGE).convert_alpha()

#Assigning an image to the creature from its frames [0] for left facing (default), [1] for right.
def assign_images(creature):
    creature.image = creature.frame[0]

#Assigning boundaries to our creatures, also, spawn in random locations (within 100 pixels) to the middle of the screen
def create_creature_boundary(creature):
    creature.boundary = creature.image.get_rect(center = ((WIDTH/2)+randint(-150,150),((HEIGHT/2)+randint(-150,150))))

#Assigning our creatures a random velocity (making sure their velocity is either -5 or 5 for x and y directions respectively)
def create_creature_velocity(creature):
    creature.velocity = [randrange(-5,6,5),randrange(-5,6,5)]
    while creature.velocity[0] == 0 or creature.velocity[1] == 0:
        creature.velocity = [randrange(-5,6,5),randrange(-5,6,5)]

#Using our creature list to call the two above functions for creature setup.
for creature in creature_list:
    assign_images(creature)
    create_creature_boundary(creature)
    create_creature_velocity(creature)

##################################
#End of screen and creature setup
##################################


##################################
#Start of game functions.
##################################

#Blitting of images
def blitting(creature):
    frame.blit(creature.image, creature.boundary)

#Checks to see what direction ghosts are moving and changes image depending.
def ghost_direction_checker(ghosts):
    if ghosts.velocity[0] < 0 and ghosts_scared == False:
        ghosts.image = ghosts.frame[0]
    elif ghosts.velocity[0] > 0 and ghosts_scared == False:
        ghosts.image = ghosts.frame[1]
    elif ghosts_scared == True:
        ghosts.image = ghost_vulnerable

#Checks to see what direction pacman is moving and changes image depending.
def pacman_direction_checker():
    if pacman.velocity[0] < 0:
        pacman.image = pacman.frame[0]
    elif pacman.velocity[0] > 0:
        pacman.image = pacman.frame[1]

#Move our creatures based on their velocity
def creature_movement(creature):
    creature.boundary = creature.boundary.move(creature.velocity)

#Wall collision detection, bounce off if creature hits a wall. (play sound only if hitting left or right wall)
def wall_collision(creature):
    if creature.boundary.left < 0 or creature.boundary.right > WIDTH:
        BOUNCE_SOUND.play()
        creature.velocity[0] = -1 * creature.velocity[0]
    if creature.boundary.top < 0 or creature.boundary.bottom > HEIGHT:
        creature.velocity[1] = -1 * creature.velocity[1]

#Check if pacman and ghosts collide.
def pacman_ghost_collision(ghosts):
    if pacman.boundary.colliderect(ghosts.boundary) == True:
        WAKKA_SOUND.play()
        if ghosts_scared == False:
            pacman.velocity[0] = -1 * pacman.velocity[0]
        elif ghosts_scared == True:
            ghost.velocity[0] = -1 * ghost.velocity[0]

finished = False
ghosts_scared = False
while not finished:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            MODE_CHANGE_SOUND.play()
            if ghosts_scared == False:
                ghosts_scared = True
            elif ghosts_scared == True:
                ghosts_scared = False
    frame.fill(BACKGROUND_COLOUR)

    for creature in creature_list:
        
        blitting(creature)
        creature_movement(creature)
        wall_collision(creature)

    for ghost in ghost_list:
        pacman_ghost_collision(ghost)
        ghost_direction_checker(ghost)
    pacman_direction_checker()
    
    timer.tick(60)
    pygame.display.flip()
pygame.quit()

#
#--------------------------------------------------------------------#
         
