import tkinter as tk
import os
from PIL import Image, ImageTk
from WidgetControls import ListScrollCombo
from tkinter import messagebox
from WidgetControls import font_return

def exercised_double_clicked(event=None):
    messagebox.showinfo(title='None', message = 'double_clicked')


def exercise_clicked(event=None):
    messagebox.showinfo(title='None', message='single_clicked')

root = tk.Tk()

current_directory = os.getcwd()
filename = current_directory + '\\exercises.txt'

f = open('exercise_names.txt',  'r')

the_exercises = []
for one_line in f.readlines():
    one_line = one_line.replace('\n', '')
    the_exercises.append(one_line)

exercise_list_box = tk.Listbox(root)
exercise_list_box.grid(column=2, row=1, sticky='n')
exercise_list_box.config(width=350, height=450)
exercise_list_box.bind('<Double-Button>', exercised_double_clicked)
exercise_list_box.bind('<Button>', exercise_clicked)

for one_exercise in the_exercises:
    exercise_list_box.insert(tk.END, one_exercise)

root.mainloop()