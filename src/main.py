import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from google.protobuf.json_format import MessageToDict
from datetime import datetime
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

color_pointer = (255,255,255)
ANCHO_P=1920
ALTO_P=1080
RATIO=ANCHO_P/ALTO_P
X=100
Y=200
xmano_ant=0
ymano_ant=0
b=3

bclick = False

pyautogui.FAILSAFE=False

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
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
                xclick = xbase-xindice
                yclick = ybase-yindice
                xclick_medio = xbase - xmedio
                yclick_medio = ybase - ymedio
                xclick_derecho = xbase - xanular
                yclick_derecho = ybase - yanular
                xclick_menique = xbase - xmenique
                yclick_menique = ybase - ymenique


                distancia_izquierdo= int((xclick**2 + yclick**2)**(1/2))
                distancia_medio = int((xclick_medio ** 2 + yclick_medio ** 2) ** (1 / 2))
                distancia_derecho = int((xclick_derecho ** 2 + yclick_derecho ** 2) ** (1 / 2))
                distancia_menique = int((xclick_menique ** 2 + yclick_menique ** 2)** (1 / 2))
                
                # The right hand will have the mouse options
                if(type_hand == 'right'):
                    #CLICK IZQUIERDO
                    if(distancia_izquierdo<=50):
                        if(bclick==False):
                            print("Click")
                            pyautogui.leftClick()
                            bclick=True
                        #bclick=True
                    if(distancia_izquierdo>=60):
                        if(bclick==True):
                            bclick=False
                    if (distancia_derecho <= 50):
                        if (bclick == False):
                            print("Click")
                            pyautogui.rightClick()
                            bclick = True
                        # bclick=True
                    if (distancia_derecho >= 60):
                        if (bclick == True):
                            bclick = False
                    if (distancia_medio <= 50):
                        if (bclick == False):
                            print("Click")
                            pyautogui.middleClick()
                            bclick = True
                        # bclick=True
                    if (distancia_medio >= 60):
                        if (bclick == True):
                            bclick = False

                    if (distancia_menique <= 50):
                        if (bclick == False):
                            print("Click")
                            pyautogui.dragTo(500, 400, duration=0.3)
                            bclick = True
                        # bclick=True
                    if (distancia_menique >= 60):
                        if (bclick == True):
                            bclick = False

                    print(f'Dist= {distancia_derecho}, blick={bclick}')
                    if((xmano<= xmano_ant-b) | (xmano>=xmano_ant+b)):
                        xmano_ant = xmano
                    if ((ymano <= ymano_ant - b) | (ymano >= ymano_ant + b)):
                        ymano_ant = ymano
                    xp = np.interp(xmano_ant, (X,X+ area_width), (0,ANCHO_P))
                    yp = np.interp(ymano_ant, (Y, Y + area_height), (0, ALTO_P))
                    pyautogui.moveTo(int(xp),int(yp))
                    cv2.circle(output,(xmano_ant, ymano_ant),10,color_pointer,-1)


#OTRA FUNCION CON DEDO MEÑIQUE
                # The left hand will be able to set audio, brightness, etc
                else:
                    # Volume up
                    if(distancia_izquierdo<=50):
                        if(bclick==False):
                            print("Volume up")
                            pyautogui.press("volumeup")
                            bclick=True
                    if(distancia_izquierdo>=60):
                        if(bclick==True):
                            bclick=False
                    # Volume down
                    if (distancia_derecho <= 50):
                        if (bclick == False):
                            print("Volume down")
                            pyautogui.press("volumedown")
                            bclick = True
                    if (distancia_derecho >= 60):
                        if (bclick == True):
                            bclick = False
                    # Screenshot
                    #   image will be save in Images folder, under the present
                    #   hour time name
                    if (distancia_medio <= 20):
                            print("Screenshot")
                            now = datetime.now()
                            print(now.strftime("%d-%m-%Y_%H-%M-%S"))
                            pyautogui.screenshot("./images/"+now.strftime("%d-%m-%Y_%H-%M-%S")+".png")
                            time.sleep(0.5)



        cv2.imshow('Frame2', output)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()