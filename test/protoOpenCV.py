#Funcion para crear calculadora
from email.mime import image
import cv2
import numpy as np

nameWindow = "Calculadora"
found = False
size_image = 600

def nothing(x):
    pass

def constructorVentana():
    cv2.namedWindow(nameWindow)
    cv2.createTrackbar("min", nameWindow,0,255, nothing)
    cv2.createTrackbar("max", nameWindow, 100, 255, nothing)
    cv2.createTrackbar("kernel", nameWindow, 12, 100, nothing)
    cv2.createTrackbar("areaMin", nameWindow, 10000, 10000, nothing)

#Calcula el área o tamaño de las figuras
#Un cálculo basado en pixeles
def calcularAreas(figuras):
    areas=[]
    for figuraActual in figuras:
        areas.append(cv2.contourArea(figuraActual))
    return areas

def mostrarTexto(mensaje, imagen, figuraActual):
    cv2.putText(imagen, mensaje, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.drawContours(imagen, [figuraActual], 0, (0, 0, 255), 2)

def detectarForma(imagen):
    global found
    #sacamos los mínimos y los máximos
    min = cv2.getTrackbarPos("min", nameWindow)
    max = cv2.getTrackbarPos("max", nameWindow)
    tamañoKernel = cv2.getTrackbarPos("kernel", nameWindow)

    #Como la imagen llega a color tenemos que aplanarla
    imagenGris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #Convierte a escala de grises
    imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)  # Convierte a HSV
    #cv2.imshow("gris", imagenGris)

    #vamos a detectar bordes
    bordes = cv2.Canny(imagenGris, min, max)
    kernel = np.ones((tamañoKernel, tamañoKernel), np.uint8)
    bordes = cv2.dilate(bordes, kernel)
    # cv2.imshow("Bordes", bordes)

    #Detección de la figura, cierre de los polígonos
    #Las jerarquías son como si hay figuras dentro de otras
    figuras, jerarquia = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = calcularAreas(figuras)
    areaMin = cv2.getTrackbarPos("areaMin", nameWindow)


    
    #A continuación hacemos un análisis de cada uno de los elementos que hay en
    #la lista de figuras y también si es una figura relevante
    i = 0
    cropped_contour = bordes
    for figuraActual in figuras:
        if(found == False):
            cropped_contour = bordes

        if areas[i] >= areaMin:
            i = i+1
            #Esta operación toma la figura y analiza la cantidad de vértices
            #y dependiendo de estos se puede determinarque figura es
            vertices = cv2.approxPolyDP(figuraActual, 0.05 * cv2.arcLength(figuraActual, True), True)
            
            if len(vertices) == 4:
                x,y,w,h = cv2.boundingRect(figuraActual)
                cropped_contour = imagen[y:y+h, x:x+w]
                if(y+h < size_image and x+w < size_image):
                    found = True
                    cv2.imwrite("recorte.jpg", cropped_contour)
                #imagen = cv2.imread("recorte.jpg")
                #mostrarTexto(f"{x} {y} {w} {h}", imagen, figuraActual)

    return cropped_contour


#Apertura de la cámara
video = cv2.VideoCapture(0)
bandera = True
constructorVentana()

while bandera:
    _,imagen = video.read() #El guión bajo es para desechar otro parámetro que devuelve el .read
    imagen = detectarForma(imagen)
    if(len(imagen) != None):
        cv2.imshow("imagen", imagen)

    #parar el programa
    #detectamos la tecla que el usuario presione para eso
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        bandera = False

#Cuando se termine el ciclo se debe cerrar el video y además cerrar las ventanas
video.release()
cv2.destroyAllWindows()