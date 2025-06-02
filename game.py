import pygame
import sys
from config import *
from entities import Snake, Food
from utils import create_forest_background, create_gradient_surface, draw_rounded_rect

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        
        self.background = create_forest_background(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.reset_game()
        self.high_score = 0
        
        self.ui_animation = 0
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = INITIAL_SPEED
        self.game_time = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.snake.change_direction(UP)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.snake.change_direction(DOWN)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.snake.change_direction(LEFT)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def update(self):
        if not self.game_over and not self.paused:
            self.game_time += 1
            self.ui_animation += 1
            
            self.food.update()
            
            self.snake.move()
            
            if self.snake.eat_food(self.food.position):
                self.score += FOOD_SCORE
                self.food.respawn(self.snake.body)
                
                self.speed = min(20, self.speed + SPEED_INCREMENT)
            
            if self.snake.check_collision():
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
    
    def draw_grid(self):
        path_color = (Colors.FOREST_ACCENT[0] + 10, Colors.FOREST_ACCENT[1] + 10, Colors.FOREST_ACCENT[2] + 10)
        
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, path_color, 
                           (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, path_color, 
                           (0, y), (WINDOW_WIDTH, y), 1)
    
    def draw_ui(self):
        score_text = self.large_font.render(f"Score: {self.score}", True, Colors.TEXT_PRIMARY)
        score_bg = pygame.Rect(10, 10, score_text.get_width() + 20, score_text.get_height() + 10)
        draw_rounded_rect(self.screen, Colors.LIGHT_BG, score_bg, 10)
        pygame.draw.rect(self.screen, Colors.ACCENT_GREEN, score_bg, 2, border_radius=10)
        self.screen.blit(score_text, (20, 15))
        
        if self.high_score > 0:
            high_score_text = self.medium_font.render(f"Best: {self.high_score}", True, Colors.TEXT_SECONDARY)
            self.screen.blit(high_score_text, (20, 50))
        
        minutes = self.game_time // (60 * FPS)
        seconds = (self.game_time // FPS) % 60
        time_text = self.medium_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, Colors.TEXT_SECONDARY)
        time_bg = pygame.Rect(WINDOW_WIDTH - time_text.get_width() - 30, 10, 
                            time_text.get_width() + 20, time_text.get_height() + 10)
        draw_rounded_rect(self.screen, Colors.LIGHT_BG, time_bg, 10)
        pygame.draw.rect(self.screen, Colors.ACCENT_BLUE, time_bg, 2, border_radius=10)
        self.screen.blit(time_text, (WINDOW_WIDTH - time_text.get_width() - 20, 15))
        
        speed_text = self.small_font.render(f"Speed: {self.speed:.1f}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(speed_text, (WINDOW_WIDTH - speed_text.get_width() - 20, 50))
        
        if not self.game_over:
            controls = "WASD/Arrows: Move • Space: Pause • ESC: Quit"
            controls_text = self.small_font.render(controls, True, Colors.TEXT_SECONDARY)
            controls_x = (WINDOW_WIDTH - controls_text.get_width()) // 2
            self.screen.blit(controls_text, (controls_x, WINDOW_HEIGHT - 30))
    
    def draw_overlay(self, title, subtitle, instructions):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(Colors.DARK_BG)
        self.screen.blit(overlay, (0, 0))
        
        panel_width = 400
        panel_height = 200
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        draw_rounded_rect(self.screen, Colors.LIGHT_BG, panel_rect, 20)
        pygame.draw.rect(self.screen, Colors.ACCENT_GREEN, panel_rect, 3, border_radius=20)
        
        title_text = self.title_font.render(title, True, Colors.TEXT_PRIMARY)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, panel_y + 40))
        self.screen.blit(title_text, title_rect)
        
        if subtitle:
            subtitle_text = self.large_font.render(subtitle, True, Colors.ACCENT_YELLOW)
            subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, panel_y + 80))
            self.screen.blit(subtitle_text, subtitle_rect)
        
        instructions_text = self.medium_font.render(instructions, True, Colors.TEXT_SECONDARY)
        instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH//2, panel_y + 130))
        self.screen.blit(instructions_text, instructions_rect)
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_ui()
        
        if self.game_over:
            subtitle = f"Final Score: {self.score}"
            if self.score == self.high_score and self.score > 0:
                subtitle += " (New Best!)"
            self.draw_overlay("GAME OVER", subtitle, "Press SPACE to restart • ESC to quit")
        elif self.paused:
            self.draw_overlay("PAUSED", None, "Press SPACE to continue")
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()