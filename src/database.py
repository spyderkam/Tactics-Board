
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
    case "4-3-3":
      return {"blue": [
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
      ], "red": [
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
      return {"blue": [
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
        [500, 540],    # ST
      ], "red": [
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
      return {"blue": [
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
      ], "red": [
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
      return {"blue": [
        [1740, 540],   # GK
        [1464, 252],   # LB
        [1464, 450],   # LCB
        [1464, 630],   # RCB
        [1464, 828],   # RB
        [1250, 540],   # DM
        [1080, 450],   # LCM
        [1080, 630],   # RCM
        [910, 540],    # AM
        [720, 450],    # LST
        [720, 630],    # RST
      ], "red": [
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
      return {"blue": [
        [1740, 540],   # GK
        [1464, 360],   # LCB
        [1464, 540],   # CB
        [1464, 720],   # RCB
        [1250, 252],   # LWB
        [1250, 828],   # RWB
        [1080, 360],   # LCM
        [1080, 540],   # CM
        [1080, 720],   # RCM
        [720, 450],    # LST
        [720, 630],    # RST
      ], "red": [
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
      ], "red": [
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
