
import math
import random
import sys
import colorsys

import pygame


# ============================================================
# NEBULA — COSMIC PARTICLE EXPERIENCE
# Interactive particle animation built with Python + Pygame
# ============================================================

pygame.init()

WIDTH = 1100
HEIGHT = 700
FPS = 60

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEBULA | Cosmic Particle Experience")

clock = pygame.time.Clock()

# Font
FONT_SMALL = pygame.font.SysFont("consolas", 13)
FONT_MEDIUM = pygame.font.SysFont("consolas", 17)
FONT_TITLE = pygame.font.SysFont("consolas", 25, bold=True)

# Colors
BLACK = (5, 7, 18)
WHITE = (235, 245, 255)
CYAN = (70, 225, 255)
PURPLE = (170, 90, 255)
BLUE = (65, 115, 255)

# Transparent surface for glowing effects
glow_layer = pygame.Surface(
    (WIDTH, HEIGHT),
    pygame.SRCALPHA
)

# Background
background = pygame.Surface((WIDTH, HEIGHT))

for y in range(HEIGHT):
    amount = y / HEIGHT

    color = (
        int(5 + amount * 5),
        int(7 + amount * 3),
        int(18 + amount * 17)
    )

    pygame.draw.line(
        background,
        color,
        (0, y),
        (WIDTH, y)
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_glow(surface, x, y, radius, color, intensity=1.0):
    """
    Draw a soft glow using several transparent circles.
    """
    if radius <= 0:
        return

    x = int(x)
    y = int(y)

    if not (-radius <= x <= WIDTH + radius):
        return

    if not (-radius <= y <= HEIGHT + radius):
        return

    layers = (
        (3.0, 0.035),
        (2.2, 0.055),
        (1.5, 0.085),
        (1.0, 0.18),
    )

    for scale, alpha_factor in layers:
        current_radius = max(1, int(radius * scale))

        alpha = int(
            clamp(intensity * alpha_factor * 255, 0, 255)
        )

        pygame.draw.circle(
            surface,
            (*color, alpha),
            (x, y),
            current_radius
        )


def hsv_color(hue, saturation=0.8, value=1.0):
    """
    Convert HSV color values into RGB.
    """
    rgb = colorsys.hsv_to_rgb(
        hue % 1.0,
        saturation,
        value
    )

    return tuple(int(component * 255) for component in rgb)


# ============================================================
# BACKGROUND STARS
# ============================================================

class Star:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        self.radius = random.choice([1, 1, 1, 2])

        self.phase = random.uniform(0, math.tau)
        self.speed = random.uniform(0.8, 2.5)

    def update(self, dt, elapsed):
        self.phase += self.speed * dt

    def draw(self, surface, elapsed):
        brightness = (
            0.45
            + 0.55 * math.sin(self.phase + elapsed)
        )

        brightness = max(0.12, brightness)

        color = (
            int(100 * brightness),
            int(165 * brightness),
            int(230 * brightness)
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            self.radius
        )


stars = [Star() for _ in range(170)]


# ============================================================
# NEBULA PARTICLES
# ============================================================

class Particle:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, math.tau)

        distance = random.uniform(65, 330)

        self.angle = angle
        self.distance = distance

        self.speed = random.uniform(0.15, 0.75)

        self.orbit_size = random.uniform(0.5, 1.7)

        self.size = random.uniform(1.0, 3.0)

        self.hue = random.uniform(0.48, 0.82)

        self.phase = random.uniform(0, math.tau)

        self.drift = random.uniform(0.2, 1.0)

    def update(self, dt, elapsed, mouse_pos):
        self.angle += self.speed * dt

        self.phase += dt * self.drift

        # Particles breathe gently.
        breathing = math.sin(self.phase) * 7

        distance = self.distance + breathing

        self.x = (
            CENTER_X
            + math.cos(self.angle) * distance
        )

        self.y = (
            CENTER_Y
            + math.sin(self.angle) * distance * 0.65
        )

        # Mouse interaction: particles are gently displaced.
        if mouse_pos is not None:
            mx, my = mouse_pos

            dx = self.x - mx
            dy = self.y - my

            distance_to_mouse = math.hypot(dx, dy)

            if 0 < distance_to_mouse < 100:
                force = (100 - distance_to_mouse) / 100

                self.x += dx / distance_to_mouse * force * 18
                self.y += dy / distance_to_mouse * force * 18

    def draw(self, surface, glow_surface, elapsed):
        hue = self.hue + math.sin(self.phase) * 0.025

        color = hsv_color(hue, 0.75, 1.0)

        pulse = (
            0.6
            + 0.4 * math.sin(self.phase * 2)
        )

        radius = max(
            1,
            int(self.size * pulse)
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            radius
        )

        if radius >= 2:
            draw_glow(
                glow_surface,
                self.x,
                self.y,
                radius,
                color,
                0.55
            )


particles = [Particle() for _ in range(260)]


# ============================================================
# PARTICLE BURSTS
# ============================================================

class BurstParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.tau)

        speed = random.uniform(90, 430)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.uniform(0.65, 1.45)
        self.max_life = self.life

        self.size = random.uniform(1.5, 4.0)

        self.hue = random.uniform(0.45, 0.88)

    def update(self, dt):
        self.life -= dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Slow down naturally.
        damping = math.exp(-1.3 * dt)

        self.vx *= damping
        self.vy *= damping

        # A little gravity creates a natural movement.
        self.vy += 25 * dt

    def draw(self, surface, glow_surface):
        if self.life <= 0:
            return

        fade = self.life / self.max_life

        color = hsv_color(
            self.hue,
            0.65,
            clamp(fade * 1.2, 0.0, 1.0)
        )

        radius = max(
            1,
            int(self.size * fade)
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            radius
        )

        draw_glow(
            glow_surface,
            self.x,
            self.y,
            radius,
            color,
            fade * 0.7
        )


burst_particles = []


def create_burst(x, y, amount=65):
    """
    Create an explosion of particles at a given position.
    """
    for _ in range(amount):
        burst_particles.append(
            BurstParticle(x, y)
        )


# ============================================================
# MOUSE TRAIL
# ============================================================

class TrailPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.life = 0.45
        self.max_life = self.life

        self.size = random.uniform(2, 5)

        self.hue = random.uniform(0.48, 0.82)

    def update(self, dt):
        self.life -= dt

    def draw(self, surface, glow_surface):
        if self.life <= 0:
            return

        fade = self.life / self.max_life

        color = hsv_color(
            self.hue,
            0.65,
            fade
        )

        radius = max(
            1,
            int(self.size * fade)
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            radius
        )

        draw_glow(
            glow_surface,
            self.x,
            self.y,
            radius,
            color,
            fade * 0.8
        )


mouse_trail = []


# ============================================================
# ENERGY CORE
# ============================================================

def draw_energy_core(surface, glow_surface, elapsed):
    pulse = (
        1.0
        + 0.08 * math.sin(elapsed * 2.4)
    )

    core_radius = int(24 * pulse)

    # Outer atmospheric glow.
    draw_glow(
        glow_surface,
        CENTER_X,
        CENTER_Y,
        22 * pulse,
        CYAN,
        1.0
    )

    draw_glow(
        glow_surface,
        CENTER_X,
        CENTER_Y,
        13 * pulse,
        PURPLE,
        0.8
    )

    # Rotating rings.
    for index in range(4):
        angle = elapsed * (0.45 + index * 0.16)

        rx = 45 + index * 15
        ry = 19 + index * 8

        points = []

        for step in range(100):
            theta = step / 100 * math.tau

            px = math.cos(theta) * rx
            py = math.sin(theta) * ry

            rotated_x = (
                px * math.cos(angle)
                - py * math.sin(angle)
            )

            rotated_y = (
                px * math.sin(angle)
                + py * math.cos(angle)
            )

            points.append(
                (
                    int(CENTER_X + rotated_x),
                    int(CENTER_Y + rotated_y)
                )
            )

        color = (
            CYAN
            if index % 2 == 0
            else PURPLE
        )

        pygame.draw.aalines(
            surface,
            color,
            True,
            points
        )

        # Moving light along each ring.
        marker_angle = elapsed * (1.2 + index * 0.25)

        marker_x = (
            CENTER_X
            + math.cos(marker_angle) * rx
        )

        marker_y = (
            CENTER_Y
            + math.sin(marker_angle) * ry
        )

        draw_glow(
            glow_surface,
            marker_x,
            marker_y,
            4,
            color,
            1.0
        )

        pygame.draw.circle(
            surface,
            WHITE,
            (int(marker_x), int(marker_y)),
            2
        )

    # The center is made of several luminous layers.
    pygame.draw.circle(
        surface,
        (25, 45, 90),
        (CENTER_X, CENTER_Y),
        core_radius + 5
    )

    pygame.draw.circle(
        surface,
        (80, 210, 255),
        (CENTER_X, CENTER_Y),
        core_radius
    )

    pygame.draw.circle(
        surface,
        (190, 245, 255),
        (CENTER_X, CENTER_Y),
        int(core_radius * 0.55)
    )

    pygame.draw.circle(
        surface,
        WHITE,
        (CENTER_X, CENTER_Y),
        5
    )


# ============================================================
# INTERFACE
# ============================================================

def draw_interface(surface, elapsed):
    # Small title.
    title = FONT_TITLE.render(
        "N E B U L A",
        True,
        (155, 220, 255)
    )

    surface.blit(
        title,
        (28, 25)
    )

    subtitle = FONT_SMALL.render(
        "COSMIC PARTICLE EXPERIENCE",
        True,
        (100, 135, 175)
    )

    surface.blit(
        subtitle,
        (30, 58)
    )

    # Animated status indicator.
    pulse = 150 + int(
        70 * math.sin(elapsed * 3)
    )

    pygame.draw.circle(
        surface,
        (70, pulse, 255),
        (WIDTH - 32, 35),
        4
    )

    status = FONT_SMALL.render(
        "SYSTEM ACTIVE",
        True,
        (125, 175, 210)
    )

    surface.blit(
        status,
        (WIDTH - 150, 28)
    )

    # Instructions.
    instructions = [
        "CLICK       - ENERGY EXPLOSION",
        "MOVE MOUSE  - DISTURB PARTICLES",
        "SPACE       - RANDOM BURST",
        "R           - RESET PARTICLES",
        "ESC         - EXIT"
    ]

    y = HEIGHT - 125

    for line in instructions:
        text = FONT_SMALL.render(
            line,
            True,
            (105, 135, 175)
        )

        surface.blit(
            text,
            (28, y)
        )

        y += 19

    # Small decorative line.
    pygame.draw.line(
        surface,
        (35, 65, 100),
        (28, HEIGHT - 22),
        (210, HEIGHT - 22),
        1
    )


# ============================================================
# MAIN LOOP
# ============================================================

def main():
    global mouse_trail

    running = True

    elapsed = 0.0

    mouse_pos = None

    # Start with a subtle burst.
    create_burst(
        CENTER_X,
        CENTER_Y,
        45
    )

    while running:
        dt = min(
            clock.tick(FPS) / 1000.0,
            0.033
        )

        elapsed += dt

        # ----------------------------------------------------
        # EVENTS
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    x = random.randint(150, WIDTH - 150)
                    y = random.randint(100, HEIGHT - 100)

                    create_burst(x, y, 85)

                elif event.key == pygame.K_r:
                    particles.clear()

                    particles.extend(
                        Particle()
                        for _ in range(260)
                    )

                    burst_particles.clear()
                    mouse_trail.clear()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    create_burst(
                        event.pos[0],
                        event.pos[1],
                        75
                    )

                elif event.button == 3:
                    create_burst(
                        event.pos[0],
                        event.pos[1],
                        130
                    )

        mouse_pos = pygame.mouse.get_pos()

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        for star in stars:
            star.update(dt, elapsed)

        for particle in particles:
            particle.update(
                dt,
                elapsed,
                mouse_pos
            )

        for particle in burst_particles[:]:
            particle.update(dt)

            if particle.life <= 0:
                burst_particles.remove(particle)

        # Create trail points while the mouse moves.
        if pygame.mouse.get_focused():
            if random.random() < 0.75:
                mouse_trail.append(
                    TrailPoint(
                        mouse_pos[0],
                        mouse_pos[1]
                    )
                )

        for point in mouse_trail[:]:
            point.update(dt)

            if point.life <= 0:
                mouse_trail.remove(point)

        # Keep the trail from growing too large.
        if len(mouse_trail) > 100:
            mouse_trail = mouse_trail[-100:]

        # ----------------------------------------------------
        # DRAW BACKGROUND
        # ----------------------------------------------------

        screen.blit(background, (0, 0))

        # Twinkling stars.
        for star in stars:
            star.draw(screen, elapsed)

        # Clear the glow layer every frame.
        glow_layer.fill((0, 0, 0, 0))

        # Draw the main energy core.
        draw_energy_core(
            screen,
            glow_layer,
            elapsed
        )

        # Draw orbiting particles.
        for particle in particles:
            particle.draw(
                screen,
                glow_layer,
                elapsed
            )

        # Draw click explosions.
        for particle in burst_particles:
            particle.draw(
                screen,
                glow_layer
            )

        # Draw mouse trail.
        for point in mouse_trail:
            point.draw(
                screen,
                glow_layer
            )

        # Blend the glow on top of the scene.
        screen.blit(
            glow_layer,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_ADD
        )

        # Draw interface last so the text stays readable.
        draw_interface(
            screen,
            elapsed
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()