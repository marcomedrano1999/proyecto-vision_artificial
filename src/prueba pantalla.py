import cv2
import mediapipe as mp
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

ANCHO_P=1920
ALTO_P=1080

RATIO=ANCHO_P/ALTO_P
print(RATIO)

screenshot = pyautogui.screenshot(region=(0,0,ANCHO_P,ALTO_P))
screenshot = np.array(screenshot)
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
cv2.imshow("Pantalla", screenshot)
cv2.waitKey()
cv2.destroyAllWindows()