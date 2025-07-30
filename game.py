import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 900
JUMP_STRENGTH = -420
PIPE_SPEED = 180
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Load sprites
Bird_downflap = pygame.image.load("flappy-bird-assets\sprites\bluebird-downflap.png")
Bird_midflap = pygame.image.load("flappy-bird-assets\sprites\bluebird-midflap.png")
Bird_upflap = pygame.image.load("flappy-bird-assets\sprites\bluebird-upflap.png")
pipe_sprite = pygame.image.load("flappy-bird-assets\sprites\pipe-green.png")
bg = pygame.image.load("flappy-bird-assets\sprites\background-day.png")
zero = pygame.image.load("flappy-bird-assets\sprites\0.png")
one = pygame.image.load("flappy-bird-assets\sprites\1.png")
two = pygame.image.load("flappy-bird-assets\sprites\2.png")
three = pygame.image.load("flappy-bird-assets\sprites\3.png")
four = pygame.image.load("flappy-bird-assets\sprites\4.png")
five = pygame.image.load("flappy-bird-assets\sprites\5.png")
six = pygame.image.load("flappy-bird-assets\sprites\6.png")
seven = pygame.image.load("flappy-bird-assets\sprites\7.png")
eight = pygame.image.load("flappy-bird-assets\sprites\8.png")
nine = pygame.image.load("flappy-bird-assets\sprites\9.png")

# Scale sprites to appropriate sizes
bird_width, bird_height = 51, 36  # Decreased from 68, 48
Bird_downflap = pygame.transform.scale(Bird_downflap, (bird_width, bird_height))
Bird_midflap = pygame.transform.scale(Bird_midflap, (bird_width, bird_height))
Bird_upflap = pygame.transform.scale(Bird_upflap, (bird_width, bird_height))

pipe_width, pipe_height = 78, 480  # Decreased from 104, 640
pipe_sprite = pygame.transform.scale(pipe_sprite, (pipe_width, pipe_height))

bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Scale number sprites
number_width, number_height = 36, 54  # Increased from 24, 36
number_sprites = [zero, one, two, three, four, five, six, seven, eight, nine]
number_sprites = [pygame.transform.scale(sprite, (number_width, number_height)) for sprite in number_sprites]

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.animation_index = 0
        self.animation_speed = 0.2
        self.animation_counter = 0
        self.rotation = 0
        self.just_jumped = False
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        self.rotation = 0  # Reset rotation when jumping
        # Start with down-flap and animate through the cycle
        self.animation_index = 2  # Down-flap
        self.animation_counter = 2.0
        self.animation_speed = 3  # Much faster animation for jump
        self.just_jumped = True  # Flag to track jump animation
        
    def update(self, dt):
        self.velocity += GRAVITY * dt
        self.y += self.velocity * dt
        
        # Rotation based on velocity
        target_rotation = self.velocity * -5  # Negative because pygame rotates clockwise
        self.rotation += (target_rotation - self.rotation) * 0.1 * dt  # Smooth transition
        
        # Animation - cycle through up-flap, mid-flap, down-flap
        self.animation_counter += self.animation_speed * dt
        
        # Handle jump animation sequence
        if self.just_jumped:
            if self.animation_counter >= 3.0:  # Completed full cycle
                self.animation_counter = 0
                self.animation_speed = 0.2  # Reset to normal speed
                self.just_jumped = False
        else:
            # Normal animation cycle
            if self.animation_counter >= 3:
                self.animation_counter = 0
                
        self.animation_index = int(self.animation_counter)
        
    def draw(self, screen):
        bird_sprites = [Bird_upflap, Bird_midflap, Bird_downflap]
        rotated_bird = pygame.transform.rotate(bird_sprites[self.animation_index], self.rotation)
        # Get the rect of the rotated bird to center it properly
        bird_rect = rotated_bird.get_rect(center=(self.x + bird_width//2, self.y + bird_height//2))
        screen.blit(rotated_bird, bird_rect)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, bird_width, bird_height)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(50, SCREEN_HEIGHT - 150)
        self.passed = False
        
    def update(self, dt):
        self.x -= PIPE_SPEED * dt
        
    def draw(self, screen):
        # Top pipe
        top_pipe = pygame.transform.rotate(pipe_sprite, 180)
        screen.blit(top_pipe, (self.x, self.gap_y - pipe_height))
        
        # Bottom pipe
        screen.blit(pipe_sprite, (self.x, self.gap_y + PIPE_GAP))
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.gap_y - pipe_height, pipe_width, pipe_height)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, pipe_width, pipe_height)
        return top_rect, bottom_rect

def draw_score(screen, score):
    score_str = str(score)
    score_width = len(score_str) * number_width
    
    for i, digit in enumerate(score_str):
        digit_int = int(digit)
        x = (SCREEN_WIDTH - score_width) // 2 + i * number_width
        y = 50
        screen.blit(number_sprites[digit_int], (x, y))

def main():
    bird = Bird(100, SCREEN_HEIGHT // 2)
    pipes = []
    score = 0
    game_active = True
    last_pipe = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.jump()
                    else:
                        # Restart game
                        bird = Bird(100, SCREEN_HEIGHT // 2)
                        pipes = []
                        score = 0
                        game_active = True
                        last_pipe = current_time
        
        if game_active:
            # Update bird
            bird.update(dt)
            
            # Generate pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe(SCREEN_WIDTH))
                last_pipe = current_time
            
            # Update pipes
            for pipe in pipes[:]:
                pipe.update(dt)
                if pipe.x < -pipe_width:
                    pipes.remove(pipe)
                elif not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
            
            # Check collisions
            bird_rect = bird.get_rect()
            
            # Check if bird hits the ground or ceiling
            if bird.y <= 0 or bird.y >= SCREEN_HEIGHT - bird_height:
                game_active = False
            
            # Check pipe collisions
            for pipe in pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    game_active = False
        
        # Draw everything
        screen.blit(bg, (0, 0))
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)
        
        # Draw bird
        bird.draw(screen)
        
        # Draw score
        draw_score(screen, score)
        
        # Game over message
        if not game_active:
            font = pygame.font.Font(None, 32)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            text2 = font.render('Press SPACE to restart', True, WHITE)
            text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +32))
            screen.blit(text, text_rect)
            screen.blit(text2, text2_rect)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()









