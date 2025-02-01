import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeepSeek Oracle's Spinning Hexagon with Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Hexagon properties
HEX_RADIUS = 200
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_ANGLE = 0  # Initial rotation angle
HEX_ROTATION_SPEED = 0.01  # Rotation speed in radians per frame

# Ball properties
BALL_RADIUS = 20
ball_pos = [HEX_CENTER[0], HEX_CENTER[1] - HEX_RADIUS + BALL_RADIUS]
ball_vel = [2, 0]  # Initial velocity
GRAVITY = 0.1
FRICTION = 0.99

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(angle + i * math.pi / 3)
        y = center[1] + radius * math.sin(angle + i * math.pi / 3)
        vertices.append((x, y))
    return vertices

# Function to check if ball collides with hexagon walls
def check_collision(ball_pos, ball_vel, hex_vertices):
    for i in range(len(hex_vertices)):
        x1, y1 = hex_vertices[i]
        x2, y2 = hex_vertices[(i + 1) % len(hex_vertices)]
        
        # Calculate the normal vector of the wall
        wall_vector = (x2 - x1, y2 - y1)
        normal_vector = (-wall_vector[1], wall_vector[0])
        normal_length = math.hypot(normal_vector[0], normal_vector[1])
        normal_vector = (normal_vector[0] / normal_length, normal_vector[1] / normal_length)
        
        # Calculate the ball's position relative to the wall
        relative_pos = (ball_pos[0] - x1, ball_pos[1] - y1)
        
        # Dot product to check if ball is on the correct side of the wall
        dot_product = relative_pos[0] * normal_vector[0] + relative_pos[1] * normal_vector[1]
        
        if dot_product < BALL_RADIUS:
            # Reflect the ball's velocity
            ball_vel[0] -= 2 * dot_product * normal_vector[0]
            ball_vel[1] -= 2 * dot_product * normal_vector[1]
            ball_pos[0] += (BALL_RADIUS - dot_product) * normal_vector[0]
            ball_pos[1] += (BALL_RADIUS - dot_product) * normal_vector[1]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    HEX_ANGLE += HEX_ROTATION_SPEED
    hex_vertices = calculate_hexagon_vertices(HEX_CENTER, HEX_RADIUS, HEX_ANGLE)

    # Update ball position and velocity
    ball_vel[1] += GRAVITY  # Apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_vel[0] *= FRICTION  # Apply friction
    ball_vel[1] *= FRICTION

    # Check for collisions with hexagon walls
    check_collision(ball_pos, ball_vel, hex_vertices)

    # Clear screen
    screen.fill(BLACK)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_vertices, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
