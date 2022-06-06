import cv2
import numpy as np
import os
import codificarEnviarImagen as cei

#Código para tomar las imagenes 
nameWindow = "Captura de imagen"
found = False # Bandera que indica si se encontró la figura
size_image = 1000 # Tamaño maximo en pixeles
seleccionadas = [None,None]

def nothing(x):
    pass

def constructorVentana():
    cv2.namedWindow(nameWindow)
    cv2.createTrackbar("min", nameWindow,50,255, nothing)
    cv2.createTrackbar("max", nameWindow, 255, 255, nothing)
    cv2.createTrackbar("kernel", nameWindow, 15, 100, nothing)
    cv2.createTrackbar("areaMin", nameWindow, 4000, 10000, nothing)

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

    #Detección de la figura, cierre de elos polígonos
    #Las jerarquías son como si hay figuras dentro de otras
    figuras, jerarquia = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = calcularAreas(figuras)
    areaMin = cv2.getTrackbarPos("areaMin", nameWindow)

    recortes = []
    des = 20

    #A continuación hacemos un análisis de cada uno de los elementos que hay en
    #la lista de figuras y también si es una figura relevante
    i = 0
    cropped_contour = bordes # Mientras no se encuentre la figura muestra solo la vista de contornos
    for figuraActual in figuras:
        if areas[i] >= areaMin:
            i = i+1
            #Esta operación toma la figura y analiza la cantidad de vértices
            #y dependiendo de estos se puede determinarque figura es
            vertices = cv2.approxPolyDP(figuraActual, 0.05 * cv2.arcLength(figuraActual, True), True)
            
            # Por cada area detectada solo usa la de 4 vertices
            if len(vertices) == 4:
                # A la figura que tiene un area determinada se le caputa sus coordenadas y dimensiones
                x,y,w,h = cv2.boundingRect(figuraActual)
                
                if(len(figuras)==1):
                    x += des
                    y += des
                    h -= des*2
                    w -= des*2
                # Se hace el recorte
                cropped_contour = imagen[y:y+h, x:x+w]
                recortes.append(cropped_contour)

                cv2.drawContours(imagen, [figuraActual], 0, (0, 0, 255), 2)
                # Si el recorte tiene una determinada caracteristica lo almacena
                if(y+h < size_image and x+w < size_image):
                    found = True
                    
                    #cv2.imwrite("recorte.jpg", cropped_contour)
                #imagen = cv2.imread("recorte.jpg")
                #mostrarTexto(f"{x+w} {y+h}", cropped_contour, figuraActual)

    for i in range(len(recortes)):
        #print(recortes[i].shape)
        cv2.imshow(f"ROI {i}", recortes[i])
        if(i == 0):
            cv2.moveWindow(f"ROI {i}", 40,30)
        else:
            cv2.moveWindow(f"ROI {i}", 400,30)

    if(len(recortes) == 1):
        seleccionadas[0] = recortes[0]

    if(len(recortes) == 2):
        seleccionadas[0] = recortes[0]
        seleccionadas[1] = recortes[1]

    return (imagen, None)

imagen_forma = None
#Apertura de la cámara
def abrirCamara():
    global found
    video = cv2.VideoCapture(0)
    roi = False
    bandera = True

    # Recorre la carpeta de imagenes para eliminar lo anterior
    test = os.listdir("./images/")
    for item in test:
        if item.endswith(".jpg"):
            os.remove(os.path.join("./images/", item))
    constructorVentana()

    number_image = 1
    while bandera:
        _,imagen = video.read() #El guión bajo es para desechar otro parámetro que devuelve el .read
        
        if(roi):
            found = False
            detectarForma(imagen)

        if(len(imagen) != None):
            cv2.imshow("imagen", imagen)

        #parar el programa
        #detectamos la tecla que el usuario presione para eso
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            bandera = False

        if k == ord('c'):
            roi = True

        if k == ord('e'):
            print(f"Fotos Capturadas")
            for s in seleccionadas:
                cv2.imwrite(f"./images/recorte{number_image}.jpg", s)
                number_image += 1

            '''
            #cv2.imwrite(f"./images/recorte{number_image}.jpg", imagen)
            cv2.imwrite(f"./images/recorte{number_image}.jpg", imagen_forma[1][0])
            number_image += 1
            if(len(imagen_forma[1]) > 1):
                cv2.imwrite(f"./images/recorte{number_image}.jpg", imagen_forma[1][1])
                number_image += 1'''
        
        if k == ord('s'):
            cei.codificarEnviar(number_image)
            bandera = False

    #Cuando se termine el ciclo se debe cerrar el video y además cerrar las ventanas
    video.release()
    cv2.destroyAllWindows()