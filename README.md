# Dynamic Sunset Cityscape
This project is a Pygame-based animated cityscape that simulates a sunset scene with dynamic elements. It includes a transitioning sky color, a setting sun, moving buildings, and a Lamborghini-style car cruising across the scene. The animation creates a smooth and visually appealing depiction of a sunset in a bustling city.

## Features
- Gradient Sky Transition: The sky color changes through four stages, from daylight to twilight, based on the sun's position.
Setting Sun Animation: The sun gradually moves downward, simulating a sunset.
- Procedurally Generated Buildings: Buildings of random heights and widths scroll across the screen to give a dynamic, moving cityscape.
- Animated Car: A red Lamborghini-style car continuously drives across the road and wraps around the screen when it reaches the edge.
- Smooth 60 FPS Animation: The animation maintains a smooth framerate for a realistic feel.
  
## Requirements
- Python 3.x
- Pygame library
To install Pygame, run:

` bash
Copy code
pip install pygame
`

## Code Structure
### Main Components
- Sky Transition: The draw_sky function creates a gradient effect for the sky by interpolating between two colors based on the sun’s height.
- Sun Animation: The draw_sun function draws a descending sun, representing the sunset.
- Building Generation: The draw_buildings function creates buildings with randomized heights and widths, as well as organized windows.
- Car Animation: The draw_car function animates a Lamborghini-style car that moves across the screen, giving a lively touch to the scene.
  
### Key Variables
- `WIDTH, HEIGHT`: Screen dimensions.
- `SKY_COLORS`: Preset color stages for the sky as the sun descends.
- `car_speed`: Speed of the car moving across the road.

## How It Works
- Initialize Pygame and set up the display.
- Main Loop:
Event handling to allow closing the window.
Update the sun’s position and switch sky color stages based on its height.
Draw the sky, sun, buildings, road, and car in each frame.
- Animation Update: Moves buildings and car position each frame to create a continuous animation.
- Repeat until the user closes the window.

## Customization
We experimented with:

- Sky Colors: Change `SKY_COLORS` to customize the sky's color transitions.
- Car Speed: Adjust `car_speed` to change how fast the car moves.
- Building Sizes: Modify building dimensions and spacing to change the cityscape look.
