import pygame
import random
import math
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Background Music Setup
pygame.mixer.music.load("relaxing-guitar-loop-v5-245859.mp3")  # Replace with your file name
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Display setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Sunset, Moonrise, and Cityscape")

# Colors and gradients
COLORS = {
    'dawn': [(47, 53, 84), (242, 190, 138), (255, 183, 107)],
    'early_morning': [(135, 206, 235), (200, 200, 255), (255, 200, 150)],
    'day': [(135, 206, 235), (157, 217, 245), (255, 255, 255)],
    'pre_sunset': [(255, 166, 89), (255, 121, 98), (255, 175, 123)],
    'sunset': [(44, 58, 121), (255, 89, 89), (255, 121, 98)],
    'dusk': [(20, 24, 82), (44, 58, 121), (255, 89, 89)],
    'night': [(0, 0, 20), (20, 24, 82), (30, 34, 95)]
}


# Star system
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT//2), random.random()*0.8 + 0.2) 
         for _ in range(200)]

class Building:
    def __init__(self, x, layer):
        self.layer = layer
        self.speed = 1.5  # Match original speed
        self.is_clock_tower = random.random() < 0.05  # 5% chance to be a clock tower
        
        if self.is_clock_tower and layer == 0:  # Only front layer can be clock tower
            self.width = 80
            self.height = 450
            self.clock_radius = 25
            self.top_height = 70  # Height of the tower top
            self.color = (70, 70, 90)
            self.x = x + random.randint(100, 200)
        else:
            self.width = random.randint(60, 100) // (layer + 1)
            self.height = random.randint(200, 400) // (layer + 1)
            self.x = x
            self.color = (
                random.randint(20, 40),
                random.randint(20, 40),
                random.randint(30, 50)
            )
            self.is_clock_tower = False  # Force non-clock tower if not in front layer
        
        self.windows = []
        self.generate_windows()

    def generate_windows(self):
        window_rows = self.height // 30
        window_cols = self.width // 25
        for row in range(window_rows):
            for col in range(window_cols):
                if random.random() < 0.8:  # 80% chance for a window
                    self.windows.append({
                        'x': col * 25 + 5,
                        'y': row * 30 + 5,
                        'lit': random.random() < 0.3,
                        'blink_timer': random.randint(0, 100)
                    })

    def draw_clock(self, screen, time_of_day):
        # Move clock to the very top of the tower
        clock_x = self.x + self.width // 2
        clock_y = HEIGHT - self.height - self.top_height + 35  # Position at top
        
        # Draw clock frame
        frame_color = (60, 60, 80)
        pygame.draw.circle(screen, frame_color, (clock_x, clock_y), self.clock_radius + 5)
        pygame.draw.circle(screen, (240, 240, 240), (clock_x, clock_y), self.clock_radius)
        
        # Draw hour markers
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            start = (clock_x + math.cos(angle) * (self.clock_radius - 5),
                    clock_y + math.sin(angle) * (self.clock_radius - 5))
            end = (clock_x + math.cos(angle) * self.clock_radius,
                  clock_y + math.sin(angle) * self.clock_radius)
            pygame.draw.line(screen, (0, 0, 0), start, end, 2)
        
        # Calculate realistic time based on day/night cycle
        # Map time_of_day to real 24-hour clock
        # 0.0 = midnight, 0.25 = 6AM, 0.5 = noon, 0.75 = 6PM
        hours = (time_of_day * 24) % 24
        minutes = (time_of_day * 24 * 60) % 60
        
        # Hour hand
        hour_angle = math.radians((hours % 12) * 30 - 90 + minutes / 60 * 30)
        hour_length = self.clock_radius * 0.6
        hour_end = (clock_x + math.cos(hour_angle) * hour_length,
                   clock_y + math.sin(hour_angle) * hour_length)
        pygame.draw.line(screen, (0, 0, 0), (clock_x, clock_y), hour_end, 4)
        
        # Minute hand
        min_angle = math.radians(minutes * 6 - 90)
        min_length = self.clock_radius * 0.8
        min_end = (clock_x + math.cos(min_angle) * min_length,
                  clock_y + math.sin(min_angle) * min_length)
        pygame.draw.line(screen, (0, 0, 0), (clock_x, clock_y), min_end, 3)
        
        # Center dot
        pygame.draw.circle(screen, (0, 0, 0), (clock_x, clock_y), 4)

    def draw(self, screen, time_of_day):
        if self.is_clock_tower:
            # Draw base building first
            building_rect = pygame.Rect(self.x, HEIGHT - self.height, self.width, self.height)
            pygame.draw.rect(screen, self.color, building_rect)
            
            # Draw tower top
            pygame.draw.polygon(screen, self.color, [
                (self.x, HEIGHT - self.height),
                (self.x + self.width, HEIGHT - self.height),
                (self.x + self.width//2, HEIGHT - self.height - self.top_height)
            ])
            
            # Draw clock at the very top
            self.draw_clock(screen, time_of_day)
            
            # Draw ornamental details
            detail_color = (min(self.color[0] + 15, 255),
                          min(self.color[1] + 15, 255),
                          min(self.color[2] + 15, 255))
            
            # Vertical pillars
            pillar_width = 8
            pygame.draw.rect(screen, detail_color,
                           (self.x, HEIGHT - self.height, pillar_width, self.height))
            pygame.draw.rect(screen, detail_color,
                           (self.x + self.width - pillar_width, HEIGHT - self.height, 
                            pillar_width, self.height))
            
            # Add decorative window below clock
            window_y = HEIGHT - self.height - self.top_height + 70  # Position below clock
            pygame.draw.rect(screen, (255, 223, 186), 
                           (self.x + self.width//4, window_y, 
                            self.width//2, 40))  # Decorative window
            
            # Draw ornamental details
            detail_color = (min(self.color[0] + 15, 255),
                          min(self.color[1] + 15, 255),
                          min(self.color[2] + 15, 255))
            
            # Vertical pillars
            pillar_width = 8
            pygame.draw.rect(screen, detail_color,
                           (self.x, HEIGHT - self.height, pillar_width, self.height))
            pygame.draw.rect(screen, detail_color,
                           (self.x + self.width - pillar_width, HEIGHT - self.height, 
                            pillar_width, self.height))
            
            # Add decorative window below clock
            window_y = HEIGHT - self.height - self.top_height + 70  # Position below clock
            pygame.draw.rect(screen, (255, 223, 186), 
                           (self.x + self.width//4, window_y, 
                            self.width//2, 40))  # Decorative window
            
        else:
            # Draw regular building
            building_rect = pygame.Rect(self.x, HEIGHT - self.height, self.width, self.height)
            pygame.draw.rect(screen, self.color, building_rect)
        
        # Draw windows (avoiding clock area for clock tower)
        for window in self.windows:
            if time_of_day > 0.7:  # Night time
                if window['blink_timer'] == 0:
                    window['lit'] = random.random() < 0.8
                    window['blink_timer'] = random.randint(50, 200)
                window['blink_timer'] -= 1
                window_color = (255, 223, 186) if window['lit'] else (50, 50, 60)
            else:
                window_color = (255, 223, 186)
            
            # Don't draw windows in clock area for clock tower
            if not (self.is_clock_tower and 
                   70 < window['y'] < 130):  # Adjusted clock area clearance
                pygame.draw.rect(screen, window_color, (
                    self.x + window['x'],
                    HEIGHT - self.height + window['y'],
                    15, 20
                ))

class Cloud:
    def __init__(self):
        self.x = random.randint(-100, WIDTH + 100)
        self.y = random.randint(50, HEIGHT//3)
        self.speed = 0.5  # Keep this moderate speed
        self.size = random.randint(50, 150)
        self.opacity = random.randint(150, 255)

    def draw(self, screen, time_of_day):
        # Adjust cloud color based on time of day
        base_color = (255, 255, 255) if time_of_day < 0.7 else (150, 150, 150)
        cloud_color = (*base_color, self.opacity)
        
        cloud_surface = pygame.Surface((self.size * 2, self.size), pygame.SRCALPHA)
        pygame.draw.ellipse(cloud_surface, cloud_color, (0, 0, self.size, self.size))
        pygame.draw.ellipse(cloud_surface, cloud_color, (self.size * 0.5, 0, self.size, self.size))
        pygame.draw.ellipse(cloud_surface, cloud_color, (self.size * 0.8, -self.size * 0.2, self.size, self.size))
        screen.blit(cloud_surface, (self.x, self.y))

class Car:
    def __init__(self, direction=1):
        self.direction = direction  # 1: right, -1: left
        self.speed = random.uniform(2, 4) * direction  # More moderate speed range
        self.x = -100 if direction == 1 else WIDTH + 100
        self.y = HEIGHT - 80 if direction == 1 else HEIGHT - 120
        self.color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
        self.length = random.randint(40, 60)

    def draw(self, screen):
        # Car body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 20))
        pygame.draw.rect(screen, self.color, (self.x + 10, self.y - 15, self.length - 20, 15))
        
        # Wheels
        wheel_color = (30, 30, 30)
        pygame.draw.circle(screen, wheel_color, (self.x + 10, self.y + 20), 8)
        pygame.draw.circle(screen, wheel_color, (self.x + self.length - 10, self.y + 20), 8)
        
        # Lights
        if self.direction == 1:
            light_color = (255, 255, 200)
            pygame.draw.circle(screen, light_color, (self.x + self.length, self.y + 10), 5)
        else:
            light_color = (255, 0, 0)
            pygame.draw.circle(screen, light_color, (self.x, self.y + 10), 5)

class Sun:
    def __init__(self):
        self.radius = 40
        self.x = WIDTH // 2
        self.y = 100
        self.flare_colors = [
            (255, 255, 0),
            (255, 200, 0),
            (255, 150, 0),
            (255, 100, 0)
        ]

    def draw(self, screen, time_of_day):
        # Calculate sun position
        self.y = -self.radius + (HEIGHT + 2 * self.radius) * time_of_day
        
        # Draw solar flares
        flare_intensity = 1.0 - abs(time_of_day - 0.5) * 2  # Strongest at noon
        if time_of_day < 0.8:  # Only draw sun during day/sunset
            for i in range(12):  # Draw 12 flares
                angle = i * (2 * math.pi / 12) + pygame.time.get_ticks() * 0.0005
                flare_length = self.radius * (0.5 + 0.2 * math.sin(pygame.time.get_ticks() * 0.005 + i))
                end_x = self.x + math.cos(angle) * (self.radius + flare_length)
                end_y = self.y + math.sin(angle) * (self.radius + flare_length)
                
                # Create gradient flare effect
                for c, color in enumerate(self.flare_colors):
                    alpha = int(255 * flare_intensity * (1 - c/len(self.flare_colors)))
                    flare_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.line(flare_surface, (*color, alpha), 
                                   (self.x, self.y), (end_x, end_y), 
                                   3 - c)
                    screen.blit(flare_surface, (0, 0))
            
            # Draw main sun body with gradient
            for i in range(self.radius, 0, -1):
                alpha = int(255 * flare_intensity)
                color = (255, 
                        max(100, int(204 * (i/self.radius))), 
                        max(0, int(100 * (i/self.radius))))
                pygame.draw.circle(screen, (*color, alpha), 
                                 (int(self.x), int(self.y)), i)

class Moon:
    def __init__(self):
        self.radius = 40
        self.color = (245, 245, 255)  # Brighter white
        self.crescent_offset = 12
        self.x = -100
        self.y = 100
        self.opacity = 0
        self.glow_radius = 60

    def draw(self, screen, time_of_day):
        # Slower, smoother moon transitions
        if 0.8 < time_of_day < 1.0:  # Moon rising
            progress = (time_of_day - 0.8) * 2.5  # Slower rise (was 5)
            self.opacity = int(255 * min(1.0, progress * 1.5))  # Smoother fade in
            self.x = -50 + (WIDTH//3) * progress  # More gradual movement
            self.y = 150 - 50 * progress
        elif 0.0 <= time_of_day < 0.2:  # Moon setting
            progress = 1 - (time_of_day * 2.5)  # Slower set (was 5)
            self.opacity = int(255 * min(1.0, progress * 1.5))  # Smoother fade out
            self.x = WIDTH//3 + (WIDTH//3) * (1 - progress)
            self.y = 100 + 50 * (1 - progress)
        elif time_of_day >= 0.2:  # Moon hidden during day
            self.opacity = 0
        
        if self.opacity > 0:
            # Create surface for moon with transparency
            moon_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            
            # Draw main moon circle
            pygame.draw.circle(moon_surface, (*self.color, self.opacity), 
                             (self.radius, self.radius), self.radius)
            
            # Draw darker circle offset to create crescent
            shadow_color = (20, 24, 82, self.opacity)
            pygame.draw.circle(moon_surface, shadow_color,
                             (self.radius + self.crescent_offset, self.radius), 
                             self.radius)
            
            # Add subtle glow effect
            glow_radius = self.radius + 10
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            for r in range(10):
                glow_opacity = int((10-r) * self.opacity * 0.1)
                pygame.draw.circle(glow_surface, (*self.color, glow_opacity),
                                 (glow_radius, glow_radius), 
                                 self.radius + r)
            
            # Draw both surfaces to screen
            screen.blit(glow_surface, 
                       (self.x - glow_radius, self.y - glow_radius))
            screen.blit(moon_surface, 
                       (self.x - self.radius, self.y - self.radius))

def get_sky_color(time_of_day):
    if time_of_day < 0.2:  # Dawn
        colors = COLORS['dawn']
    elif time_of_day < 0.3:  # Early morning
        colors = COLORS['early_morning']
    elif time_of_day < 0.6:  # Day
        colors = COLORS['day']
    elif time_of_day < 0.7:  # Pre-sunset
        colors = COLORS['pre_sunset']
    elif time_of_day < 0.8:  # Sunset
        colors = COLORS['sunset']
    elif time_of_day < 0.9:  # Dusk
        colors = COLORS['dusk']
    else:  # Night
        colors = COLORS['night']
    return colors

def draw_sky(screen, time_of_day):
    colors = get_sky_color(time_of_day)
    
    # Create smooth gradient with adaptive colors
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        # Calculate sun influence on sky color
        sun_influence = max(0, 1 - abs(time_of_day - 0.5) * 2)  # Strongest at noon
        
        # Blend colors based on time of day and sun position
        if time_of_day > 0.6 and time_of_day < 0.8:  # Sunset period
            r = int(colors[0][0] * (1 - ratio) + colors[2][0] * ratio + sun_influence * 50)
            g = int(colors[0][1] * (1 - ratio) + colors[2][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[2][2] * ratio)
        else:
            r = int(colors[0][0] * (1 - ratio) + colors[2][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[2][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[2][2] * ratio)
        
        pygame.draw.line(screen, (min(255, r), min(255, g), min(255, b)), (0, y), (WIDTH, y))

class AROverlay:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.weather_icons = {
            'sun': '☀',
            'moon': '☾',
            'cloud': '☁'
        }
        
    def draw_overlay(self, screen, time_of_day, temperature):
        # Draw time overlay
        hours = int((time_of_day * 24) % 24)
        minutes = int((time_of_day * 24 * 60) % 60)
        time_text = f"{hours:02d}:{minutes:02d}"
        
        # Temperature varies with time of day
        temp = temperature + math.sin(time_of_day * math.pi * 2) * 5
        
        # Weather icon based on time
        icon = self.weather_icons['sun'] if 0.3 < time_of_day < 0.7 else \
               self.weather_icons['moon'] if time_of_day > 0.8 or time_of_day < 0.2 else \
               self.weather_icons['cloud']
        
        # Draw overlays
        self.draw_text(screen, f"Time: {time_text}", (10, 10))
        self.draw_text(screen, f"Temp: {temp:.1f}°C", (10, 50))
        self.draw_text(screen, f"Weather: {icon}", (10, 90))
    
    def draw_text(self, screen, text, pos):
        text_surface = self.font.render(text, True, (255, 255, 255))
        shadow_surface = self.font.render(text, True, (0, 0, 0))
        screen.blit(shadow_surface, (pos[0] + 2, pos[1] + 2))
        screen.blit(text_surface, pos)

class LightSource:
    def __init__(self):
        self.radius = 40
        self.color = (255, 200, 100)
        self.x = WIDTH // 2
        self.y = 100

    def cast_dynamic_shadows(self, screen, buildings, time_of_day):
        if 0.3 < time_of_day < 0.7:  # Daytime shadows
            shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            sun_angle = (time_of_day - 0.3) * math.pi  # Sun movement angle
            shadow_length = 100 + abs(math.sin(sun_angle)) * 150
            
            for building in buildings:
                shadow_points = [
                    (building.x, HEIGHT - building.height),
                    (building.x + building.width, HEIGHT - building.height),
                    (building.x + building.width + shadow_length, HEIGHT),
                    (building.x + shadow_length, HEIGHT)
                ]
                pygame.draw.polygon(shadow_surface, (0, 0, 0, 40), shadow_points)
            
            screen.blit(shadow_surface, (0, 0))

class InteractiveElements:
    def __init__(self):
        self.particles = []
        self.last_mouse_pos = None
        
    def update(self, screen, mouse_pos):
        if self.last_mouse_pos:
            # Create trail effect
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
            if abs(dx) > 0 or abs(dy) > 0:
                self.particles.append({
                    'pos': list(mouse_pos),
                    'vel': [dx*0.1, dy*0.1],
                    'life': 1.0,
                    'color': (255, 255, 200)
                })
        
        # Update particles
        new_particles = []
        for p in self.particles:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['life'] -= 0.02
            
            if p['life'] > 0:
                alpha = int(255 * p['life'])
                color = (*p['color'], alpha)
                pygame.draw.circle(screen, color, 
                                 (int(p['pos'][0]), int(p['pos'][1])), 
                                 int(3 * p['life']))
                new_particles.append(p)
        
        self.particles = new_particles
        self.last_mouse_pos = mouse_pos

class EnhancedAROverlay:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.icons = {'sun': '☀', 'moon': '☾', 'cloud': '☁'}
        self.notifications = []
        
    def draw_text(self, screen, text, pos, alpha=255):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_surface.set_alpha(alpha)
        shadow_surface = self.font.render(text, True, (0, 0, 0))
        shadow_surface.set_alpha(alpha)
        screen.blit(shadow_surface, (pos[0] + 2, pos[1] + 2))
        screen.blit(text_surface, pos)
        
    def add_notification(self, text, duration=2.0):
        self.notifications.append({
            'text': text,
            'life': duration,
            'y': len(self.notifications) * 40 + 130
        })
    
    def draw_overlay(self, screen, time_of_day, temperature):
        # Existing time and weather display
        hours = int((time_of_day * 24) % 24)
        minutes = int((time_of_day * 24 * 60) % 60)
        
        # Dynamic temperature based on time
        temp = temperature + math.sin(time_of_day * math.pi * 2) * 5
        
        # Weather conditions
        conditions = []
        if 0.3 < time_of_day < 0.7:
            conditions.append("Clear Skies")
        elif time_of_day > 0.8 or time_of_day < 0.2:
            conditions.append("Night")
        
        # Draw basic info
        self.draw_text(screen, f"{hours:02d}:{minutes:02d}", (10, 10))
        self.draw_text(screen, f"{temp:.1f}°C", (10, 50))
        self.draw_text(screen, f"{' | '.join(conditions)}", (10, 90))
        
        # Update and draw notifications
        new_notifications = []
        for notif in self.notifications:
            if notif['life'] > 0:
                alpha = min(255, int(notif['life'] * 255))
                self.draw_text(screen, notif['text'], (10, notif['y']), 
                             alpha=alpha)
                notif['life'] -= 0.016
                new_notifications.append(notif)
        self.notifications = new_notifications

class ShootingStar:
    def __init__(self):
        self.reset()
        self.active = False
    
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT//3)
        self.speed = random.uniform(15, 25)
        self.angle = random.uniform(math.pi/6, math.pi/3)  # 30-60 degrees
        self.length = random.randint(20, 40)
        self.life = 1.0
    
    def update_and_draw(self, screen):
        if self.active:
            # Create trail effect
            trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(self.length):
                alpha = int(255 * self.life * (1 - i/self.length))
                pos = (int(self.x - i * math.cos(self.angle)), 
                      int(self.y + i * math.sin(self.angle)))
                pygame.draw.circle(trail_surface, (255, 255, 255, alpha), pos, 1)
            screen.blit(trail_surface, (0, 0))
            
            # Update position
            self.x += self.speed * math.cos(self.angle)
            self.y -= self.speed * math.sin(self.angle)
            self.life -= 0.02
            
            if self.life <= 0 or self.x > WIDTH or self.y < 0:
                self.active = False

def main():
    clock = pygame.time.Clock()
    time_of_day = 0.3  # Start at morning
    
    # Initialize objects (remove duplicates)
    sun = Sun()
    moon = Moon()
    buildings = []
    for layer in range(3):
        x = -200
        while x < WIDTH + 200:
            building = Building(x, layer)
            buildings.append(building)
            x += building.width + (50 if building.is_clock_tower else 20)
    
    clouds = [Cloud() for _ in range(10)]
    cars = [Car(direction=1 if random.random() < 0.5 else -1) for _ in range(8)]
    light_source = LightSource()
    interactive = InteractiveElements()
    ar_overlay = EnhancedAROverlay()  # Use only EnhancedAROverlay
    base_temperature = 20
    shooting_stars = [ShootingStar() for _ in range(3)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Slower progression during night and transitions
        if 0.7 <= time_of_day <= 0.8:  # Sunset transition
            time_of_day = (time_of_day + 0.0005) % 1.0  # Slower sunset
        elif 0.8 < time_of_day < 0.2:  # Night time
            time_of_day = (time_of_day + 0.0003) % 1.0  # Much slower at night
        elif 0.2 <= time_of_day <= 0.3:  # Sunrise transition
            time_of_day = (time_of_day + 0.0005) % 1.0  # Slower sunrise
        else:  # Day time
            time_of_day = (time_of_day + 0.001) % 1.0  # Normal speed during day

        # Draw sky
        draw_sky(screen, time_of_day)
        
        # Draw sun
        sun.draw(screen, time_of_day)

        # Draw stars during night
        if time_of_day > 0.8 or time_of_day < 0.2:
            for star in stars:
                brightness = int(255 * star[2] * (math.sin(pygame.time.get_ticks() * 0.001 + star[0]) * 0.3 + 0.7))
                pygame.draw.circle(screen, (brightness, brightness, brightness), (star[0], star[1]), 1)
        
        # Draw moon (before clouds and buildings)
        moon.draw(screen, time_of_day)
        
        # Draw and update clouds
        for cloud in clouds:
            cloud.x += cloud.speed
            if cloud.x > WIDTH + 100:
                cloud.x = -200
                cloud.y = random.randint(50, HEIGHT//3)
            cloud.draw(screen, time_of_day)

        # Draw buildings with constant speed (no time multiplier)
        for layer in range(2, -1, -1):
            layer_buildings = [b for b in buildings if b.layer == layer]
            for building in layer_buildings:
                building.x -= building.speed  # No time multiplier
                if building.x < -building.width:
                    building.x = WIDTH + random.randint(50, 150)
                building.draw(screen, time_of_day)

        # Draw road
        pygame.draw.rect(screen, (40, 40, 40), (0, HEIGHT - 150, WIDTH, 150))
        pygame.draw.rect(screen, (255, 255, 0), (0, HEIGHT - 85, WIDTH, 5))
        
        # Update and draw cars with constant speed (no time multiplier)
        for car in cars:
            car.x += car.speed  # No time multiplier
            if car.direction == 1 and car.x > WIDTH + 100:
                car.x = -200
            elif car.direction == -1 and car.x < -200:
                car.x = WIDTH + 100
            car.draw(screen)

        # Add new features
        light_source.cast_dynamic_shadows(screen, buildings, time_of_day)
        mouse_pos = pygame.mouse.get_pos()
        interactive.update(screen, mouse_pos)
        ar_overlay.draw_overlay(screen, time_of_day, base_temperature)

        # Handle shooting stars during night
        if time_of_day > 0.8 or time_of_day < 0.2:
            for star in shooting_stars:
                if not star.active and random.random() < 0.005:  # Small chance to activate
                    star.reset()
                    star.active = True
                if star.active:
                    star.update_and_draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()