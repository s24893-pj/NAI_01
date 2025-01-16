import cv2
import mediapipe as mp
import numpy as np

# Inicjalizacja modelu ręki za pomocą biblioteki mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# deklaracja obsługi kamery oraz pola do rysowania
canvas = None
cap = cv2.VideoCapture(0)
drawing = False

# Ustawienie koloru i szerokości pędzla
color = (255, 0, 0)
brush_thickness = 5

# Poprzednia pozycja palca
prev_x, prev_y = None, None

# Pętla do obsługi kamery
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    h, w, _ = frame.shape

    # inicjalizacja pola do rysunku if None sprawdza czy pole istnieje, potrzebne do zainicjalizowania go w pierwszej klatce
    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Konwersja kolorów do RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesowanie klatki
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # koordynaty palca wskazującego
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            # koordynaty Y palca wskazującego i kciuka
            index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
            thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            # Sprawdzenie czy kciuk jest powyżej palca wskazującego, aby mieć kontrole kiedy rysujemy
            if thumb_tip_y > index_tip_y:
                drawing = True
            else:
                drawing = False

            # Rysowanie linii ciągłej na ekranie
            if drawing:
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), color, brush_thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            # Model ręki
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Połączenie pola do rysowania i kamery
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Pokazanie kamery na monitorze
    cv2.imshow("Rysowanie na kamerze", frame)

    # Obsługa przycisków
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Wyłącz program
        break
    elif key == ord('c'):  # Wyczyść rysunek
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    elif key == ord('r'):  # Kolor czerwony
        color = (0, 0, 255)
    elif key == ord('g'):  # Kolor zielony
        color = (0, 255, 0)
    elif key == ord('b'):  # Kolor niebieski
        color = (255, 0, 0)
    elif key == ord('a'):  # Eksport rysunku
        white_background = np.ones((h, w, 3), dtype=np.uint8) * 255
        mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
        white_background[mask == 255] = canvas[mask == 255]
        cv2.imwrite("drawing.png", white_background)
        print("Drawing saved as 'drawing.png'. Exiting program.")
        break

cap.release()
cv2.destroyAllWindows()
