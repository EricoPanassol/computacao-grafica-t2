from Triangulo import Triangulo
from Ponto import Ponto
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Objeto3D:   
    def __init__(self):
        self.faces = []
        self.nFaces = 0

    def LeObjeto(self, nome):
        try:
            arq = open(nome, 'r')
            self.faces = []
            
            self.nFaces = int(arq.readline().strip())
            for i in range(self.nFaces):
                line = arq.readline().strip().split()
                print(i, line)
                x1, y1, z1,x2,y2,z2,x3,y3,z3 = map(float, line[:9])
                p1 = Ponto(x1, y1, z1)
                p2 = Ponto(x2, y2, z2)
                p3 = Ponto(x3, y3, z3)
                
                face = Triangulo(p1, p2, p3)
                self.faces.append(face)
                #print(len(self.faces) - 1, ": ", end="")
                #face.imprime()
                
            arq.close()
        except IOError:
            print("Erro na abertura do arquivo", nome, ".")

    def ImprimeObjeto(self):
        for i,t in enumerate(self.faces):
            print(f"Face {i}")
            t.imprime()

    def ExibeObjeto(self,ponto,angulo):
        glColor4f(1,1,1,1)

        glPushMatrix()
        glTranslatef(ponto.x,ponto.y+0.5,ponto.z)
        glRotatef(angulo,0,1,0)
        glScalef(1,1,1)
        glRotatef(270,0,1,0)
        # desenha QUAD preenchido
        for t in self.faces:
            
            glBegin ( GL_TRIANGLES )            
            glNormal3f(t.normal.x,t.normal.y,t.normal.z)
            glVertex3f(t.p1.x,  t.p1.y, t.p1.z)
            glVertex3f(t.p2.x,  t.p2.y, t.p2.z)
            glVertex3f(t.p3.x,  t.p3.y, t.p3.z)
            glEnd()

        glPopMatrix()




