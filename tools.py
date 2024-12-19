
import pygame

def draw_triangle(screen, points, team_color):
    # Create a semi-transparent orange surface
    triangle_color = (255, 165, 0, 128)  # Orange with alpha
    
    # Create a surface for the semi-transparent triangle
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    pygame.draw.polygon(surface, triangle_color, points)
    
    # Blit the surface onto the screen
    screen.blit(surface, (0, 0))
