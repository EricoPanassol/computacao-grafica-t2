# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
# 
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# 
# ***********************************************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
#from PIL import Image
import time
import math


Angulo = 0.0
Angulo_Carro = 0.0
Pos_Carro = Ponto(0,0,5)
alvo = Ponto(0,0,0)
observador = Ponto(0, 2, 10)
thirdPerson = False
upView = False
turning = 0
moving = False
# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #image = Image.open("Tex.png")
    #print ("X:", image.size[0])
    #print ("Y:", image.size[1])
    #image.show()
    
   

# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
	# Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
	# Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)
    
    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4] 
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0 ]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)

# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCubo():
    glutSolidCube(1)
    
def PosicUser():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    
    gluPerspective(60,AspectRatio,0.01,50) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #gluLookAt(observador.x, observador.y+2, observador.z, alvo.x,alvo.y,alvo.z, 0,1.0,0) 

    if(thirdPerson):
        gluLookAt(observador.x, observador.y+2, observador.z+3, alvo.x,alvo.y,alvo.z, 0,1.0,0) 
    elif(upView):
        gluLookAt(0,20,0.1, 0,0,0,  0,1,0)
    else:
        gluLookAt(observador.x, observador.y, observador.z, alvo.x,alvo.y,alvo.z, 0,1.0,0)

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    glColor3f(0,0,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glVertex3f(-5,  0.0, -5)
    glVertex3f(-5,  0.0,  5)
    glVertex3f( 5,  0.0,  5)
    glVertex3f( 5,  0.0, -5)
    glEnd()
    
    glColor3f(1,1,1) # desenha a borda da QUAD 
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(-5,  0.0, -5)
    glVertex3f(-5,  0.0,  5)
    glVertex3f( 5,  0.0,  5)
    glVertex3f( 5,  0.0, -5)
    glEnd()
    
# **********************************************************************
def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20,-1,-10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 10)
        glPopMatrix()
        glTranslated(10, 0, 0)
    glPopMatrix()     


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    global Angulo
    global Angulo_Carro
    global moving
    global turning
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    DefineLuz()
    PosicUser()

    glMatrixMode(GL_MODELVIEW)
    
    DesenhaPiso()
    glColor3f(0.5,0.0,0.0) # Vermelho
    glPushMatrix()
    glTranslatef(-2,0,0)
    glRotatef(Angulo,0,1,0)
    DesenhaCubo()
    glPopMatrix()
    
    glColor3f(0.5,0.5,0.0) # Amarelo
    glPushMatrix()
    glTranslatef(2,0,0)
    glRotatef(-Angulo,0,1,0)
    DesenhaCubo()
    glPopMatrix()

    Angulo = Angulo + 1

    glColor3f(0.5,1,0.9) 
    glPushMatrix()
    glTranslatef(alvo.x, 0.0, alvo.z)
    DesenhaCubo()
    glPopMatrix()

    #car
    glColor3f(1,0,1)
    glPushMatrix()
    glTranslatef(Pos_Carro.x,Pos_Carro.y,Pos_Carro.z)
    glRotatef(Angulo_Carro,0,1,0)
    DesenhaCubo()
    glPopMatrix()

    #car do eriquin
    glColor3f(1,1,1)
    glPushMatrix()
    glTranslatef(observador.x,-0.1,observador.z)
    DesenhaCubo()
    glPopMatrix()

    if(moving):
        moveForward(1)

    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global image
    global moving
    global turning
    global Angulo_Carro
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        init()

    if args[0] == b'i':
        image.show()

    if args[0] == b'w':
        moveForward(1)
    
    if args[0] == b'd':
        rotaciona_alvo(-10)
        rotaciona_observador(-10)
        Angulo_Carro = Angulo_Carro + 10*-1

    if args[0] == b'a':
        rotaciona_alvo(10)
        rotaciona_observador(10)
        Angulo_Carro = Angulo_Carro + 10*1

    if args[0] == b's':
        moveBackward(1)

    if args[0] == b' ':
        moving = not moving
        
    print(args)
    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global alvo, thirdPerson, upView

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        thirdPerson = not thirdPerson
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        upView = not upView
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:       # Se pressionar RIGHT
        pass
    glutPostRedisplay()

def moveForward(fator):
    global alvo
    global observador
    global Pos_Carro
    
    vetor_alvo = alvo.__sub__(Pos_Carro)
    alvo = alvo.__add__(vetor_alvo.versor().__mul__(fator))
    Pos_Carro = Pos_Carro.__add__(vetor_alvo.versor().__mul__(fator))
    print(f"ALVO NP: x: {alvo.x},y: {alvo.y},z: {alvo.z}")
    observador = observador.__add__(vetor_alvo.versor().__mul__(fator))
    print(f"OBSERVADOR NP: x: {observador.x},y: {observador.y},z: {observador.z}")
    

def moveBackward(fator):
    global alvo
    global observador
    global Pos_Carro
    
    vetor_alvo = alvo.__sub__(Pos_Carro)
    alvo = alvo.__sub__(vetor_alvo.versor().__mul__(fator))
    Pos_Carro = Pos_Carro.__sub__(vetor_alvo.versor().__mul__(fator))
    print(f"ALVO NP: x: {alvo.x},y: {alvo.y},z: {alvo.z}")
    observador = observador.__sub__(vetor_alvo.versor().__mul__(fator))
    print(f"OBSERVADOR NP: x: {observador.x},y: {observador.y},z: {observador.z}")
    

def rotaciona_alvo(angulo_cam):
    global alvo
    global observador
    global atual_vetor_alvo
    global Pos_Carro

    vetor_alvo = alvo.__sub__(Pos_Carro)
    vetor_alvo.rotacionaY(angulo_cam)

    alvo = Pos_Carro.__add__(vetor_alvo)


def rotaciona_observador(angulo_cam):
    global alvo
    global observador
    global Pos_Carro

    vetor_alvo = observador.__sub__(Pos_Carro)
    vetor_alvo.rotacionaY(angulo_cam)

    observador = Pos_Carro.__add__(vetor_alvo)

def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()


        
# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL 3D")

# executa algumas inicializaÃ§Ãµes
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
