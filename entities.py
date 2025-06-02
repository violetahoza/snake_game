import pygame
import random
import math
from config import *
from utils import draw_rounded_rect, create_glow_effect

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        self.animation_offset = 0
        self.last_direction = RIGHT
    
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        self.last_direction = self.direction
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        self.animation_offset = (self.animation_offset + 1) % 60
    
    def change_direction(self, new_direction):
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        if opposite != new_direction:
            self.direction = new_direction
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        if (head_x < 0 or head_x >= GRID_WIDTH or 
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True
        
        if self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def eat_food(self, food_pos):
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False
    
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, 
                             GRID_SIZE - 4, GRID_SIZE - 4)
            
            if i == 0:  
                head_color = Colors.SNAKE_HEAD
                border_color = Colors.SNAKE_HEAD_BORDER
                
                pulse = math.sin(self.animation_offset * 0.2) * 0.1 + 0.9
                adjusted_rect = pygame.Rect(
                    rect.x + (1 - pulse) * rect.width // 2,
                    rect.y + (1 - pulse) * rect.height // 2,
                    rect.width * pulse,
                    rect.height * pulse
                )
                
                draw_rounded_rect(surface, head_color, adjusted_rect, 8)
                draw_rounded_rect(surface, border_color, adjusted_rect, 8)
                pygame.draw.rect(surface, border_color, adjusted_rect, 3, border_radius=8)
                
                eye_size = 4
                if self.direction == UP:
                    eye1_pos = (adjusted_rect.centerx - 4, adjusted_rect.centery - 3)
                    eye2_pos = (adjusted_rect.centerx + 4, adjusted_rect.centery - 3)
                elif self.direction == DOWN:
                    eye1_pos = (adjusted_rect.centerx - 4, adjusted_rect.centery + 3)
                    eye2_pos = (adjusted_rect.centerx + 4, adjusted_rect.centery + 3)
                elif self.direction == LEFT:
                    eye1_pos = (adjusted_rect.centerx - 3, adjusted_rect.centery - 4)
                    eye2_pos = (adjusted_rect.centerx - 3, adjusted_rect.centery + 4)
                else:  
                    eye1_pos = (adjusted_rect.centerx + 3, adjusted_rect.centery - 4)
                    eye2_pos = (adjusted_rect.centerx + 3, adjusted_rect.centery + 4)
                
                pygame.draw.circle(surface, Colors.TEXT_PRIMARY, eye1_pos, eye_size)
                pygame.draw.circle(surface, Colors.TEXT_PRIMARY, eye2_pos, eye_size)
                pygame.draw.circle(surface, Colors.DARK_BG, eye1_pos, eye_size - 1)
                pygame.draw.circle(surface, Colors.DARK_BG, eye2_pos, eye_size - 1)
                
            else:  
                size_factor = 1.0 - (i / len(self.body)) * 0.15
                body_size = int((GRID_SIZE - 4) * size_factor)
                offset = ((GRID_SIZE - 4) - body_size) // 2
                
                fade = (i - 1) / max(len(self.body) - 1, 1)
                body_color = (
                    int(Colors.SNAKE_BODY[0] * (1 - fade * 0.3)),
                    int(Colors.SNAKE_BODY[1] * (1 - fade * 0.3)),
                    int(Colors.SNAKE_BODY[2] * (1 - fade * 0.2))
                )
                border_color = Colors.SNAKE_BODY_BORDER
                
                wave_offset = math.sin((self.animation_offset + i * 8) * 0.1) * 1.5
                body_rect = pygame.Rect(rect.x + wave_offset + offset, rect.y + offset, 
                                      body_size, body_size)
                
                shadow_rect = pygame.Rect(body_rect.x + 1, body_rect.y + 1, 
                                        body_rect.width, body_rect.height)
                draw_rounded_rect(surface, (20, 25, 35), shadow_rect, 5)
                draw_rounded_rect(surface, body_color, body_rect, 5)
                pygame.draw.rect(surface, border_color, body_rect, 2, border_radius=5)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.animation_time = 0
        self.spawn_animation = 0
        self.type = "normal"  
    
    def generate_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                self.spawn_animation = 30  
                break
    
    def update(self):
        self.animation_time += 1
        if self.spawn_animation > 0:
            self.spawn_animation -= 1
    
    def draw(self, surface):
        x, y = self.position
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        pulse = math.sin(self.animation_time * 0.15) * 0.2 + 0.8
        radius = int((GRID_SIZE // 2 - 2) * pulse)
        
        if self.spawn_animation > 0:
            scale = 1 - (self.spawn_animation / 30) * 0.5
            radius = int(radius * scale)
        
        if radius > 5:
            create_glow_effect(surface, Colors.FOOD_GLOW, 
                             (center_x, center_y), radius + 5)
        
        pygame.draw.circle(surface, Colors.FOOD_PRIMARY, 
                         (center_x, center_y), radius)
        pygame.draw.circle(surface, Colors.FOOD_SECONDARY, 
                         (center_x, center_y), radius, 3)
        
        highlight_pos = (center_x - radius // 2, center_y - radius // 2)
        highlight_radius = radius // 3
        pygame.draw.circle(surface, Colors.TEXT_PRIMARY, 
                         highlight_pos, highlight_radius)