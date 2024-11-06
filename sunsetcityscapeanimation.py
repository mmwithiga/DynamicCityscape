import pygame
import random

# Initialize Pygame
pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Sunset Cityscape")

# Color stages for the sky (day to twilight)
SKY_COLORS = [
    ((135, 206, 235), (176, 224, 230)),  # Daylight blues
    ((255, 153, 51), (255, 204, 153)),  # Sunset oranges
    ((255, 102, 102), (153, 50, 204)),  # Intense red and purple
    ((25, 25, 112), (0, 0, 139))  # Twilight blues
]

# Colors for other elements
SUN_COLOR = (255, 140, 0)  # Orange sun
WINDOW_COLOR = (255, 223, 186)  # Warm light windows
ROAD_COLOR = (50, 50, 50)  # Dark road
CAR_BODY_COLOR = (200, 0, 0)  # Lamborghini red for the car body
CAR_WHEEL_COLOR = (30, 30, 30)  # Dark gray for car wheels

# Car speed across the screen
car_speed = 1.5


# Function to draw gradient sky transitioning from top color to bottom color
def draw_sky(sky_top, sky_bottom):
    for i in range(HEIGHT):  # Loop over the screen height
        ratio = i / HEIGHT  # Calculate the ratio for blending colors
        color = (
            int(sky_top[0] * (1 - ratio) + sky_bottom[0] * ratio),
            int(sky_top[1] * (1 - ratio) + sky_bottom[1] * ratio),
            int(sky_top[2] * (1 - ratio) + sky_bottom[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))  # Draw each line with the blended color


# Function to draw the setting sun at a specific y-position
def draw_sun(y_position):
    pygame.draw.circle(screen, SUN_COLOR, (WIDTH // 2, y_position), 60)  # Sun is centered horizontally


# Function to draw stylized buildings with random heights, widths, and organized windows
def draw_buildings(buildings):
    for building in buildings:
        x, building_width, building_height, building_color = building["x"], building["width"], building["height"], \
        building["color"]
        pygame.draw.rect(screen, building_color, (x, HEIGHT - building_height, building_width, building_height))

        # Draw windows in rows and columns on each building
        for i in range(1, building_height // 40):
            for j in range(2, building_width // 30):
                win_x = x + j * 30  # X-coordinate of window
                win_y = HEIGHT - building_height + i * 40  # Y-coordinate of window
                pygame.draw.rect(screen, WINDOW_COLOR, (win_x, win_y, 20, 20))  # Each window is 20x20 pixels


# Function to draw a car at a given x-position
def draw_car(x_position):
    # Draw car body (rectangle for main body, polygon for the top)
    pygame.draw.rect(screen, CAR_BODY_COLOR, (x_position, HEIGHT - 80, 80, 30))
    pygame.draw.polygon(screen, CAR_BODY_COLOR, [(x_position + 10, HEIGHT - 80), (x_position + 70, HEIGHT - 80),
                                                 (x_position + 60, HEIGHT - 100), (x_position + 20, HEIGHT - 100)])

    # Draw car wheels as small circles
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x_position + 20, HEIGHT - 50), 10)  # Front wheel
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x_position + 60, HEIGHT - 50), 10)  # Rear wheel


# Main animation loop
clock = pygame.time.Clock()  # Set up the clock for a smooth frame rate
sun_y = 100  # Initial position of the sun
car_x = -100  # Initial x-position of the car, starts off-screen

# Initialize buildings with random heights, widths, colors, and spaced across the screen
buildings = [{"x": i * 150 + WIDTH, "width": random.randint(60, 100), "height": random.randint(200, 400),
              "color": (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))}  # Random color
             for i in range(6)]
running = True
sky_stage = 0  # Start with the first color stage
stage_thresholds = [100, 300, 500]  # Heights where the sky color transitions to the next stage

while running:
    for event in pygame.event.get():  # Event loop to check for quit
        if event.type == pygame.QUIT:
            running = False

    # Select colors based on sun's height (sky_stage advances as the sun descends)
    if sun_y > stage_thresholds[sky_stage] and sky_stage < len(SKY_COLORS) - 1:
        sky_stage += 1  # Move to the next sky color stage
    sky_top, sky_bottom = SKY_COLORS[sky_stage]  # Get the current sky colors

    # Draw the sunset background and cityscape elements
    draw_sky(sky_top, sky_bottom)  # Draw gradient sky
    draw_sun(sun_y)  # Draw the setting sun
    draw_buildings(buildings)  # Draw buildings
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT - 40, WIDTH, 40))  # Draw road at the bottom
    draw_car(car_x)  # Draw car moving across the screen

    # Update positions for animation
    sun_y += 0.1 if sun_y < HEIGHT else 0  # Sun slowly moves downward
    car_x = (car_x + car_speed) % WIDTH  # Car moves right and wraps to the left after crossing the screen

    # Move buildings leftward at the same speed as the car
    for building in buildings:
        building["x"] -= car_speed  # Shift building left
        if building["x"] < -building["width"]:  # If building goes off-screen, reset it on the right
            building["x"] = WIDTH + random.randint(50, 150)  # Place it randomly off-screen to the right
            building["height"] = random.randint(200, 400)  # Randomize new building height
            building["width"] = random.randint(60, 100)  # Randomize new building width
            building["color"] = (
            random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))  # New random color

    pygame.display.flip()  # Update the screen with new drawings
    clock.tick(60)  # Maintain smooth 60 frames per second

# Quit Pygame when the loop ends
pygame.quit()