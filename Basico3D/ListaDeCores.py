#include "ListaDeCoresRGB.h"

#https://community.khronos.org/t/color-tables/22518/5

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


Cores = [
    [0,0,0],
    [1,1,1],
    [0.5,0.5,0.5],
    [1,1,0],
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [0.439216,0.858824,0.576471],
    [0.62352,0.372549,0.623529],
    [0.647059,0.164706,0.164706],
    [0.372549,0.623529,0.623529],
    [1,0.498039,0],
    [0.258824,0.258824,0.435294],
    [0.184314,0.309804,0.184314],
    [0.309804,0.309804,0.184314],
    [0.6,0.196078,0.8],
    [0.419608,0.137255,0.556863],
    [0.184314,0.309804,0.309804],
    [0.184314,0.309804,0.309804],
    [0.439216,0.576471,0.858824],
    [0.556863,0.137255,0.137255],
    [0.137255,0.556863,0.137255],
    [0.8,0.498039,0.196078],
    [0.858824,0.858824,0.439216],
    [0.576471,0.858824,0.439216],
    [0.309804,0.184314,0.184314],
    [0.623529,0.623529,0.372549],
    [0.74902,0.847059,0.847059],
    [0.560784,0.560784,0.737255],
    [0.196078,0.8,0.196078],
    [0.556863,0.137255,0.419608],
    [0.196078,0.8,0.6],
    [0.196078,0.196078,0.8],
    [0.419608,0.556863,0.137255],
    [0.917647,0.917647,0.678431],
    [0.576471,0.439216,0.858824],
    [0.258824,0.435294,0.258824],
    [0.498039,0,1],
    [0.498039,1,0],
    [0.439216,0.858824,0.858824],
    [0.858824,0.439216,0.576471],
    [0.184314,0.184314,0.309804],
    [0.137255,0.137255,0.556863],
    [0.137255,0.137255,0.556863],
    [1,0.5,0],
    [1,0.25,0],
    [0.858824,0.439216,0.858824],
    [0.560784,0.737255,0.560784],
    [0.737255,0.560784,0.560784],
    [0.917647,0.678431,0.917647],
    [0.435294,0.258824,0.258824],
    [0.137255,0.556863,0.419608],
    [0.556863,0.419608,0.137255],
    [0.196078,0.6,0.8],
    [0,0.498039,1],
    [0,1,0.498039],
    [0.137255,0.419608,0.556863],
    [0.858824,0.576471,0.439216],
    [0.847059,0.74902,0.847059],
    [0.678431,0.917647,0.917647],
    [0.309804,0.184314,0.309804],
    [0.8,0.196078,0.6],
    [0.847059,0.847059,0.74902],
    [0.6,0.8,0.196078],
    [0.22,0.69,0.87],
    [0.35,0.35,0.67],
    [0.71,0.65,0.26],
    [0.72,0.45,0.2],
    [0.55,0.47,0.14],
    [0.65,0.49,0.24],
    [0.9,0.91,0.98],
    [0.85,0.85,0.1],
    [0.81,0.71,0.23],
    [0.82,0.57,0.46],
    [0.85,0.85,0.95],
    [1,0.43,0.78],
    [0.53,0.12,0.47],
    [0.3,0.3,1],
    [0.85,0.53,0.1],
    [0.89,0.47,0.2],
    [0.91,0.76,0.65],
    [0.65,0.5,0.39],
    [0.52,0.37,0.26],
    [1,0.11,0.68],
    [0.42,0.26,0.15],
    [0.36,0.2,0.09],
    [0.96,0.8,0.69],
    [0.92,0.78,0.62],
    [0,0,0.61],
    [0.35,0.16,0.14],
    [0.36,0.25,0.2],
    [0.59,0.41,0.31],
    [0.32,0.49,0.46],
    [0.29,0.46,0.43],
    [0.52,0.39,0.39],
    [0.13,0.37,0.31],
    [0.55,0.09,0.09],
    [0.73,0.16,0.96],
    [0.87,0.58,0.98],
    [0.94,0.81,0.99]
]

Black = 0
White = 1
Gray = 2
Yellow = 3
Red = 4
Green = 5
Blue = 6
Aquamarine = 7
BlueViolet = 8
Brown = 9
CadetBlue = 10
Coral = 11
CornflowerBlue = 12
DarkGreen = 13
DarkOliveGreen = 14
DarkOrchid = 15
DarkSlateBlue = 16
DarkSlateGray = 17
DarkSlateGrey = 18
DarkTurquoise = 19
Firebrick = 20
ForestGreen = 21
Gold = 22
Goldenrod = 23
GreenYellow = 24
IndianRed = 25
Khaki = 26
LightBlue = 27
LightSteelBlue = 28
LimeGreen = 29
Maroon = 30
MediumAquamarine = 31
MediumBlue = 32
MediumForestGreen = 33
MediumGoldenrod = 34
MediumOrchid = 35
MediumSeaGreen = 36
MediumSlateBlue = 37
MediumSpringGreen = 38
MediumTurquoise = 39
MediumVioletRed = 40
MidnightBlue = 41
Navy = 42
NavyBlue = 43
Orange = 44
OrangeRed = 45
Orchid = 46
PaleGreen = 47
Pink = 48
Plum = 49
Salmon = 50
SeaGreen = 51
Sienna = 52
SkyBlue = 53
SlateBlue = 54
SpringGreen = 55
SteelBlue = 56
Tan = 57
Thistle = 58
Turquoise = 59
Violet = 60
VioletRed = 61
Wheat = 62
YellowGreen = 63
SummerSky = 64
RichBlue = 65
Brass = 66
Copper = 67
Bronze = 68
Bronze2 = 69
Silver = 70
BrightGold = 71
OldGold = 72
Feldspar = 73
Quartz = 74
NeonPink = 75
DarkPurple = 76
NeonBlue = 77
CoolCopper = 78
MandarinOrange = 79
LightWood = 80
MediumWood = 81
DarkWood = 82
SpicyPink = 83
SemiSweetChoc = 84
BakersChoc = 85
Flesh = 86
NewTan = 87
NewMidnightBlue = 88
VeryDarkBrown = 89
DarkBrown = 90
DarkTan = 91
GreenCopper = 92
DkGreenCopper = 93
DustyRose = 94
HuntersGreen = 95
Scarlet = 96
Med_Purple = 97
Light_Purple = 98
Very_Light_Purple = 99
# LAST_COLOR = Cores[100]


def defineCor(c):
    # glColor3fv(Cores[c])
    glColor3f(Cores[c][0], Cores[c][1], Cores[c][2])

						
