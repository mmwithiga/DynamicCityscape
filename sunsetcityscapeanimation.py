import pygame
import random

# Initialize Pygame
pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Sunset, Moonrise, and Cityscape")

# Colors
SKY_COLORS = [
    ((135, 206, 235), (176, 224, 230)),  # Daylight
    ((255, 153, 51), (255, 204, 153)),  # Sunset
    ((25, 25, 112), (0, 0, 139))        # Night
]
SUN_COLOR = (255, 140, 0)
MOON_COLOR = (200, 200, 255)
WINDOW_COLOR = (255, 223, 186)
ROAD_COLOR = (50, 50, 50)
CAR_WHEEL_COLOR = (30, 30, 30)

# Initialize buildings
buildings = [
    {
        "x": i * 150,
        "width": random.randint(60, 100),
        "height": random.randint(200, 400),
        "color": (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
    }
    for i in range(6)
]

# Initialize clouds
clouds = [
    {"x": random.randint(0, WIDTH), "y": random.randint(50, 300), "size": random.randint(50, 100)}
    for _ in range(5)
]

# Initialize cars
cars = [
    {
        "x": random.randint(-800, 800),
        "speed": random.uniform(1, 3),
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    }
    for _ in range(5)
]

# Gradient sky
def draw_sky(top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio),
            int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio),
            int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

# Draw clouds
def draw_clouds(stage):
    for cloud in clouds:
        x, y, size = cloud["x"], cloud["y"], cloud["size"]
        cloud_color = (240, 240, 240) if stage < 2 else (105, 105, 105)
        pygame.draw.ellipse(screen, cloud_color, (x, y, size, size // 2))
        pygame.draw.ellipse(screen, cloud_color, (x - size // 2, y + size // 4, size, size // 2))
        pygame.draw.ellipse(screen, cloud_color, (x + size // 2, y + size // 4, size, size // 2))

# Draw sun
def draw_sun(y):
    pygame.draw.circle(screen, SUN_COLOR, (WIDTH // 2, y), 60)

# Draw moon
def draw_moon(x, y):
    pygame.draw.circle(screen, MOON_COLOR, (x, y), 50)

# Draw buildings
def draw_buildings():
    for building in buildings:
        x, width, height, color = building["x"], building["width"], building["height"], building["color"]
        pygame.draw.rect(screen, color, (x, HEIGHT - height, width, height))
        for i in range(1, height // 40):
            for j in range(2, width // 30):
                win_x = x + j * 30
                win_y = HEIGHT - height + i * 40
                pygame.draw.rect(screen, WINDOW_COLOR, (win_x, win_y, 20, 20))

# Draw car
def draw_car(car):
    x, color = car["x"], car["color"]
    # Body
    pygame.draw.rect(screen, color, (x, HEIGHT - 80, 80, 30))
    pygame.draw.polygon(screen, color, [
        (x + 10, HEIGHT - 80),
        (x + 70, HEIGHT - 80),
        (x + 60, HEIGHT - 100),
        (x + 20, HEIGHT - 100)
    ])
    # Wheels
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x + 20, HEIGHT - 50), 10)
    pygame.draw.circle(screen, CAR_WHEEL_COLOR, (x + 60, HEIGHT - 50), 10)

# Main loop
clock = pygame.time.Clock()
sun_y = 100
moon_x, moon_y = -50, 50  # Starting position of the moon in the northwest
sky_stage = 0
moon_rising = False
new_day = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Transition sky colors
    if sun_y > HEIGHT // 2 and sky_stage < 1:
        sky_stage = 1
    elif sun_y >= HEIGHT and sky_stage < 2:
        sky_stage = 2
        moon_rising = True

    if moon_rising and moon_y > HEIGHT:
        moon_rising = False
        new_day = True  # Switch to a new day

    if new_day:
        sun_y = 100  # Reset sun position
        moon_x, moon_y = -50, 50  # Reset moon position
        sky_stage = 0  # Reset sky to daylight
        new_day = False  # Reset day cycle flag

    # Get current sky colors
    sky_top, sky_bottom = SKY_COLORS[sky_stage]

    # Draw elements
    draw_sky(sky_top, sky_bottom)
    draw_clouds(sky_stage)
    if sun_y < HEIGHT:
        draw_sun(sun_y)
    if moon_rising:
        draw_moon(moon_x, moon_y)
    draw_buildings()
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT - 40, WIDTH, 40))  # Road

    # Draw and move cars
    for car in cars:
        draw_car(car)
        car["x"] = (car["x"] + car["speed"]) % WIDTH

    # Update positions
    if sun_y < HEIGHT:
        sun_y += 0.5
    if moon_rising:
        moon_x += 1  # Move right
        moon_y += 0.5  # Move downward

    # Move clouds
    for cloud in clouds:
        cloud["x"] -= 0.5
        if cloud["x"] + cloud["size"] < 0:
            cloud["x"] = WIDTH
            cloud["y"] = random.randint(50, 300)
            cloud["size"] = random.randint(50, 100)

    # Move buildings with the car
    for building in buildings:
        building["x"] -= 1.5
        if building["x"] < -building["width"]:
            building["x"] = WIDTH + random.randint(50, 150)
            building["width"] = random.randint(60, 100)
            building["height"] = random.randint(200, 400)
            building["color"] = (
                random.randint(50, 150),
                random.randint(50, 150),
                random.randint(50, 150)
            )

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()