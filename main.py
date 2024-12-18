#!/user/bin/env python3

__author__ = "spyderkam"

from formations import formation
import os
import pygame
import sys


# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Field")

# Colors
BLUE = (0, 0, 255)
GREEN = (50, 168, 82)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Team formations
ORIGINAL_BLUE = formation("433")[0]
ORIGINAL_RED = formation("442")[1]
BLUE_TEAM = [pos[:] for pos in ORIGINAL_BLUE]
RED_TEAM = [pos[:] for pos in ORIGINAL_RED]

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to reset
                    BLUE_TEAM[:] = [pos[:] for pos in ORIGINAL_BLUE]
                    RED_TEAM[:] = [pos[:] for pos in ORIGINAL_RED]
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
        pygame.draw.rect(SCREEN, WHITE, (50, 175, 150, 250), 2)         # Left
        pygame.draw.rect(SCREEN, WHITE, (WIDTH-200, 175, 150, 250), 2)  # Right

        # Goal areas
        pygame.draw.rect(SCREEN, WHITE, (50, 225, 60, 150), 2)          # Left
        pygame.draw.rect(SCREEN, WHITE, (WIDTH-110, 225, 60, 150), 2)   # Right

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