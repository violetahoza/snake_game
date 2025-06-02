import pygame

from config import Colors

def create_gradient_surface(width, height, start_color, end_color):
    surface = pygame.Surface((width, height))
    
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    return surface

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def create_glow_effect(surface, color, position, radius):
    glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    
    for i in range(radius, 0, -2):
        alpha = int(30 * (radius - i) / radius)
        glow_color = (*color[:3], alpha)
        pygame.draw.circle(glow_surface, glow_color, 
                         (radius * 2, radius * 2), i)
    
    surface.blit(glow_surface, 
                (position[0] - radius * 2, position[1] - radius * 2))

def lerp(start, end, t):
    return start + (end - start) * t

def create_forest_background(width, height):
    import random
    surface = pygame.Surface((width, height))
    
    for y in range(height):
        ratio = y / height
        r = int(Colors.FOREST_DARK[0] * (1 - ratio) + Colors.FOREST_LIGHT[0] * ratio)
        g = int(Colors.FOREST_DARK[1] * (1 - ratio) + Colors.FOREST_LIGHT[1] * ratio)
        b = int(Colors.FOREST_DARK[2] * (1 - ratio) + Colors.FOREST_LIGHT[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    
    random.seed(42)  
    for _ in range(8):
        tree_x = random.randint(50, width - 50)
        tree_y = random.randint(50, height - 100)
        
        trunk_width = random.randint(8, 15)
        trunk_height = random.randint(30, 50)
        trunk_rect = pygame.Rect(tree_x - trunk_width//2, tree_y, trunk_width, trunk_height)
        pygame.draw.rect(surface, Colors.TREE_BROWN, trunk_rect, border_radius=3)
        
        crown_radius = random.randint(20, 35)
        crown_center = (tree_x, tree_y - crown_radius//2)
        
        for i in range(3):
            offset_x = random.randint(-8, 8)
            offset_y = random.randint(-8, 8)
            crown_pos = (crown_center[0] + offset_x, crown_center[1] + offset_y)
            pygame.draw.circle(surface, Colors.LEAF_GREEN, crown_pos, crown_radius - i*3)
    
    for _ in range(15):
        grass_x = random.randint(0, width)
        grass_y = random.randint(0, height)
        grass_size = random.randint(10, 25)
        
        for j in range(random.randint(3, 7)):
            grass_offset_x = random.randint(-grass_size//2, grass_size//2)
            grass_offset_y = random.randint(-grass_size//2, grass_size//2)
            grass_pos = (grass_x + grass_offset_x, grass_y + grass_offset_y)
            grass_radius = random.randint(3, 8)
            pygame.draw.circle(surface, Colors.GRASS_GREEN, grass_pos, grass_radius)
    
    for _ in range(5):
        mushroom_x = random.randint(30, width - 30)
        mushroom_y = random.randint(30, height - 30)
        
        stem_rect = pygame.Rect(mushroom_x - 2, mushroom_y, 4, 8)
        pygame.draw.rect(surface, (245, 245, 220), stem_rect)
        
        cap_color = random.choice([(178, 34, 34), (139, 69, 19), (160, 82, 45)])
        pygame.draw.circle(surface, cap_color, (mushroom_x, mushroom_y), 6)
        
        if random.random() > 0.5:
            for _ in range(random.randint(2, 4)):
                spot_x = mushroom_x + random.randint(-4, 4)
                spot_y = mushroom_y + random.randint(-4, 4)
                pygame.draw.circle(surface, (255, 255, 255), (spot_x, spot_y), 1)
    
    return surface