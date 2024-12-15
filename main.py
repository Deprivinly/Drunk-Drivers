import pygame
from pygame.locals import *
import random

pygame.init()

# Window 
width = 800
height = 600
screensize = (width, height)
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption('Drunk Drivers')

# Colors 
gray = (100, 100, 100)
green = (76, 208, 56)
red = (208, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Game Settings 
gameover = False
speed = 2
score = 0

# Markers 
marker_width = 10
marker_height = 50  # Reduced the height of markers to make them closer together

# Road and edge markers
road_width = 300
road = ((width - road_width) // 2, 0, road_width, height)
left_edge = ((width - road_width) // 2 - marker_width, 0, marker_width, height)
right_edge = ((width + road_width) // 2, 0, marker_width, height)

# x coordinate of lanes
left_lane = width // 2 - road_width // 6
center_lane = width // 2
right_lane = width // 2 + road_width // 6
lanes = [left_lane, center_lane, right_lane]

# for animating movement of the lane markers
lane_marker_move = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Scale the image to fit the road width, but make it slightly smaller
        image_scale = (road_width / 3 / image.get_rect().width) * 0.7  # Reduced scale by 30%
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
        self.image = pygame.transform.rotate(self.image, 90)  # Rotate 90 degrees left
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('asset/1.png')  # Corrected the image path
        super().__init__(image, x, y)

# Player's starting position (center of the screen)
player_x = width // 2
player_y = height - 100  # Slightly above the bottom of the screen

# Create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load the other vehicle images
image_filenames = ['asset/2.png', 'asset/3.png', 'asset/4.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load(image_filename)
    vehicle_images.append(image)


# sprite group for vehicles
vehicle_group = pygame.sprite.Group()


# Load the crash image
crash_image = pygame.image.load('asset/crash1.png')
crash_rect = crash_image.get_rect()

# Game loop
clock = pygame.time.Clock()
fps = 60
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # move the player's car using the left/right arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100  
            elif event.key == pygame.K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

                # check if theres a side swipe collision after changing lanes
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        gameover = True

                        # place the players car next to other vehicle
                        # Determine where to posistion the crash image
                        if event.key == pygame.K_LEFT:
                            player.rect.left = vehicle.rect.right
                            crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        elif event.key == pygame.K_RIGHT:
                            player.rect.right = vehicle.rect.left
                            crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # Draw the Grass
    screen.fill(green)

    # Draw the Road
    pygame.draw.rect(screen, gray, road)

    # Draw the Edge Markers
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)

    # Draw the Lane Markers
    lane_marker_move += speed * 2
    if lane_marker_move >= marker_height * 2:
        lane_marker_move = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane, y + lane_marker_move, marker_width, marker_height))
        pygame.draw.rect(screen, white, (right_lane, y + lane_marker_move, marker_width, marker_height))

    # Draw the Player's Vehicle
    player_group.draw(screen)

    # add up to two vehicles to the vehicle group
    if len(vehicle_group) < 2:

        # ensure theres enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:

            # select a random lane
            lane = random.choice(lanes)

            # Randomly select the vehicle image and lane
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)


    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # remove the vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()

            # add a score
            score += 1

            # speed up the game
            if score > 0 and score % 5 == 0:
                speed += 1

    
    # Draw the vehicles
    vehicle_group.draw(screen)

    # Display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.bottomright = (width - 20, height - 20)  # Position in bottom right
    screen.blit(text, text_rect)

    # check if there's a head-on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

        # Display game over
        if gameover:
            screen.blit(crash_image, crash_rect)

            pygame.draw.rect(screen, red, (0, 50, width, 100))

            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width // 2, 100)
            screen.blit(text, text_rect)
            

    pygame.display.update()

    # check if player wants to play again
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                running = False

            # get the players input (y or N)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == pygame.K_n:
                    # exit the game
                    gameover = False
                    running = False

pygame.quit()
