import math 

import math

def angle_between_arrows(x1, y1, x2, y2, x3, y3, x4, y4):

    vector1 = (x2 - x1, y2 - y1)

    vector2 = (x4 - x3, y4 - y3)

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))

    angle_deg = math.degrees(angle_rad)

    return angle_deg

#Another attempt that "blends" the lines together
def blend(p1, p2, ALPHA):
    return (
        p1[0] * (1 - ALPHA) + p2[0] * ALPHA,
        p1[1] * (1 - ALPHA) + p2[1] * ALPHA,
    )