import tkinter as tk
from WidgetControls import font_return
from build_sequence import ExerciseClass_Sequence
import pyttsx3
import winsound
import time
import keyboard
import ctypes

class ViewingFrameClass(tk.Frame):

    def __init__(self, image_object, *args, **kwargs):

        super().__init__(*args, **kwargs)

        def return_to_main():
            self.winfo_toplevel().nametowidget('main_frame').tkraise()

        font_size = 25
        self.total_time = 0
        self.image_object = image_object
        self.the_sequence = []
        self.dimensions = [900,600]
        self.the_image = self.image_object.get_from_image_folder(
            'blank', self.dimensions)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        tk.Label(self, text='The Sequence', name='title_line',
                 font=font_return(80)).grid(row=1, column=1, columnspan=5)
        tk.Button(self, text='Start', command=self.start_sequence, font=font_return(
            font_size), name='start_button').grid(row=2, column=1)
        tk.Button(self, text='Return', command=return_to_main, font=font_return(
            font_size), name='return_to_main').grid(row=2, column=2)

        
        tk.Label(self, font=font_return(font_size), text='Rep').grid(row=3, column=1)
        tk.Label(self, font=font_return(font_size), text='-',
                 name='rep_label').grid(row=4, column=1)

        tk.Label(self, font=font_return(font_size), text='Time Left').grid(row=3, column=3)
        tk.Label(self, font=font_return(font_size), name='time_left_label', 
                 text='-').grid(row=4, column=3)

        tk.Label(self, font=font_return(font_size),
                 text='Time Left').grid(row=5, column=1)
        tk.Label(self, font=font_return(font_size), text='-',
                 name='time_label').grid(row=6, column=1)

        tk.Label(self, font=font_return(font_size),
                 text=' ').grid(row=7, column=1)

        tk.Label(self, name='picture', image=self.the_image, width=1350, 
                height=720).grid(row=2, column=4, rowspan=7)

        self.rowconfigure(9, weight=1)
        self.columnconfigure(6, weight=1)

    def bring_up_viewing_frame(self, the_sequence):

        self.set_sequence(the_sequence)
        self.tkraise()

    def prepare_sequence(self, file_name):
        return_value = ExerciseClass_Sequence()
        return_value.exercise = file_name
        return_value.number_of_reps = 1
        return_value.time_per_rep = 0.3
        return_value.is_an_exercise = False
        return return_value

    def set_sequence(self, the_sequence):
        self.the_sequence=[]
        self.total_time = 0

        self.the_sequence.append(self.prepare_sequence('Ready'))
        self.the_sequence.append(self.prepare_sequence('Set'))
        self.the_sequence.append(self.prepare_sequence('Go'))

        for one_exercise in the_sequence:
            self.the_sequence.append(one_exercise)
            self.total_time += (one_exercise.number_of_reps*one_exercise.time_per_rep) 
            #don't include time for pause

    def start_sequence(self):
        
        the_picture = self.nametowidget('picture')
        rep_label = self.nametowidget('rep_label')
        time_label =  self.nametowidget('time_label')
        title_line = self.nametowidget('title_line')
        time_left_label = self.nametowidget('time_left_label')
        local_total_time = self.total_time

        rep_timer = 0
        which_rep = 0
        image_index = 0
        number_images = len(self.the_sequence)
        which_image = self.the_sequence[image_index]
        pause_keyboard = False  

        self.the_image = self.image_object.get_image(which_image, self.dimensions)
        the_picture.configure(image=self.the_image)
        self.winfo_toplevel().update()
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        engine.say(which_image.exercise)
        engine.runAndWait()


# this will prevent the screen saver or sleep.
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

        rep_label['text']='1'

        time_left=0
        #avoid_screen_saver_time = time.time()

        while True:

            interval_starting_time = time.time()

            while True:  # .1 second increments
                if time.time() - interval_starting_time >= .1:  # 1/10th second
                    break
                
                if keyboard.is_pressed('space'):
                    pause_keyboard = not(pause_keyboard)

            if pause_keyboard:
                continue
            
            rep_timer += .1
            time_left -= .1
            local_total_time -= .1
            time_left_label['text'] = self.get_time_left_str(local_total_time)

            if (int(time_left*10)%10)==0:
                time_label['text']=str(int(time_left))

            if which_image.is_an_exercise and which_image.warning>0:
                if abs((which_image.time_per_rep - rep_timer)-(which_image.warning)) < .08:
                    winsound.Beep(500, 75)
                if abs((which_image.time_per_rep - rep_timer)-(which_image.warning+.1)) < .08:
                    winsound.Beep(500, 75)

            if not(which_rep<which_image.number_of_reps):
                
                if which_image.is_an_exercise:
                    engine.say('done')
                    engine.runAndWait()

                which_rep=0
                image_index += 1
                if image_index<number_images:
                    which_image = self.the_sequence[image_index]
                    self.the_image = self.image_object.get_image(
                        which_image, self.dimensions)
                    the_picture.configure(image=self.the_image)

                    rep_label['text']='-'
                    if which_image.is_an_exercise:
                        title_line['text']=which_image.exercise

                    self.winfo_toplevel().update()

                    what_to_say=which_image.exercise
                    engine.say(what_to_say)
                    engine.runAndWait()
                    time.sleep(0.25)
                    
                    what_to_say = ''
                    if which_image.is_an_exercise:
                        what_to_say  +=  ' ' + \
                            str(which_image.number_of_reps) + ' rep'
                        if which_image.number_of_reps>1:
                            what_to_say += 's'

                    
                    engine.say(what_to_say)
                    engine.runAndWait()

                    time.sleep(which_image.pause)

                    if which_image.is_an_exercise:
                        engine.say('start')
                        engine.runAndWait()

                    time_left = which_image.number_of_reps * which_image.time_per_rep
                    time_label['text']=str(int(time_left))
                    rep_label['text']=str(which_rep+1)

            if rep_timer > which_image.time_per_rep:
                which_rep += 1
                rep_label['text'] = str(which_rep+1)
                rep_timer = 0
                winsound.Beep(500, 250)

            if not(image_index<number_images):
                break
            
            self.winfo_toplevel().update()

        ctypes.windll.kernel32.SetThreadExecutionState(
            0x80000000)  # set the setting back to normal


    def get_time_left_str(self, time_left):
        minutes = int(time_left/60)
        seconds = int(time_left - 60*minutes)

        return str(
            '%d minutes\n%d seconds' % (minutes, seconds))
