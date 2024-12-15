# Drunk-Drivers

Core Game Elements
Game Objective:

The player navigates their car left or right across lanes to avoid collisions with other vehicles.
The score increases as vehicles are successfully avoided.
The game gets progressively harder as the speed increases.
Player Car:

The player's car starts at the bottom-center of the road and can move left or right between predefined lanes.
Enemy Vehicles:

Other vehicles spawn at random lanes and move down the screen.
The player must avoid these vehicles to continue playing.
Game Over:

The game ends when the player collides with another car (head-on or side collision).
A "Game Over" screen appears, allowing the player to restart or exit the game.
Detailed Explanation
1. Initialization
Pygame Setup:
Initializes Pygame, sets up the display, and defines essential variables like screen size, colors, and game settings.
Road and Lanes:
The road is centered on the screen with three lanes:
Left lane, center lane, and right lane.
Lane markers and road edge markers are drawn for visual clarity.
2. Player Car
Player Initialization:

The player's car is represented by a PlayerVehicle class, a specialized subclass of the Vehicle class.
The player's car starts at the bottom-center of the road (player_x, player_y).
Player Movement:

The player can move left or right by pressing the arrow keys.
Movement is constrained to the three lanes using checks (if event.key == pygame.K_LEFT and lane boundaries).
Collision Detection:

Side Swipe: Checks for a collision when the player changes lanes.
Head-On: Checks for a collision when enemy cars overlap the player's car.
3. Enemy Vehicles
Random Spawn:
Enemy vehicles are created randomly using the Vehicle class.
They spawn at random lanes and move downward at the current game speed.
Despawn:
Once an enemy vehicle moves off-screen, it is removed from memory (vehicle.kill()), and the score is incremented.
Difficulty Scaling:
Every 5 points, the game speed increases, making it more challenging to avoid cars.
4. Lane and Road Design
Road:
A gray rectangle in the middle of the screen represents the road.
Lane Markers:
White markers are drawn at regular intervals, creating a dashed-line effect.
The markers move upward, creating the illusion of forward motion (lane_marker_move).
5. Game Over
Collision Handling:
When the player collides with an enemy vehicle:
The game displays a crash image at the point of collision.
A "Game Over" screen is displayed, prompting the player to restart or exit.
Restart Option:
Pressing "Y" resets the game variables, such as the score, speed, and enemy vehicles.
Exit Option:
Pressing "N" exits the game.
Key Classes and Methods
Vehicle Class:

Represents both the player's car and enemy vehicles.
Scales and rotates the vehicle images for proper display.
PlayerVehicle Class:

A subclass of Vehicle, specific to the player's car.
Initializes the player’s car with its starting position and image.
Collision Detection:

Uses pygame.sprite.collide_rect() and pygame.sprite.spritecollide() for precise hit detection between vehicles.
Gameplay Flow
Start:

The game starts with the player’s car positioned in the center lane.
Enemy vehicles spawn randomly in lanes and move downward.
Player Input:

The player moves left or right using arrow keys to avoid collisions.
Score and Speed:

The player earns points for every vehicle successfully avoided.
The speed of the game increases as the score progresses.
Game Over:

Collision with an enemy vehicle ends the game.
The player is prompted to restart or exit.
Game Features
Dynamic Difficulty:

Speed increases as the score increases, making the game progressively harder.
Collision Detection:

Handles both head-on and side-swipe collisions with realistic positioning adjustments.
Game Over Screen:

Displays a crash image and allows the player to restart or exit.
Visual Effects:

Moving lane markers and scaled vehicles add to the visual appeal of the game.
Possible Enhancements
Add sound effects for collisions and background music.
Introduce power-ups (e.g., slow-motion or extra lives).
Implement different vehicle speeds for added difficulty.
Track high scores and display them on the game over screen.
