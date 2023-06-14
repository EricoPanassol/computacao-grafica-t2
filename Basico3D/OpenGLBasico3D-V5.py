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
from copy import copy
import numpy as np
from PIL import Image
import random
import os.path
import time
import math

Angulo = 0.0
Angulo_Carro = 0.0
Pos_Carro = Ponto(5,0,20)
alvo = Ponto(Pos_Carro.x,0,Pos_Carro.z+5)
alvo_camera = Ponto(0,0,0)
observador = Ponto(0, 4, 13)
moving = False
camera_view = 0
Texturas = []
gasolinas_no_mapa = 0
gasolinas = []
tanque = 100
# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(76/256, 169/256, 250/256, 1.0)

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

def enche_tanque():
    global tanque

    if tanque + 10 > 100:
        tanque = 100
        return
    
    tanque += 10


def DesenhaCubo():
    glutSolidCube(1)
    
def PosicUser():
    global camera_view, observador, alvo, Pos_Carro, alvo_camera

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    
    gluPerspective(60,AspectRatio,0.01,1000) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #gluLookAt(observador.x, observador.y+2, observador.z, alvo.x,alvo.y,alvo.z, 0,1.0,0) 

    if camera_view == 0:
        vetor_alvo = alvo.__sub__(Pos_Carro)
        vetor_alvo = vetor_alvo.__mul__(1.5)

        obs_pos = Pos_Carro.__sub__(vetor_alvo)
        alvo_camera.x = alvo.x
        alvo_camera.z = alvo.z
        observador = Ponto(obs_pos.x, obs_pos.y+3, obs_pos.z)
    
    elif camera_view == 1:
        alvo_camera.x = alvo.x
        alvo_camera.z = alvo.z
        observador = Ponto(Pos_Carro.x,Pos_Carro.y+100,Pos_Carro.z)

    elif camera_view == 2:
        alvo_camera.x = alvo.x
        alvo_camera.z = alvo.z
        observador = Ponto(Pos_Carro.x,Pos_Carro.y+1,Pos_Carro.z)

    elif camera_view == 3:
        alvo_camera.x = 225
        alvo_camera.y = 1
        alvo_camera.z = 225
        observador = Ponto(225,390,224)

    gluLookAt(observador.x, observador.y, observador.z, alvo_camera.x,alvo_camera.y,alvo_camera.z, 0,1.0,0)

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    glColor3f(0.5,0.5,0.5) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(0,  0.0, 0)
    glTexCoord(0,1)
    glVertex3f(0,  0.0,  15)
    glTexCoord(1,1)
    glVertex3f( 15,  0.0,  15)
    glTexCoord(1,0)
    glVertex3f( 15,  0.0, 0)
    glEnd()
    
    # glColor3f(1,1,1) # desenha a borda da QUAD 
    # glBegin ( GL_LINE_STRIP )
    # glNormal3f(0,1,0)
    # glVertex3f(-7.5,  0.0, -7.5)
    # glVertex3f(-7.5,  0.0,  7.5)
    # glVertex3f( 7.5,  0.0,  7.5)
    # glVertex3f( 7.5,  0.0, -7.5)
    # glEnd()
    
# **********************************************************************
def DesenhaPiso():
    glPushMatrix()
    glTranslated(0,-1,0)
    for x in range(-15, 15):
        glPushMatrix()
        for z in range(-15, 15):
            UseTexture((matrizMapa[z+15][x+15]))
            DesenhaLadrilho()
            glTranslated(0, 0, 15)
        glPopMatrix()
        glTranslated(15, 0, 0)
    glPopMatrix()     

def lerMatriz(arquivo):
    matriz = []
    with open(os.path.dirname(__file__) + arquivo, 'r') as file:
        linhas = file.readlines()
        for linha in linhas[1:]:
            elementos = linha.strip().split()
            matriz.append([int(elemento) for elemento in elementos])
    return matriz

def LoadTexture(nome) -> int:
    # carrega a imagem
    image = Image.open(nome)
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL 
    img_data = np.array(list(image.getdata()), np.uint8)

    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION: 
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()
    return texture

def UseTexture (NroDaTextura: int):
    global Texturas
    if (NroDaTextura>len(Texturas)):
        print ("Numero invalido da textura.")
        glDisable (GL_TEXTURE_2D)
        return
    if (NroDaTextura < 0):
        glDisable (GL_TEXTURE_2D)
    else:
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, Texturas[NroDaTextura])

def testaColisao(proxima_pos):
    pos_x_matriz = proxima_pos.x/15
    pos_z_matriz = proxima_pos.z/15

    print(f"pos x: {pos_x_matriz}\npos z: {pos_z_matriz}\n")
    
    if pos_x_matriz >= 30 or pos_x_matriz <= 0:
        return True

    if pos_z_matriz >= 30 or pos_z_matriz <= 0:
        return True

    if matrizMapa[int(pos_z_matriz)][int(pos_x_matriz)] == 0 or matrizMapa[int(pos_x_matriz)][int(pos_z_matriz)] > 12:
        return True
    
    return False

def spawn_gasolina():
    global matrizMapa, gasolinas_no_mapa, gasolinas

    while gasolinas_no_mapa < 5:
        x_gasolina = random.randint(1,449)
        z_gasolina = random.randint(1,449)

        x_gas_abs = int(x_gasolina/15)
        z_gas_abs = int(z_gasolina/15)

        if matrizMapa[z_gas_abs][x_gas_abs] > 0 and matrizMapa[z_gas_abs][x_gas_abs] <= 12:
            nova_gasolina = Ponto(x_gasolina,0,z_gasolina)
            gasolinas.append(nova_gasolina)
            gasolinas_no_mapa += 1
            print(f"Galão de gasolina spawnado em x:{nova_gasolina.x} z:{nova_gasolina.z}")
    


def get_gasolina():
    global gasolinas_no_mapa, tanque

    for gas in gasolinas:
        if int(gas.x/15) == int(Pos_Carro.x/15) and int(gas.z/15) == int(Pos_Carro.z/15):
            gasolinas.remove(gas)
            gasolinas_no_mapa -= 1
            tanque += 10
            print("PLIM gasalina c:")
            return
        
def desenha_gasolinas():
    for gas in gasolinas:
        glColor3f(1,0,0)
        glPushMatrix()
        glTranslatef(gas.x,gas.y,gas.z)
        DesenhaCubo()
        glPopMatrix()
        
    

def printMatriz(matriz):
    for linha in matriz:
        print(linha)
# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    global Angulo
    global Angulo_Carro
    global moving
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    DefineLuz()
    PosicUser()
    spawn_gasolina()

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

    # glColor3f(0.5,1,0.9) 
    # glPushMatrix()
    # glTranslatef(alvo.x, 0.0, alvo.z)
    # DesenhaCubo()
    # glPopMatrix()

    #car
    glColor3f(1,0,1)
    glPushMatrix()
    glTranslatef(Pos_Carro.x,Pos_Carro.y,Pos_Carro.z)
    glRotatef(Angulo_Carro,0,1,0)
    DesenhaCubo()
    glPopMatrix()

    desenha_gasolinas()
    #car do eriquin
    # glColor3f(1,1,1)
    # glPushMatrix()
    # glTranslatef(observador.x,-0.1,observador.z)
    # DesenhaCubo()
    # glPopMatrix()

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
    global Angulo_Carro
    global alvo_camera

    var_angulo = 15
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
        rotaciona_alvo(-var_angulo)
        rotaciona_observador(-var_angulo)
        Angulo_Carro = Angulo_Carro + var_angulo*-1

    if args[0] == b'a':
        rotaciona_alvo(var_angulo)
        rotaciona_observador(var_angulo)
        Angulo_Carro = Angulo_Carro + var_angulo*1

    if args[0] == b's':
        moveBackward(1)

    if args[0] == b' ':
        moving = not moving

    if args[0] == b'u':
        alvo_camera.y += 1

    if args[0] == b'j':
        alvo_camera.y -= 1

        
    print(args)
    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global alvo, matrizMapa

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        change_camera_view()
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        printMatriz(matrizMapa)
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
    global moving
    global tanque

    if tanque > 0:
        vetor_alvo = alvo.__sub__(Pos_Carro)
        nova_pos_alvo = alvo.__add__(vetor_alvo.versor().__mul__(fator))
        nova_pos_car = Pos_Carro.__add__(vetor_alvo.versor().__mul__(fator))
        nova_pos_obs = observador = observador.__add__(vetor_alvo.versor().__mul__(fator))

        colided = testaColisao(nova_pos_car)
        get_gasolina()
            
        if colided:
            moving = False   
            return

        alvo = nova_pos_alvo
        Pos_Carro = nova_pos_car
        observador = nova_pos_obs

        tanque -= 0.1

        Pos_Carro.imprime()
    

def moveBackward(fator):
    global alvo
    global observador
    global Pos_Carro
    
    vetor_alvo = alvo.__sub__(Pos_Carro)
    alvo = alvo.__sub__(vetor_alvo.versor().__mul__(fator))
    Pos_Carro = Pos_Carro.__sub__(vetor_alvo.versor().__mul__(fator))
    observador = observador.__sub__(vetor_alvo.versor().__mul__(fator))
    

def change_camera_view():
    global camera_view

    camera_view += 1 

    if camera_view == 4:
        camera_view = 0

    print(f"Camera View: {camera_view}")
        

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

def testaColisaoCarro():
    global Pos_Carro
        
# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

matrizMapa = lerMatriz("/Textures/Mapa1.txt")

#Texturas.append(LoadTexture("/Textures/NADA.png"))

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

Texturas.append(LoadTexture("Textures/GRASS.jpg"))
Texturas.append(LoadTexture("Textures/CROSS.jpg"))
Texturas.append(LoadTexture("Textures/DL.jpg"))
Texturas.append(LoadTexture("Textures/DLR.jpg"))
Texturas.append(LoadTexture("Textures/DR.jpg"))
Texturas.append(LoadTexture("Textures/LR.jpg"))
Texturas.append(LoadTexture("Textures/None.jpg"))
Texturas.append(LoadTexture("Textures/UD.jpg"))
Texturas.append(LoadTexture("Textures/UDL.jpg"))
Texturas.append(LoadTexture("Textures/UDR.jpg"))
Texturas.append(LoadTexture("Textures/UL.jpg"))
Texturas.append(LoadTexture("Textures/ULR.jpg"))
Texturas.append(LoadTexture("Textures/UR.jpg"))

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
