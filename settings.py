import glm
import numpy as np
import math

# Window
W_WIDTH = 1280
W_HEIGHT = 720
RESOLUTION = (W_WIDTH, W_HEIGHT)
TITLE = "Cubegame"
VSYNC = False
RESIZEABLE = False
GL_VERSION = (3, 3)

# Camera
ASPECT_RATIO = W_WIDTH / W_HEIGHT
FOV = 60
V_FOV = glm.radians(FOV)
H_FOV = 2 * glm.atan(glm.tan(V_FOV * 0.5) * ASPECT_RATIO)
NEAR = 0.1
FAR = 1000.0
PITCH_MAX = glm.radians(89.0)


# Chunk
SIZE = 16
HEIGHT = 64
SPHERE_RADIUS = math.sqrt(2) * SIZE * 0.5
AREA = SIZE * SIZE
VOLUME = AREA * HEIGHT