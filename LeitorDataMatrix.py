import cv2
from pylibdmtx.pylibdmtx import decode
import sys
import os
import time

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
serial_log = os.path.join(script_dir, 'SERIAL.LOG')

camLigado = True
startCont = 0 
startCont =  time.time()

if os.path.exists(serial_log):
    os.remove(serial_log)

def readDataMatrix(cam):
    global camLigado
    
    while camLigado:
        try:
            ret, frame = cam.read()
            if not ret:
                print("Falha ao capturar imagem da câmera.")
                break
          
            x,y,h,w = (656, 401 , 264, 224) 
            cutQR = frame[y:y+w, x:x+h]

            cv2.imshow("Data Matrix Detected", cutQR)
            cv2.waitKey(1)
          
            gray_image = cv2.cvtColor(cutQR, cv2.COLOR_BGR2GRAY)

            decoded_objects = decode(gray_image)

            if (time.time() >= startCont + 12):
                camLigado = False
                with open(serial_log, 'w') as file:
                    file.write("FAIL")
                camLigado = False      

            if decoded_objects:

                for obj in decoded_objects: 

                    serial = obj.data.decode('utf-8') 
                    print("Serial:", serial)
                    
                    with open(serial_log, 'w') as file:
                            file.write(serial)
                        
                    camLigado = False
                            
        except Exception as e:
            print("Erro ao ler data matrix :", e)
    
    cam.release()
    cv2.destroyAllWindows()

def captureImage():
    capturaImage = cv2.VideoCapture(0, cv2.CAP_DSHOW) 


    capturaImage.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capturaImage.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
    capturaImage.set(cv2.CAP_PROP_FOCUS,  190)
    readDataMatrix(capturaImage)

    
captureImage()







