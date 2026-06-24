import pygame
import random
import sys
import os

# --- Constants ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BLOCK_SIZE = 25  # 40x28 grid
FPS = 7          # Relaxed speed (less speed) for better control and retro vibe

# Colors (R, G, B) - Premium Neon / Cyberpunk Theme
BG_COLOR = (11, 12, 16)         # Deep slate black
GRID_COLOR = (20, 24, 33)       # Subtle grid line
BORDER_COLOR = (102, 252, 241)  # Neon Cyan
WHITE = (224, 230, 237)         # Off-white text
GRAY = (139, 155, 180)          # Muted text

# Snake Colors
SNAKE_HEAD_COLOR = (102, 252, 241) # Neon Cyan
SNAKE_BODY_START = (102, 252, 241) # Cyan
SNAKE_BODY_END = (31, 111, 120)    # Deep Teal

# Food Colors
FOOD_COLOR = (255, 0, 127)         # Neon Pink/Magenta
LEAF_COLOR = (82, 183, 136)        # Emerald Green

# Directions
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NEON ARCADE // SNAKE")
        self.clock = pygame.time.Clock()
        
        # Load fonts safely
        try:
            self.font = pygame.font.SysFont("arial", 22, bold=True)
            self.large_font = pygame.font.SysFont("arial", 56, bold=True)
            self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        except Exception:
            self.font = pygame.font.Font(None, 28)
            self.large_font = pygame.font.Font(None, 64)
            self.title_font = pygame.font.Font(None, 42)
            
        self.high_score = self.load_high_score()
        self.reset_game()

    def load_high_score(self):
        """Load high score from a file if it exists."""
        try:
            if os.path.exists("highscore.txt"):
                with open("highscore.txt", "r") as f:
                    return int(f.read().strip())
        except Exception:
            pass
        return 0

    def save_high_score(self):
        """Save high score to a file."""
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    def reset_game(self):
        """Initialize or reset the game state."""
        # Snake starts in the middle, length of 3 segments
        start_x = (WINDOW_WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE
        start_y = (WINDOW_HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE
        
        self.snake = [
            [start_x, start_y],
            [start_x - BLOCK_SIZE, start_y],
            [start_x - (2 * BLOCK_SIZE), start_y]
        ]
        
        self.direction = RIGHT
        self.input_queue = [] # Buffer to prevent rapid counter-steers
        
        self.score = 0
        self.food_pos = self.spawn_food()
        self.game_over = False
        self.paused = False

    def spawn_food(self):
        """Spawn food at a random location not occupied by the snake, leaving margins."""
        max_cols = WINDOW_WIDTH // BLOCK_SIZE
        max_rows = WINDOW_HEIGHT // BLOCK_SIZE
        
        while True:
            # Leave 1 grid block margin around the screen for visual border
            x = random.randrange(1, max_cols - 1) * BLOCK_SIZE
            y = random.randrange(1, max_rows - 1) * BLOCK_SIZE
            if [x, y] not in self.snake:
                return [x, y]

    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.save_high_score()
                        pygame.quit()
                        sys.exit()
                else:
                    # Toggle Pause
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        continue
                        
                    if self.paused:
                        # Pressing directions while paused resumes the game
                        self.paused = False

                    # Map keys to directions
                    new_dir = None
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        new_dir = UP
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        new_dir = DOWN
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        new_dir = LEFT
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        new_dir = RIGHT

                    if new_dir:
                        # Use input queue to avoid self-collisions from double taps
                        last_planned = self.input_queue[-1] if self.input_queue else self.direction
                        if new_dir == UP and last_planned != DOWN:
                            self.input_queue.append(UP)
                        elif new_dir == DOWN and last_planned != UP:
                            self.input_queue.append(DOWN)
                        elif new_dir == LEFT and last_planned != RIGHT:
                            self.input_queue.append(LEFT)
                        elif new_dir == RIGHT and last_planned != LEFT:
                            self.input_queue.append(RIGHT)

    def update(self):
        """Update game logic."""
        if self.game_over or self.paused:
            return

        # Pop next direction from queue if available
        if self.input_queue:
            self.direction = self.input_queue.pop(0)
        
        # Calculate new head position
        head = list(self.snake[0])
        if self.direction == UP:
            head[1] -= BLOCK_SIZE
        elif self.direction == DOWN:
            head[1] += BLOCK_SIZE
        elif self.direction == LEFT:
            head[0] -= BLOCK_SIZE
        elif self.direction == RIGHT:
            head[0] += BLOCK_SIZE

        # Check wall collisions (die on wall)
        if head[0] < 0 or head[0] >= WINDOW_WIDTH or head[1] < 0 or head[1] >= WINDOW_HEIGHT:
            self.trigger_game_over()
            return

        # Check self collisions
        if head in self.snake[1:]:
            self.trigger_game_over()
            return

        # Move snake
        self.snake.insert(0, head)

        # Check food collision
        if head == self.food_pos:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.food_pos = self.spawn_food()
        else:
            # Remove tail if no food was eaten
            self.snake.pop()

    def trigger_game_over(self):
        self.game_over = True
        self.save_high_score()

    def get_gradient_color(self, start_color, end_color, factor):
        """Linearly interpolate between two colors."""
        r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
        return (r, g, b)

    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(BG_COLOR)

        # Draw grid
        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

        # Draw outer neon boundary border
        pygame.draw.rect(self.screen, BORDER_COLOR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 4)

        # Draw snake body and head
        for i, segment in enumerate(self.snake):
            if i == 0:
                # Snake Head
                head_rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, SNAKE_HEAD_COLOR, head_rect, border_radius=6)
                
                # Draw direction-oriented eyes
                eye_color = (255, 255, 255)
                pupil_color = (0, 0, 0)
                eye_radius = 3
                pupil_radius = 1
                
                head_x, head_y = segment
                if self.direction == RIGHT:
                    eye1 = (head_x + int(BLOCK_SIZE * 0.7), head_y + int(BLOCK_SIZE * 0.3))
                    eye2 = (head_x + int(BLOCK_SIZE * 0.7), head_y + int(BLOCK_SIZE * 0.7))
                elif self.direction == LEFT:
                    eye1 = (head_x + int(BLOCK_SIZE * 0.3), head_y + int(BLOCK_SIZE * 0.3))
                    eye2 = (head_x + int(BLOCK_SIZE * 0.3), head_y + int(BLOCK_SIZE * 0.7))
                elif self.direction == UP:
                    eye1 = (head_x + int(BLOCK_SIZE * 0.3), head_y + int(BLOCK_SIZE * 0.3))
                    eye2 = (head_x + int(BLOCK_SIZE * 0.7), head_y + int(BLOCK_SIZE * 0.3))
                else: # DOWN
                    eye1 = (head_x + int(BLOCK_SIZE * 0.3), head_y + int(BLOCK_SIZE * 0.7))
                    eye2 = (head_x + int(BLOCK_SIZE * 0.7), head_y + int(BLOCK_SIZE * 0.7))

                pygame.draw.circle(self.screen, eye_color, eye1, eye_radius)
                pygame.draw.circle(self.screen, eye_color, eye2, eye_radius)
                pygame.draw.circle(self.screen, pupil_color, eye1, pupil_radius)
                pygame.draw.circle(self.screen, pupil_color, eye2, pupil_radius)
            else:
                # Snake Body with gradient tail-fade
                blend_factor = i / len(self.snake)
                color = self.get_gradient_color(SNAKE_BODY_START, SNAKE_BODY_END, blend_factor)
                
                # Make body segments slightly taper towards the tail
                taper = max(0.7, 1.0 - (i / len(self.snake)) * 0.25)
                size = int(BLOCK_SIZE * taper)
                offset = (BLOCK_SIZE - size) // 2
                
                body_rect = pygame.Rect(segment[0] + offset, segment[1] + offset, size, size)
                pygame.draw.rect(self.screen, color, body_rect, border_radius=4)

        # Draw food (pink cherry-like shape)
        food_x, food_y = self.food_pos
        food_rect = pygame.Rect(food_x + 2, food_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect, border_radius=10)
        
        # Little green leaf
        leaf_x = food_x + BLOCK_SIZE // 2
        leaf_y = food_y
        leaf_rect = pygame.Rect(leaf_x, leaf_y, BLOCK_SIZE // 4, BLOCK_SIZE // 4)
        pygame.draw.rect(self.screen, LEAF_COLOR, leaf_rect, border_radius=2)

        # HUD Panel at the top (Score & High Score)
        score_bg = pygame.Surface((250, 45))
        score_bg.set_alpha(180)
        score_bg.fill((16, 17, 26))
        self.screen.blit(score_bg, (15, 15))
        pygame.draw.rect(self.screen, BORDER_COLOR, (15, 15, 250, 45), 1, border_radius=4)

        score_text = self.font.render(f"SCORE: {self.score:04d}   HI: {self.high_score:04d}", True, WHITE)
        self.screen.blit(score_text, (30, 24))

        # Pause Overlay
        if self.paused and not self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 5, 8, 200))  # Semi-transparent dark overlay
            self.screen.blit(overlay, (0, 0))

            paused_title = self.large_font.render("GAME PAUSED", True, BORDER_COLOR)
            paused_rect = paused_title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(paused_title, paused_rect)

            resume_text = self.font.render("Press SPACE / ESC to Resume or Direction to Steer", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(resume_text, resume_rect)

        # Game Over Screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((5, 5, 8, 220))  # Slightly darker overlay
            self.screen.blit(overlay, (0, 0))

            go_title = self.large_font.render("GAME OVER", True, FOOD_COLOR)
            go_rect = go_title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(go_title, go_rect)

            score_summary = self.title_font.render(f"FINAL SCORE: {self.score}", True, WHITE)
            summary_rect = score_summary.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(score_summary, summary_rect)

            restart_text = self.font.render("Press SPACE to Restart or ESC to Exit", True, GRAY)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()