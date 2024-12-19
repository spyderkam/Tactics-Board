
#!/user/bin/env python3

__author__ = "spyderkam"

# Colors
BLUE = (0, 0, 255)
GREEN = (50, 168, 82)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def formation(formation_type):
  match formation_type:
    case "433":
      return {"blue": [
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
      ], "red": [
        [1740, 540],   # GK
        [1356, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1356, 828],   # RB
        [1080, 360],   # LCM
        [1080, 540],   # CM
        [1080, 720],   # RCM
        [720, 270],    # LW
        [720, 540],    # ST
        [720, 810],    # RW
      ]}
        
    case "4231":
      return {"blue": [
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
        [1440, 540],   # ST
      ], "red": [
        [1740, 540],   # GK
        [1356, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1356, 828],   # RB
        [1080, 450],   # LDM
        [1080, 630],   # RDM
        [720, 270],    # LAM
        [720, 540],    # CAM
        [720, 810],    # RAM
        [480, 540],    # ST
      ]}

    case "442":
      return {"blue": [
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
      ], "red": [
        [1740, 540],   # GK
        [1356, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1356, 828],   # RB
        [1080, 270],   # LM
        [1080, 450],   # LCM
        [1080, 630],   # RCM
        [1080, 810],   # RM
        [720, 450],    # LST
        [720, 630],    # RST
      ]}
