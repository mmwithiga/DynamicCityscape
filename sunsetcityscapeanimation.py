import pygame
import random

# Initialize Pygame
pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Sunset Cityscape")

# Color stages for the sky
SKY_COLORS = [
    ((135, 206, 235), (176, 224, 230)),  # Daylight blues
    ((255, 153, 51), (255, 204, 153)),  # Sunset oranges
    ((255, 102, 102), (153, 50, 204)),  # Intense red and purple
    ((25, 25, 112), (0, 0, 139))  # Twilight blues
]

# Colors for other elements
SUN_COLOR = (255, 140, 0)
BUILDING_COLOR = (70, 70, 70)
WINDOW_COLOR = (255, 223, 186)
ROAD_COLOR = (50, 50, 50)
CAR_BODY_COLOR = (200, 0, 0)  # Lamborghini red
CAR_WHEEL_COLOR = (30, 30, 30)

# Car speed
car_speed = 1.5

# Function to draw gradient sky
def draw_sky(sky_top, sky_bottom):
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        color = (
            int(sky_top[0] * (1 - ratio) + sky_bottom[0] * ratio),
            int(sky_top[1] * (1 - ratio) + sky_bottom[1] * ratio),
            int(sky_top[2] * (1 - ratio) + sky_bottom[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

# Function to draw the setting sun
def draw_sun(y_position):
    pygame.draw.circle(screen, SUN_COLOR, (WIDTH // 2, y_position), 60)

# Function to draw stylized buildings
def draw_buildings(buildings):
    for building in buildings:
        x, building_width, building_height = building["x"], building["width"], building["height"]
        pygame.draw.rect(screen, BUILDING_COLOR, (x, HEIGHT - building_height, building_width, building_height))
        
        # Draw windows with an organized, symmetrical style
        for i in range(1, building_height // 40):
            for j in range(2, building_width // 30):
                win_x = x + j * 30
                win_y = HEIGHT - building_height + i * 40
                pygame.draw.rect(screen, WINDOW_COLOR, (win_x, win_y, 20, 20))

# Function to draw a red Lamborghini-style car
def draw_car(x_position):
    # Draw car body
    pygame.draw.rect(screen, CAR_BODY_COLOR, (x_position, HEIGHT - 80, 80, 30))
    pygame.draw.polygon(screen, CAR_BODY_COLOR, [(x_position + 10, HEIGHT - 80), (x_position + 70, HEIGHT - 80), 
                                                 (x_position + 60, HEIGHT - 100), (x_position + 20, HEIGHT - 100)])
    
    # Draw car wheels
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x_position + 20, HEIGHT - 50), 10)
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x_position + 60, HEIGHT - 50), 10)

# Main animation loop
clock = pygame.time.Clock()
sun_y = 100
car_x = -100

# Initialize buildings with random heights and widths
buildings = [{"x": i * 150 + WIDTH, "width": random.randint(60, 100), "height": random.randint(200, 400)} for i in range(6)]
running = True
sky_stage = 0
stage_thresholds = [100, 300, 500]  # Heights where the sky color changes

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Select colors based on sun's height
    if sun_y > stage_thresholds[sky_stage] and sky_stage < len(SKY_COLORS) - 1:
        sky_stage += 1
    sky_top, sky_bottom = SKY_COLORS[sky_stage]

    # Draw the sunset background and elements
    draw_sky(sky_top, sky_bottom)
    draw_sun(sun_y)
    draw_buildings(buildings)
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT - 40, WIDTH, 40))  # Draw road
    draw_car(car_x)

    # Update positions for animation
    sun_y += 0.1 if sun_y < HEIGHT else 0  # Sun descends gradually
    car_x = (car_x + car_speed) % WIDTH  # Car moves across the screen and wraps around

    # Move buildings leftward at the same speed as the car
    for building in buildings:
        building["x"] -= car_speed
        if building["x"] < -building["width"]:  # Reset building to the right once it goes off-screen
            building["x"] = WIDTH + random.randint(50, 150)
            building["height"] = random.randint(200, 400)
            building["width"] = random.randint(60, 100)

    pygame.display.flip()
    clock.tick(60)  # Maintain smooth 60 FPS

# Quit Pygame
pygame.quit()
