import tkinter as tk
from tkinter import Canvas, Label
from PIL import ImageGrab, Image, ImageTk
import numpy as np
import cv2
import pyautogui
import time

# Инициализация главного окна Tkinter
root = tk.Tk()
root.title("Скриншот и поиск шаблона")

# Инициализация переменных
Poplovok = False
object_x_position = 0
AUTO_RESET_TIME = 5
last_detection_time = time.time()

# Создание холста для отображения результатов
canvas = Canvas(root, width=320, height=130)
canvas.pack()

# Функция для автоматического сброса object_x_position
def reset_object_x_position():
    global object_x_position, Poplovok, last_detection_time
    current_time = time.time()
    if current_time - last_detection_time > AUTO_RESET_TIME:
        object_x_position = 0
        Poplovok = False
    root.after(10, reset_object_x_position)

# Запуск автоматического сброса
reset_object_x_position()

# Функция для поиска шаблона и выделения соответствия на экране
def GLAZA():
    global object_x_position, Poplovok, last_detection_time
    # Захватывает указанную область экрана
    screenshot = ImageGrab.grab(bbox=(800, 470, 1300, 700))
    # Загружает шаблон
    template = Image.open("image.png")

    # Преобразование изображений к типу данных CV_8U
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB).astype(np.uint8)
    template = cv2.cvtColor(np.array(template), cv2.COLOR_BGR2RGB).astype(np.uint8)

    # Поиск соответствия шаблона на экране
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Отмечает соответствие прямоугольником, если max_val больше порогового значения
    if max_val > 0.4:  # Пороговое значение (настройте по своему усмотрению)
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        Poplovok = True
        object_x_position = top_left[0]  # Обновляет положение объекта по оси X
        last_detection_time = time.time()

    # Отображает изображение с выделенным соответствием на холсте
    screenshot_with_rectangle = Image.fromarray(screenshot)
    screenshot_with_rectangle = ImageTk.PhotoImage(screenshot_with_rectangle)
    canvas.create_image(0, 0, image=screenshot_with_rectangle, anchor=tk.NW)
    canvas.screenshot = screenshot_with_rectangle

    # Обновляет Label с положением объекта
    object_position_label.config(text=f"Положение объекта по X: {object_x_position}")

    # Вызывает функцию BOT
    BOT()

    # Обновляет изображение через 1/60 секунды
    root.after(1000 // 60, GLAZA)

# Функция для управления мышью
def BOT():
    if Poplovok:
        if 70 < object_x_position < 150:
            pyautogui.mouseDown(button='left')
        else:
            pyautogui.mouseUp(button='left')

# Функция для постоянного обновления изображения
def update_image():
    GLAZA()

# Создает Label для отображения положения объекта
object_position_label = Label(root, text=f"Положение объекта по X: {object_x_position}")
object_position_label.pack()

# Запускает поиск и обновление изображения
update_image()

# Запуск главного цикла Tkinter
root.mainloop()
