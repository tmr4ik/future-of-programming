import pygame
import random
import sys
from pieces import Piece, PENTOMINOES, COLORS

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # Extra space for score and next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class PentosGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pentos')
        self.clock = pygame.time.Clock()
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_speed = 1000  # Starting speed in milliseconds
        self.last_fall_time = pygame.time.get_ticks()
        self.spawn_new_piece()
    
    def spawn_new_piece(self):
        """Create a new piece and set its initial position"""
        if self.next_piece is None:
            self.next_piece = Piece(random.choice(list(PENTOMINOES.keys())))
        
        self.current_piece = self.next_piece
        self.next_piece = Piece(random.choice(list(PENTOMINOES.keys())))
        
        # Set starting position
        self.current_piece.x = GRID_WIDTH // 2 - self.current_piece.get_width() // 2
        self.current_piece.y = 0
        
        # Check if game is over
        if self.check_collision():
            self.game_over = True
    
    def check_collision(self):
        """Check if current piece collides with anything"""
        shape = self.current_piece.get_shape()
        for y in range(shape.shape[0]):
            for x in range(shape.shape[1]):
                if shape[y][x]:
                    next_x = self.current_piece.x + x
                    next_y = self.current_piece.y + y
                    
                    if (next_x < 0 or next_x >= GRID_WIDTH or 
                        next_y >= GRID_HEIGHT or 
                        (next_y >= 0 and self.grid[next_y][next_x] is not None)):
                        return True
        return False
    
    def lock_piece(self):
        """Lock the current piece in place"""
        shape = self.current_piece.get_shape()
        for y in range(shape.shape[0]):
            for x in range(shape.shape[1]):
                if shape[y][x]:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        
        self.clear_lines()
        self.spawn_new_piece()
    
    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        if not lines_to_clear:
            return
        
        # Update score based on number of lines cleared
        lines_count = len(lines_to_clear)
        if lines_count == 1:
            self.score += 100 * self.level
        elif lines_count == 2:
            self.score += 300 * self.level
        elif lines_count == 3:
            self.score += 500 * self.level
        elif lines_count == 4:
            self.score += 700 * self.level
        elif lines_count == 5:
            self.score += 800 * self.level
        
        # Remove the lines and add new empty lines at the top
        for line in sorted(lines_to_clear, reverse=True):
            self.grid.pop(line)
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        self.lines_cleared += lines_count
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(100, 1000 - (self.level - 1) * 100)  # Speed up as level increases
    
    def move(self, dx, dy):
        """Move the current piece if possible"""
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if self.check_collision():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:  # If moving down caused collision, lock the piece
                self.lock_piece()
    
    def rotate(self):
        """Rotate the current piece if possible"""
        self.current_piece.rotate()
        if self.check_collision():
            # Try wall kicks
            original_x = self.current_piece.x
            for dx in [-1, 1, -2, 2]:
                self.current_piece.x += dx
                if not self.check_collision():
                    return
                self.current_piece.x = original_x
            
            # If all wall kicks fail, revert rotation
            for _ in range(3):
                self.current_piece.rotate()
    
    def hard_drop(self):
        """Drop the piece to the bottom instantly"""
        drop_distance = 0
        while not self.check_collision():
            self.current_piece.y += 1
            drop_distance += 1
        
        self.current_piece.y -= 1
        drop_distance -= 1
        self.score += drop_distance * 2  # 2 points per cell dropped
        self.lock_piece()
    
    def draw(self):
        """Draw the game state"""
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, GRAY,
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                   (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # Draw current piece
        if self.current_piece:
            shape = self.current_piece.get_shape()
            for y in range(shape.shape[0]):
                for x in range(shape.shape[1]):
                    if shape[y][x]:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       ((self.current_piece.x + x) * BLOCK_SIZE,
                                        (self.current_piece.y + y) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # Draw next piece preview
        if self.next_piece:
            font = pygame.font.Font(None, 36)
            text = font.render('Next:', True, WHITE)
            self.screen.blit(text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
            
            shape = self.next_piece.get_shape()
            for y in range(shape.shape[0]):
                for x in range(shape.shape[1]):
                    if shape[y][x]:
                        pygame.draw.rect(self.screen, self.next_piece.color,
                                       (GRID_WIDTH * BLOCK_SIZE + 20 + x * BLOCK_SIZE,
                                        80 + y * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 200))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 20, 240))
        
        if self.game_over:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render('GAME OVER', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            self.hard_drop()
            
            if not self.game_over:
                # Handle continuous key presses
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    self.move(0, 1)
                    self.score += 1  # 1 point per cell for soft drop
                
                # Natural falling
                if current_time - self.last_fall_time > self.fall_speed:
                    self.move(0, 1)
                    self.last_fall_time = current_time
            
            self.draw()
            self.clock.tick(60)

if __name__ == '__main__':
    game = PentosGame()
    game.run()
