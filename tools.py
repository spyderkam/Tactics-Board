#!/user/bin/env python3

__author__ = "spyderkam"

import pygame

class Shape:
  """Shapes to draw on the board."""
  def __init__(self):
    self.shapes_visible = True

  def draw_triangle1(self, screen, points):
    "Semi-transparent orange triangle"
    triangle_color = (255, 165, 0, 100)  # Orange with alpha
    
    # Create a surface for the semi-transparent triangle
    surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.polygon(surface, triangle_color, points)
    
    # Blit the surface onto the screen
    screen.blit(surface, (0, 0))

  def draw_triangle2(self, screen, points):
    "Semi-transparent orange triangle"
    triangle_color = (128, 0, 128, 100)  # Purple with alpha 
    
    # Create a surface for the semi-transparent triangle
    surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.polygon(surface, triangle_color, points)
    
    # Blit the surface onto the screen
    screen.blit(surface, (0, 0))

  def draw_lines(self, screen, points):
    """Draw thin black lines connecting consecutive points, avoiding player circles"""
    if len(points) > 1:
      surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
      
      for i in range(len(points) - 1):
        # Calculate direction vector
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        # Calculate distance
        distance = (dx*dx + dy*dy)**0.5
        if distance == 0:
          continue
        
        # Normalize direction vector
        dx, dy = dx/distance, dy/distance
        
        # Adjust start and end points to be on circle edges
        start_x = points[i][0] + dx * 20  # 20 is circle radius
        start_y = points[i][1] + dy * 20
        end_x = points[i+1][0] - dx * 20
        end_y = points[i+1][1] - dy * 20
        
        # Draw dashed line between adjusted points
        dash_length = 20
        dash_gap = 10
        total_length = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5
        num_dashes = int(total_length / (dash_length + dash_gap))
        
        for i in range(num_dashes):
            start_ratio = i * (dash_length + dash_gap) / total_length
            end_ratio = min((i * (dash_length + dash_gap) + dash_length) / total_length, 1)
            
            dash_start_x = start_x + (end_x - start_x) * start_ratio
            dash_start_y = start_y + (end_y - start_y) * start_ratio
            dash_end_x = start_x + (end_x - start_x) * end_ratio
            dash_end_y = start_y + (end_y - start_y) * end_ratio
            
            pygame.draw.line(surface, (0, 0, 0, 200), (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), 6)
      
      screen.blit(surface, (0, 0))

class StopTool:
  """Tool to stop all active tools"""
  def __init__(self):
    self.name = "Stop Tool"
    
  def execute(self):
    return {
      'allow_dragging': True,
      'show_ball': False,
      'show_triangle1': False,
      'show_triangle2': False,
      'show_lines': False
    }