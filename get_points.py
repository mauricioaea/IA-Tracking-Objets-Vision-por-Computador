# Importamos librerias
import cv2

def run(im, multi=False):
    # aqui creo 2 copias de visualización- cuando le damos a la letra (p) se abren 2 ventanas, en una selecciono el objeto que quiero identificar
    # en la otra confirmo que quiero seleccionar ese objeto,por que puedo volver a seleccionar otro objeto si yo quiero. 
    im_disp = im.copy()
    im_draw = im.copy()
    window_name = "Selecciona el objeto para hacerle seguimiento."
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, im_draw)
    # creo las siguientes listas  en la parte superior izquierda y la parte inferior derecha para recortar la imagen.
    pts_1 = []
    pts_2 = []
    rects = []



    # A partire de aqui lo que voy hacer es llamar a los eventos del MOUSE, con el fin de que seleccionemos con el MOUSE el PUNTO INICIAL o el PUNTO FINAL
    # de nuestro rectangulo o cuadrado donde esta el objeto que quiero restrear 
    run.mouse_down = False
    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
         run.mouse_down = True
         pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            print ("Objecto seleccionado en[{}, {}]".format(pts_1[-1], pts_2[-1]))
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = im.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (0,255,0), 3)
            cv2.imshow(window_name, im_draw)
    print ("Presione y suelte el mouse alrededor del objeto a ser rastreado.")
    cv2.setMouseCallback(window_name, callback)
    print ("Presione la tecla 'p' para continuar con los puntos seleccionados ")
    print ("Presione la tecla 'd' para descartar el último objeto seleccionado. ")
    print ("Presione la tecla 'q' para salir del programa ")
    while True:
        # dibujo el rectangulo en la imagen que quiero rastrer
        window_name_2 = "Objects to be tracked."
        for pt1, pt2 in zip(pts_1, pts_2):
            rects.append([pt1[0],pt2[0], pt1[1], pt2[1]])
            cv2.rectangle(im_disp, pt1, pt2, (255, 0, 0), 3)
        #muestra las imagenes cortadas
        cv2.namedWindow(window_name_2, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name_2, im_disp)
        key = cv2.waitKey(30)
        if key == ord('p'):
            # Presiona 's' para volvel a seleccionar los puntos
            cv2.destroyAllWindows()
            point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
            corrected_point=check_point(point)
            return corrected_point
        elif key == ord('q'):
            # Presiona 'q' para salir del programa
            print ("Eliminando sin guardar.")
            exit()
        elif key == ord('d'):
            # Presionna 'd' para borrar y cambiar el rectangulo de seguimiento
            if run.mouse_down == False and pts_1:
                print ("Objecto borrado en  [{}, {}]".format(pts_1[-1], pts_2[-1]))
                pts_1.pop()
                pts_2.pop()
                im_disp = im.copy()
            else:
                print ("No objecto para borrar.")
    cv2.destroyAllWindows()
    point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
    corrected_point=check_point(point)
    return corrected_point
def check_point(points):
    out=[]
    for point in points:
        #para encontrar min y max de las coordenadas en x
        if point[0]<point[2]:
            minx=point[0]
            maxx=point[2]
        else:
            minx=point[2]
            maxx=point[0]
        #para encontrar min y max de las coordenadas en y
        if point[1]<point[3]:
            miny=point[1]
            maxy=point[3]
        else:
            miny=point[3]
            maxy=point[1]
        out.append((minx,miny,maxx,maxy))
    return out
if __name__ == "__main__":
    points = run(im)