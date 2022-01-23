import tkinter as tk
import os
from WidgetControls import font_return

class PreviewFrameClass(tk.Frame):
    
    def __init__(self, image_object, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.dimensions = [600, 400]
        self.the_sequence = []
        self.image_object = image_object

        def return_main_screen():
            self.winfo_toplevel().nametowidget('main_frame').tkraise()

        def forward():
            nonlocal index

            index += 1
            if index==len(self.the_sequence):
                self.set_end()
            elif index > len(self.the_sequence):
                index -=1
            else:
                self.set_picture(index)

        def backward():
            nonlocal index

            index -= 1
            if index == -1:
                self.set_start()
            elif index<-1:
                index += 1
            else:
                self.set_picture(index)

        index = 0
        
        self.columnconfigure(0, weight=1)

        tk.Label(self, text='The Sequence', name='title_line',
                 font=font_return(80)).grid(row=1, column=1, columnspan=4)
        tk.Label(self, text=' ', name='the_exercise',
                 font=font_return(30)).grid(row=2, column=3)
        tk.Button(self, text='Step Forward', font=font_return(
            30), command=forward).grid(row=3, column=1)
        tk.Button(self, text='Step Backward', font=font_return(
            30), command=backward).grid(row=4, column=1)
        tk.Button(self, text='Main Screen', font=font_return(
            30), command=return_main_screen).grid(row=5, column=1)

        self.the_image = self.image_object.get_from_image_folder(
            'blank', self.dimensions)
        tk.Label(self, name='picture_label', image=self.the_image, width=600, height=400).grid(
            row=3, column=3, rowspan=2, sticky='n')

        tk.Label(self, text='Reps', font=font_return(30)).grid(row=5, column=2)
        tk.Label(self, text='-', name='reps_label',
                 font=font_return(30)).grid(row=6, column=2)

        self.rowconfigure(7, weight=1)
        self.columnconfigure(5, weight=1)

    def set_sequence(self, which_sequence, the_sequence):

        self.nametowidget('title_line')['text']=which_sequence
        self.the_sequence = the_sequence

        self.set_picture(0)

    def set_start(self):
        self.the_image = self.image_object.get_from_image_folder(
            'start', self.dimensions)
        self.nametowidget('picture_label').configure(image=self.the_image)

        self.nametowidget('reps_label')[
            'text'] = ''

    def set_end(self):
        self.the_image = self.image_object.get_from_image_folder(
            'end', self.dimensions)
        self.nametowidget('picture_label').configure(image=self.the_image)

        self.nametowidget('reps_label')[
            'text'] = ''

    def set_picture(self, which):

        self.the_image = self.image_object.get_exercise_image(
            self.the_sequence[which].exercise, self.dimensions)
        self.nametowidget('picture_label').configure(image=self.the_image)

        self.nametowidget('reps_label')[
            'text'] = self.the_sequence[which].number_of_reps
            
        self.nametowidget('the_exercise')[
            'text'] = self.the_sequence[which].exercise

        self.winfo_toplevel().update()
