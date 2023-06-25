# ************************************************
#   TPoint.py
#   Define a classe TPoint
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

import math

""" Classe TPoint """
class TPoint:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    
    def subtract(self, other):
        return TPoint(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other):
        return TPoint(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)
        
    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length
        self.z /= length

    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            print (msg, self.x, self.y, self.z)
        else:
            print (self.x, self.y, self.z)

    """ Define os valores dos eixos do ponto """
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
# Definicao de operadores
# https://www.programiz.com/python-programming/operator-overloading
    def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
            return TPoint(x, y, z)

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return TPoint(x,y,z)

    def __mul__(self, value: float):
            x = self.x * value
            y = self.y * value
            z = self.z * value
            return TPoint(x, y, z)
    
    def modulo(self):
        p = 2
        return math.sqrt(math.pow(self.x,p) + math.pow(self.y,p) + math.pow(self.z, p))

    def versor(self):
        m = TPoint.modulo(self)
        x = self.x/m
        y = self.y/m
        z = self.z/m
        return TPoint(x,y,z)

    def rotacionaY(self, angulo):
        anguloRad = angulo * math.pi/180.0
        xr =  self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        
        self.x = xr
        self.z = zr

# ********************************************************************** */
#                                                                        */
#  Calcula a interseccao entre 2 retas (no plano "XY" Z = 0)             */
#                                                                        */
# k : ponto inicial da reta 1                                            */
# l : ponto final da reta 1                                              */
# m : ponto inicial da reta 2                                            */
# n : ponto final da reta 2                                              */
# 
# Retorna:
# 0, se não houver interseccao ou 1, caso haja                                                                       */
# int, valor do parâmetro no ponto de interseção (sobre a reta KL)       */
# int, valor do parâmetro no ponto de interseção (sobre a reta MN)       */
#                                                                        */
# ********************************************************************** */
def intersec2d(k: TPoint, l: TPoint, m: TPoint, n: TPoint) -> (int, float, float):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: TPoint, l: TPoint, m: TPoint, n: TPoint)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: TPoint, l: TPoint, m: TPoint, n: TPoint) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

