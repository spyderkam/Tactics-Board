#!/user/bin/env python3

# Specifies the author of the code

__author__ = "spyderkam"

# Define color constants using RGB values (Red, Green, Blue) from 0-255

# These colors are used throughout the application for visual elements

BLUE = (0, 0, 255)      # Pure blue color
GREEN = (50, 168, 82)   # Custom green color for the field
RED = (255, 0, 0)       # Pure red color
WHITE = (255, 255, 255) # Pure white color
BLACK = (0, 0, 0)       # Pure black color

def formation(formation_type):
  """
  Takes a formation type as input and returns a dictionary containing two arrays
  of coordinates for both blue and red teams.
  Each array contains 11 player positions [x, y] where:
  - x represents horizontal position (0 to 1920)
  - y represents vertical position (0 to 1080)
  """
  match formation_type:
    case "4-3-3":
      # Classic attacking formation
      # Numbers in comments indicate player positions (GK, LB, etc.)
      return {"blue": [
        [1740, 540],   # GK (Goalkeeper)
        [1356, 252],   # LB (Left Back)
        [1464, 450],   # LCB (Left Center Back)
        [1464, 630],   # RCB (Right Center Back)
        [1356, 828],   # RB (Right Back)
        [1080, 360],   # LCM (Left Center Midfielder)
        [1080, 540],   # CM (Center Midfielder)
        [1080, 720],   # RCM (Right Center Midfielder)
        [720, 270],    # LW (Left Wing)
        [720, 540],    # ST (Striker)
        [720, 810],    # RW (Right Wing)
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [564, 252],    # LB
        [456, 450],    # LCB
        [456, 630],    # RCB
        [564, 828],    # RB
        [840, 360],    # LCM
        [840, 540],    # CM
        [840, 720],    # RCM
        [1200, 270],   # LW
        [1200, 540],   # ST
        [1200, 810],   # RW
      ]}

    case "4-2-3-1":
      # Modern defensive formation with two holding midfielders
      return {"blue": [
        [1740, 540],   # GK
        [1356, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1356, 828],   # RB
        [1080, 450],   # LDM (Left Defensive Midfielder)
        [1080, 630],   # RDM (Right Defensive Midfielder)
        [720, 270],    # LAM (Left Attacking Midfielder)
        [720, 540],    # CAM (Center Attacking Midfielder)
        [720, 810],    # RAM (Right Attacking Midfielder)
        [500, 540],    # ST
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [564, 252],    # LB
        [456, 450],    # LCB
        [456, 630],    # RCB
        [564, 828],    # RB
        [840, 450],    # LDM
        [840, 630],    # RDM
        [1200, 270],   # LAM
        [1200, 540],   # CAM
        [1200, 810],   # RAM
        [1420, 540],   # ST
      ]}

    case "4-4-2":
      # Classic balanced formation with four midfielders and two strikers
      return {"blue": [
        [1740, 540],   # GK
        [1356, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1356, 828],   # RB
        [1080, 270],   # LM (Left Midfielder)
        [1080, 450],   # LCM
        [1080, 630],   # RCM
        [1080, 810],   # RM (Right Midfielder)
        [720, 450],    # LST (Left Striker)
        [720, 630],    # RST (Right Striker)
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [564, 252],    # LB
        [456, 450],    # LCB
        [456, 630],    # RCB
        [564, 828],    # RB
        [840, 270],    # LM
        [840, 450],    # LCM
        [840, 630],    # RCM
        [840, 810],    # RM
        [1200, 450],   # LST
        [1200, 630],   # RST
      ]}

    case "4-4-2 Diamond":
      # Variation of 4-4-2 with diamond-shaped midfield
      return {"blue": [
        [1740, 540],   # GK
        [1464, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1464, 828],   # RB
        [1250, 540],   # DM (Defensive Midfielder)
        [1080, 450],   # LCM
        [1080, 630],   # RCM
        [910, 540],    # AM (Attacking Midfielder)
        [720, 450],    # LST
        [720, 630],    # RST
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [456, 252],    # LB
        [456, 450],    # LCB
        [456, 630],    # RCB
        [456, 828],    # RB
        [670, 540],    # DM
        [840, 450],    # LCM
        [840, 630],    # RCM
        [1010, 540],   # AM
        [1200, 450],   # LST
        [1200, 630],   # RST
      ]}

    case "3-5-2":
      # Formation with three defenders and wing-backs
      return {"blue": [
        [1740, 540],   # GK
        [1464, 360],   # LCB
        [1464, 540],   # CB
        [1464, 720],   # RCB
        [1250, 252],   # LWB (Left Wing-Back)
        [1250, 828],   # RWB (Right Wing-Back)
        [1080, 360],   # LCM
        [1080, 540],   # CM
        [1080, 720],   # RCM
        [720, 450],    # LST
        [720, 630],    # RST
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [456, 360],    # LCB
        [456, 540],    # CB
        [456, 720],    # RCB
        [670, 252],    # LWB
        [670, 828],    # RWB
        [840, 360],    # LCM
        [840, 540],    # CM
        [840, 720],    # RCM
        [1200, 450],   # LST
        [1200, 630],   # RST
      ]}

    case "3-4-3":
      # Attacking formation with three forwards
      return {"blue": [
        [1740, 540],   # GK
        [1464, 360],   # LCB
        [1464, 540],   # CB
        [1464, 720],   # RCB
        [1080, 270],   # LM
        [1080, 450],   # LCM
        [1080, 630],   # RCM
        [1080, 810],   # RM
        [720, 270],    # LW
        [720, 540],    # ST
        [720, 810]     # RW
      ], "red": [        # Mirror positions for red team
        [180, 540],    # GK
        [456, 360],    # LCB
        [456, 540],    # CB
        [456, 720],    # RCB
        [840, 270],    # LM
        [840, 450],    # LCM
        [840, 630],    # RCM
        [840, 810],    # RM
        [1200, 270],   # LW
        [1200, 540],   # ST
        [1200, 810]    # RW
      ]}
