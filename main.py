import tkinter as tk
import os
from main_frame import main_dlg_class
from build_sequence import SequenceEditorClass
from preview_frame import PreviewFrameClass
from image_file import Image_Class
from viewing_frame import ViewingFrameClass

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(2, weight=15)
root.rowconfigure(2, weight=1)

image_object = Image_Class(os.getcwd())

main_dlg_class(root, name='main_frame').grid(row=1, column=1, sticky='news')
SequenceEditorClass(image_object, root, name='sequence_building_frame').grid(row=1, column=1, sticky='news')
PreviewFrameClass(image_object, root, name='preview_frame').grid(
    row=1, column=1, sticky='news')
ViewingFrameClass(image_object, root, name='viewing_frame').grid(
    row=1, column=1, sticky='news')

root.nametowidget('main_frame').tkraise()    
root.attributes('-fullscreen', True)
#root.geometry('1500x800')
root.mainloop()
