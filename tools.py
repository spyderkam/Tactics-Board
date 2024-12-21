#!/user/bin/env python3

__author__ = "spyderkam"

import pygame

def draw_triangle1(screen, points, team_color):
  # Create a semi-transparent orange surface
  triangle_color = (255, 165, 0, 128)  # Orange with alpha
  
  # Create a surface for the semi-transparent triangle
  surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
  pygame.draw.polygon(surface, triangle_color, points)
  
  # Blit the surface onto the screen
  screen.blit(surface, (0, 0))
