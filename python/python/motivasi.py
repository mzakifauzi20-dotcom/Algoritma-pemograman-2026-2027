from __future__ import annotations
import math
import random
import sys
from dataclasses import dataclass
import pygame

@dataclass(frozen=True)
class Config:
    width: int = 1000
    height: int = 1000
    bg_color: tuple[int, int, int] = (3, 7, 19)  # Biru tua kosmik yang sangat elegan
    caption: str = "La Tahzan Innallaha Ma'ana — Floating Words & Stars"
    
    fill_gap: int = 24  # Kerapatan teks pembentuk bulan sabit agar jelas dan rapi
    fade_speed_min: int = 4
    fade_speed_max: int = 10
    
    moon_texts: tuple[str, ...] = (
        "La Tahzan", 
        "Innallaha", 
        "Ma'ana", 
        "La Tahzan Innallaha Ma'ana"
    )
    center_text: str = "LA TAHZAN INNALLAHA MA'ANA"
    
    colors: tuple[tuple[int, int, int], ...] = (
        (0, 240, 255),  # Cyan terang
        (0, 160, 255),  # Biru elektrik
        (100, 210, 255),# Biru muda
        (50, 120, 240)  # Biru safir
    )

class Star:
    """Efek bintang berkelap-kelip di latar belakang"""
    def __init__(self, width: int, height: int):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.size = random.uniform(1.0, 3.0)
        self.alpha = random.randint(50, 255)
        self.fade_speed = random.uniform(0.5, 2.0)

    def update(self):
        self.alpha += self.fade_speed
        if self.alpha > 255 or self.alpha < 50:
            self.fade_speed *= -1

    def draw(self, surface: pygame.Surface):
        current_alpha = int(max(0, min(255, self.alpha)))
        s = pygame.Surface((int(self.size*4), int(self.size*4)), pygame.SRCALPHA)
        # Glow bintang
        pygame.draw.circle(s, (0, 200, 255, current_alpha // 3), (int(self.size*2), int(self.size*2)), self.size * 2)
        # Inti bintang
        pygame.draw.circle(s, (200, 245, 255, current_alpha), (int(self.size*2), int(self.size*2)), self.size)
        surface.blit(s, (self.x - self.size*2, self.y - self.size*2))

class DriftingText:
    """Kata-kata motivasi yang berterbangan bebas di sekitar layar"""
    def __init__(self, width: int, height: int, font: pygame.font.Font):
        self.width = width
        self.height = height
        self.font = font
        self.reset()
        
    def reset(self):
        self.x = random.randint(50, self.width - 50)
        self.y = random.randint(50, self.height - 50)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.7, -0.2)
        self.text = random.choice([
            "La Tahzan", "Innallaha Ma'ana", "Sabar", "Tawakal", "Yakin", "Harapan"
        ])
        self.color = random.choice([
            (0, 220, 255), (100, 200, 255), (50, 150, 255), (200, 230, 255)
        ])
        self.alpha = 0.0
        self.max_alpha = random.randint(100, 180)
        self.state = "fade_in"
        self.life = random.randint(200, 400)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.state == "fade_in":
            self.alpha += 1.5
            if self.alpha >= self.max_alpha:
                self.alpha = self.max_alpha
                self.state = "float"
        elif self.state == "float":
            self.life -= 1
            if self.life <= 0:
                self.state = "fade_out"
        elif self.state == "fade_out":
            self.alpha -= 1.5
            if self.alpha <= 0:
                self.reset()
                
        if self.y < -20 or self.x < -50 or self.x > self.width + 50:
            self.reset()

    def draw(self, surface: pygame.Surface):
        if self.alpha <= 0:
            return
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(int(self.alpha))
        rect = surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(surf, rect)

class SilhouetteText:
    """Teks pembentuk siluet Bulan Sabit"""
    def __init__(self, x: float, y: float, text: str, font: pygame.font.Font, color: tuple[int, int, int], delay: float):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.delay = delay
        self.alpha = 0.0
        self.fade_speed = random.uniform(4, 10)
        self.rendered_surface = self.font.render(self.text, True, self.color)
        
    def update(self, dt: float):
        if self.delay > 0:
            self.delay -= dt
            return
        if self.alpha < 255:
            self.alpha = min(255.0, self.alpha + self.fade_speed * dt * 60)

    def draw(self, surface: pygame.Surface):
        if self.alpha <= 0:
            return
        surf = self.rendered_surface.copy()
        surf.set_alpha(int(self.alpha))
        rect = surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(surf, rect)

def generate_crescent_points(config: Config) -> list[tuple[float, float, float]]:
    points = []
    R_outer = 300
    R_inner = 270
    cx_inner, cy_inner = 100, -35
    
    for x in range(-340, 340, config.fill_gap):
        for y in range(-340, 340, config.fill_gap):
            dist_outer = x**2 + y**2
            dist_inner = (x - cx_inner)**2 + (y - cy_inner)**2
            
            if dist_outer <= R_outer**2 and dist_inner > R_inner**2:
                dist_from_center = math.hypot(x, y)
                delay = 1.0 + (dist_from_center / R_outer) * 2.0
                screen_x = config.width / 2 + x
                screen_y = config.height / 2 + y
                points.append((screen_x, screen_y, delay))
                
    return points

def main():
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption(config.caption)
    clock = pygame.time.Clock()
    
    font_small = pygame.font.SysFont("Segoe UI", 12, bold=True)
    font_drift = pygame.font.SysFont("Segoe UI", 13, bold=True)
    font_large = pygame.font.SysFont("Segoe UI", 36, bold=True)
    
    # 1. Bintang latar belakang yang berkelap-kelip
    stars = [Star(config.width, config.height) for _ in range(120)]
    
    # 2. Kata-kata motivasi yang berterbangan bebas di layar
    drifting_texts = [DriftingText(config.width, config.height, font_drift) for _ in range(20)]
    
    # 3. Siluet Bulan Sabit
    crescent_points = generate_crescent_points(config)
    silhouette_texts: list[SilhouetteText] = []
    
    for x, y, delay in crescent_points:
        text = random.choice(config.moon_texts)
        color = random.choice(config.colors)
        silhouette_texts.append(SilhouetteText(x, y, text, font_small, color, delay))
        
    # 4. Teks Utama Besar persis di TENGAH layar pada detik akhir
    center_text_obj = SilhouetteText(
        config.width / 2, 
        config.height / 2, 
        config.center_text, 
        font_large, 
        (255, 255, 255),  # Warna putih terang bercahaya
        delay=3.8
    )
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                
        # Render Latar Belakang
        screen.fill(config.bg_color)
        
        # Gambar Bintang Berkelap-kelip
        for star in stars:
            star.update()
            star.draw(screen)
            
        # Gambar Kata-kata Berterbangan (Drifting Texts)
        for dt_item in drifting_texts:
            dt_item.update()
            dt_item.draw(screen)
            
        # Gambar Siluet Bulan Sabit
        for st in silhouette_texts:
            st.update(dt)
            st.draw(screen)
            
        # Gambar Teks Besar di Tengah pada Detik Akhir
        center_text_obj.update(dt)
        center_text_obj.draw(screen)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()