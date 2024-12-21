#!/user/bin/env python3

__author__ = "spyderkam"

import pygame

class Shape:
  """Shapes to draw on the board."""
  def __init__(self):
    pass

  def draw_triangle1(self, screen, points):
    "Semi-transparent orange triangle"
    triangle_color = (255, 165, 0, 128)  # Orange with alpha
    
    # Create a surface for the semi-transparent triangle
    surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.polygon(surface, triangle_color, points)
    
    # Blit the surface onto the screen
    screen.blit(surface, (0, 0))
