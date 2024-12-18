
import pygame
import sys
import os

# Configure SDL to use a compatible display driver
os.environ['SDL_VIDEODRIVER'] = 'x11'

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Field")

# Colors
GREEN = (50, 168, 82)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player positions for 4-4-2 formation
BLUE_TEAM = [
    [150, 300],  # GK
    [200, 150],  # DEF
    [200, 250],  # DEF
    [200, 350],  # DEF
    [200, 450],  # DEF
    [350, 150],  # MID
    [350, 250],  # MID
    [350, 350],  # MID
    [350, 450],  # MID
    [450, 250],  # FWD
    [450, 350],  # FWD
]

RED_TEAM = [
    [650, 300],  # GK
    [600, 150],  # DEF
    [600, 250],  # DEF
    [600, 350],  # DEF
    [600, 450],  # DEF
    [450, 150],  # MID
    [450, 250],  # MID
    [450, 350],  # MID
    [450, 450],  # MID
    [350, 250],  # FWD
    [350, 350],  # FWD
]

def draw_player(screen, pos, color):
    pygame.draw.circle(screen, color, pos, 10)

def get_clicked_player(pos, team):
    for i, player_pos in enumerate(team):
        distance = ((pos[0] - player_pos[0])**2 + (pos[1] - player_pos[1])**2)**0.5
        if distance < 10:
            return i
    return None

# Main game loop
def main():
    running = True
    dragging = False
    selected_team = None
    selected_player = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                blue_player = get_clicked_player(mouse_pos, BLUE_TEAM)
                red_player = get_clicked_player(mouse_pos, RED_TEAM)
                
                if blue_player is not None:
                    selected_team = BLUE_TEAM
                    selected_player = blue_player
                    dragging = True
                elif red_player is not None:
                    selected_team = RED_TEAM
                    selected_player = red_player
                    dragging = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                selected_team = None
                selected_player = None
                
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_pos = pygame.mouse.get_pos()
                selected_team[selected_player][0] = mouse_pos[0]
                selected_team[selected_player][1] = mouse_pos[1]

        # Fill background with green
        SCREEN.fill(GREEN)

        # Draw field lines
        # Outer boundary
        pygame.draw.rect(SCREEN, WHITE, (50, 50, WIDTH-100, HEIGHT-100), 2)
        
        # Center line
        pygame.draw.line(SCREEN, WHITE, (WIDTH//2, 50), (WIDTH//2, HEIGHT-50), 2)
        
        # Center circle
        pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 70, 2)
        pygame.draw.circle(SCREEN, WHITE, (WIDTH//2, HEIGHT//2), 5)

        # Penalty areas
        pygame.draw.rect(SCREEN, WHITE, (50, 175, 150, 250), 2)  # Left
        pygame.draw.rect(SCREEN, WHITE, (WIDTH-200, 175, 150, 250), 2)  # Right

        # Goal areas
        pygame.draw.rect(SCREEN, WHITE, (50, 225, 60, 150), 2)  # Left
        pygame.draw.rect(SCREEN, WHITE, (WIDTH-110, 225, 60, 150), 2)  # Right

        # Draw players
        for pos in BLUE_TEAM:
            draw_player(SCREEN, pos, BLUE)
        for pos in RED_TEAM:
            draw_player(SCREEN, pos, RED)

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
