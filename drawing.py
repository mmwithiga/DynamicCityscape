import math
import cairo
import random

WIDTH, HEIGHT = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(surface)


# Function to draw the sun with shading and rays
def draw_sun(context, center_x, center_y, radius):
    # Draw the sun body
    context.arc(center_x, center_y, radius, 0, 2 * math.pi)
    gradient = cairo.RadialGradient(center_x - radius * 0.3, center_y - radius * 0.3, radius * 0.3,
                                    center_x, center_y, radius)
    gradient.add_color_stop_rgb(0, 1, 0.8, 0.3)  # Bright yellow center
    gradient.add_color_stop_rgb(1, 1, 0.4, 0)  # Orange edges
    context.set_source(gradient)
    context.fill()

    # Draw sun rays
    num_rays = 12
    for i in range(num_rays):
        angle = i * (2 * math.pi / num_rays)
        ray_length = radius * 1.5
        ray_width = radius * 0.1
        ray_x1 = center_x + math.cos(angle) * radius
        ray_y1 = center_y + math.sin(angle) * radius
        ray_x2 = center_x + math.cos(angle) * ray_length
        ray_y2 = center_y + math.sin(angle) * ray_length

        context.move_to(ray_x1, ray_y1)
        context.line_to(ray_x2, ray_y2)
        context.set_line_width(ray_width)
        context.set_source_rgb(1, 0.6, 0)  # Bright orange for the rays
        context.stroke()

    # Add a glare or light spot on the sun
    glare_radius = radius * 0.2
    context.arc(center_x - radius * 0.4, center_y - radius * 0.4, glare_radius, 0, 2 * math.pi)
    context.set_source_rgb(1, 1, 1)  # White for the glare
    context.fill()


# Function to draw detailed buildings with windows
def draw_building(context, x, height, width):
    context.set_source_rgb(random.random(), random.random(), random.random())  # Random color for building
    context.rectangle(x, HEIGHT - height, width, height)
    context.fill()

    # Draw windows on the building
    for i in range(3):  # 3 rows of windows
        for j in range(3):  # 3 columns of windows
            win_x = x + j * (width // 4)
            win_y = HEIGHT - height + i * (height // 5)
            context.set_source_rgb(0.8, 0.9, 1)  # Light blue for windows
            context.rectangle(win_x, win_y, width // 5, height // 6)
            context.fill()


# Function to draw a skyline with multiple buildings
def draw_cityscape(context):
    building_widths = [random.randint(20, 50) for _ in range(10)]
    building_heights = [random.randint(100, 250) for _ in range(10)]
    x_position = 0

    for i in range(10):
        draw_building(context, x_position, building_heights[i], building_widths[i])
        x_position += building_widths[i] + random.randint(5, 20)  # Space between buildings


# Function to draw streetlights and car lights
def draw_lights(context):
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT // 2, HEIGHT)  # Lights appear at the bottom half
        radius = random.randint(2, 6)
        context.set_source_rgb(1, 1, 0)  # Yellow for the lights
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.fill()


# Function to add roads at the bottom of the cityscape
def draw_roads(context):
    context.set_source_rgb(0.2, 0.2, 0.2)  # Dark gray for the road
    context.rectangle(0, HEIGHT - 80, WIDTH, 80)
    context.fill()


# Create a gradient background for the cityscape
def create_background(context):
    gradient = cairo.LinearGradient(0, 0, WIDTH, HEIGHT)
    gradient.add_color_stop_rgb(0, 0.1, 0.1, 0.3)  # Dark blue at the top
    gradient.add_color_stop_rgb(1, 0.2, 0.3, 0.4)  # Lighter blue at the bottom (dusk effect)
    context.set_source(gradient)
    context.paint()


# Function to draw stars in the sky
def draw_stars(context, num_stars):
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)  # Stars are placed in the upper half of the screen
        radius = random.randint(1, 3)  # Random small radius for the stars
        brightness = random.uniform(0.8, 1.0)  # Random brightness for stars
        context.set_source_rgb(brightness, brightness, brightness)  # White/yellow for stars
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.fill()


# Paint the background, cityscape, and sun
create_background(context)
draw_cityscape(context)
draw_roads(context)
draw_lights(context)
draw_stars(context, 200)  # Draw 200 stars in the sky
draw_sun(context, WIDTH // 2, HEIGHT // 3, 100)  # Drawing the sun at the top center

# Save the final image
output_file = "city_sun.png"
surface.write_to_png(output_file)

print("City with stars and sun created!")
