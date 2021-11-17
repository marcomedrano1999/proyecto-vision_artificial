import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from google.protobuf.json_format import MessageToDict
from datetime import datetime
import os
from os import path
import time
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils


def hands_detection(frame):
    global bclick
    global xp, yp
    global xclick_menique, yclick_menique
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    color_pointer = (255,255,255)
    ANCHO_P=1920
    ALTO_P=1080
    RATIO=ANCHO_P/ALTO_P
    X=100
    Y=200
    xmano_ant=0
    ymano_ant=0
    b=3

    pyautogui.FAILSAFE=False

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:

        
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        area_width = width - X*2
        area_height = int(area_width/RATIO)
        aux = np.zeros(frame.shape, np.uint8)
        aux = cv2.rectangle(aux,(X,Y),(X + area_width, Y + area_height), (255, 0, 0),-1)
        output=cv2.addWeighted(frame,1,aux,0.7,0)


        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                
                # Get hand data
                handesness_dict = MessageToDict(results.multi_handedness[0])

                # Type of hand (left or right)
                type_hand = handesness_dict['classification'][0]['label']
                
                # level of certainty
                certainty_score = handesness_dict['classification'][0]['score']

                # If the prediction is not 
                if(certainty_score<0.9):
                    continue

                #MEDICION DE LOS PUNTOS DE LAS MANOS
                xmano = int(hand_landmarks.landmark[0].x * width)
                ymano = int(hand_landmarks.landmark[0].y * height)
                xbase = int(hand_landmarks.landmark[4].x * width)
                ybase = int(hand_landmarks.landmark[4].y * height)

                xindice = int(hand_landmarks.landmark[8].x * width)
                yindice = int(hand_landmarks.landmark[8].y * height)
                xmedio = int(hand_landmarks.landmark[12].x * width)
                ymedio = int(hand_landmarks.landmark[12].y * height)
                xanular = int(hand_landmarks.landmark[16].x * width)
                yanular = int(hand_landmarks.landmark[16].y * height)
                xmenique = int(hand_landmarks.landmark[20].x * width)
                ymenique = int(hand_landmarks.landmark[20].y * height)

                #MEDICIONES ENTRE BASE Y DEDO
                xclick_indice = xbase-xindice
                yclick_indice = ybase-yindice
                xclick_medio = xbase - xmedio
                yclick_medio = ybase - ymedio
                xclick_menique = xbase - xmenique
                yclick_menique = ybase - ymenique
                xclick_anular = xbase - xanular
                yclick_anular = ybase - yanular



                distancia_indice = int((xclick_indice**2 + yclick_indice**2)**(1/2))
                distancia_medio = int((xclick_medio ** 2 + yclick_medio ** 2) ** (1 / 2))
                distancia_anular = int((xclick_anular ** 2 + yclick_anular ** 2) ** (1 / 2))
                distancia_menique = int((xclick_menique ** 2 + yclick_menique ** 2)** (1 / 2))
                
                # Move mouse pointer with both hands
                if((xmano<= xmano_ant-b) | (xmano>=xmano_ant+b)):
                    xmano_ant = xmano
                if ((ymano <= ymano_ant - b) | (ymano >= ymano_ant + b)):
                    ymano_ant = ymano
                xp = np.interp(xmano_ant, (X,X+ area_width), (0,ANCHO_P))
                yp = np.interp(ymano_ant, (Y, Y + area_height), (0, ALTO_P))
                pyautogui.moveTo(int(xp),int(yp))

                # The right hand will have the mouse options
                if(type_hand == 'Right'):
                    # Left click
                    if(distancia_indice<=50):
                        if(bclick[0]==False):
                            print("Click")
                            pyautogui.leftClick()
                            bclick[0]=True
                    if(distancia_indice>=60):
                        if(bclick[0]==True):
                            bclick[0]=False
                    # Middle click
                    if (distancia_medio<=50):
                        if (bclick[1] == False):
                            print("Click")
                            pyautogui.middleClick()
                            bclick[1] = True
                    if (distancia_medio>=60):
                        if (bclick[1] == True):
                            bclick[1] = False
                    # Right click
                    if (distancia_anular<=50):
                        if (bclick[2] == False):
                            print("Click")
                            pyautogui.rightClick()
                            bclick[2] = True
                    if (distancia_anular>=60):
                        if (bclick[2] == True):
                            bclick[2] = False
                    # Drag 
                    if (distancia_menique<=50):
                        if (bclick[3] == False):
                            print("Arrastrar")
                            pyautogui.mouseDown()    
                            bclick[3] = True
                        else:
                            pyautogui.moveTo(xp, yp)
                    if (distancia_menique>=60):
                        if (bclick[3] == True):
                            pyautogui.mouseUp()
                            bclick[3] = False
                # The left hand will be able to set audio, brightness, etc
                else:
                    # Volume up
                    if(distancia_indice<=30):
                        if(bclick[0]==False):
                            print("Volume up")
                            pyautogui.press("volumeup")
                            bclick[0]=True
                    if(distancia_indice>=40):
                        if(bclick[0]==True):
                            bclick[0]=False
                    # Screenshot
                    #   image will be save in Images folder, under the present
                    #   hour time name
                    if (distancia_medio<=50):
                       if (bclick[1] == False):
                            print("Screenshot")
                            now = datetime.now()
                            print(now.strftime("%d-%m-%Y_%H-%M-%S"))
                            image_name = folder+"/"+now.strftime("%d-%m-%Y_%H-%M-%S")+".png"
                            pyautogui.screenshot(image_name)
                            bclick[1] = True
                    if (distancia_medio>=60):
                        if (bclick[1] == True):
                            bclick[1] = False
                    # Volume down
                    if (distancia_anular<=30):
                        if (bclick[2] == False):
                            print("Volume down")
                            pyautogui.press("volumedown")
                            bclick[2] = True
                    if (distancia_anular>=40):
                        if (bclick[2] == True):
                            bclick[2] = False
                    #Texto rápido
                    if (distancia_menique<=50):
                        if (bclick[3] == False):
                            print("Texto")
                            pyautogui.typewrite("No puedo contestar por el momento, te marco cuanto me desocupe")
                            bclick[3] = True
                    if (distancia_menique>=60):
                        if (bclick[3] == True):
                            bclick[3] = False
                


def visualizar(lblVideo):
    global cap
    global xp, yp
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame,width=640)
            hands_detection(frame)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(1,lambda : visualizar(lblVideo))
        else:
            lblVideo.image = ""
            cap.release()



def iniciar():
    global cap
    global counter
    global bclick
    global xp, yp
    bclick = np.full((4,1), False)
    xp = 0
    yp = 0
    if counter < 1:
        counter+=1
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        # Video
        video = Toplevel()
        lblVideo = Label(video)
        lblVideo.grid(column=0,row=0,columnspan=2)
        visualizar(lblVideo)

def finalizar():
    global cap
    if cap is not None:
        cap.release()
    exit(0)

def main():
    global cap
    cap = None
    global counter
    counter = 0
    global folder
    # Set folder name for screenshots
    folder = "./images"

    # Check if the folder containing the images exits. If not, create it
    if(not path.isdir(folder)):
        os.mkdir(folder)

    # Start main frame
    root = Tk()
    root.title('Handless mouse')
    root.iconphoto(False, PhotoImage(file='./icons/icon.png'))
    root.geometry('400x300+700+200')
    root.configure(bg='black')

    # Image
    m_im = Image.open("./icons/hand.jpg")
    m_im = m_im.resize((300,250), Image.ANTIALIAS)
    m_image = ImageTk.PhotoImage(m_im)
    main_image = Label(root, image=m_image)
    main_image.grid(column=0, row=0, columnspan=2)
    main_image.image = m_image


    # Create a botton to start the application
    btn = Button(root, text="Iniciar", width=25, command=iniciar, bg='white')
    btn.grid(column=0,row=1,padx=5,pady=5)

    # Create a button to finish the application
    btnFinalizar = Button(root, text="Finalizar", width=25, command=finalizar, bg='white')
    btnFinalizar.grid(column=1,row=1,padx=5,pady=5)

    # Create an event loop
    root.mainloop()

    # Destroy all
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()

