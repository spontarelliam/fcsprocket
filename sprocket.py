from math import cos, sin, pi, acos, asin, atan, sqrt, radians

import sys
if sys.version_info.major >= 3:
    xrange = range

def CreateSprocket(P, N, Dr):
    """
    Create a sprocket

    w is the wirebuilder object (in which the sprocket will be constructed)
    """
    Ds = 1.0005 * Dr + 0.003
    R = Ds / 2
    A = 35 + 60/N
    B = 18 - 56 / N
    ac = 0.8 * Dr
    M = 0.8 * Dr * cos(radians(35) + radians(60)/N)
    T = 0.8 * Dr * sin(radians(35) + radians(60)/N)
    E = 1.3025 * Dr + 0.0015
    yz = Dr * (1.4 * sin(radians(17) - radians(64)/N) - 0.8 * sin(radians(18) - radians(56) / N))
    ab = 1.4 * Dr
    W = 1.4 * Dr * cos(radians(180) / N)
    V = 1.4 * Dr * sin(radians(180)/N)
    F = Dr * (0.8 * cos(radians(18) - radians(56)/N) + 1.4 * cos(radians(17) - radians(64) / N) - 1.3025) - 0.0015
    H = sqrt(F**2 - (1.4 * Dr - P/2) ** 2)
    S = P/2 * cos(radians(180)/N) + H * sin(radians(180)/N)
    PD = P / (sin(radians(180)/N))

    w.line(1)


def rotate(pt, rads):
    """
    rotate pt by rads radians about origin
    """
    sinA = sin(rads)
    cosA = cos(rads)
    return (pt[0] * cosA - pt[1] * sinA,
            pt[0] * sinA + pt[1] * cosA)

def in_to_mm(inch):
    return inch / 0.03937008
