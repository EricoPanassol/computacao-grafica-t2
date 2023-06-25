from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from TPoint import TPoint
import sys
import numpy as np

class TTriangle:
    def __init__(self, p1, p2, p3):
        self.P1 = p1
        self.P2 = p2
        self.P3 = p3

    def imprime(self):
        print("P1 ", end="")
        self.P1.imprime()
        print()
        print("P2 ", end="")
        self.P2.imprime()
        print()
        print("P3 ", end="")
        self.P3.imprime()
        print()
        

    def CalculaNormal(self):
        v1 = self.P2.subtract(self.P1)
        v2 = self.P3.subtract(self.P1)
        normal = v1.cross(v2)
        normal.normalize()
        return normal

