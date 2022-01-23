import tkinter as tk
from WidgetControls import ListScrollCombo
from WidgetControls import font_return
from WidgetControls import MyMultiListBox
from tkinter import messagebox
import pickle
import os
import math
from One_Exercise_GUI import NewExerciseWindow, EditExerciseGUI, ExerciseClass_Sequence



class SequenceEditorClass(tk.Frame):

    def __init__(self, image_object, *args, **kwargs):

        def sequence_box_clicked(event=None):
            sequence_list_box.listboxclicked(event)
            if sequence_list_box.get_number_of_selections() == 0:
                self.button_frame.nametowidget('button_remove')['state'] = tk.DISABLED
                self.button_frame.nametowidget('button_edit')['state'] = tk.DISABLED
            else:
                self.button_frame.nametowidget('button_remove')['state'] = tk.NORMAL
                self.button_frame.nametowidget('button_edit')['state'] = tk.NORMAL

        #def exercised_double_clicked(event=None):
        def add_exercise():                
            
            this_exercise=exercise_list_box.get_selected_text()
            add_exercise = NewExerciseWindow(self)
            add_exercise.build_frame(this_exercise)
            add_exercise.grab_set()

        def save():

            sequence_name = self.nametowidget('sequence_name').get()
            if not(self.valid_file_name(sequence_name)):
                return
            
            temp = self.get_sequence()

            this_file = open('sequences\\' + sequence_name + '.seq', 'wb')
            pickle.dump(temp, this_file)

            this_file.close()
            
            main_list_box = self.winfo_toplevel().nametowidget(
                'main_frame').nametowidget('sequences')

            if not(main_list_box.has_text(sequence_name)):
                main_list_box.add_item(sequence_name)
            
            cancel()

        def remove():
            which_items = self.nametowidget(
                            'sequence_list_box').get_selected_items()
            for one_item in reversed(which_items):
                self.nametowidget('sequence_list_box').unselect_item(one_item)

            self.set_time()

        def copy():
            which_items = self.nametowidget(
                'sequence_list_box').get_selected_items()
            for index in which_items:
                temp = self.get_one_exercise(index)
                sequence_list_box.add_one_record(temp)

            self.nametowidget(
                'sequence_list_box').deselect_all()

            self.set_time()

        def edit():
            if len(sequence_list_box.get_selected_items()) == 0:
                messagebox.showerror('Selection Error', 'Select at least one exercise from the sequence')
                return

            edit_exercise = EditExerciseGUI(self)
            edit_exercise.build_frame('')
            edit_exercise.grab_set()

        def cancel():
            self.winfo_toplevel().nametowidget('main_frame').tkraise()

        super().__init__(*args, **kwargs)

        self.dimensions = [300, 200]
        this_row = 0
        self.image_object = image_object
        #took me an  hour to figure out that I needed to start the current image in 
        #permament variable
        self.the_image = self.image_object.get_from_image_folder('blank', self.dimensions)

        tk.Label(self, text='Sequencing Editor', name='title_lable',
                font=font_return(24)).grid(column=2, columnspan=5,  row=this_row)

        this_row += 1
        tk.Label(self, text='Name of Sequence',
                font=font_return(20)).grid(column=2, row=this_row)
        tk.Entry(self, name='sequence_name', font=font_return(
            20), width=20).grid(column=3, row=this_row)

        tk.Label(self, text='Total Time', font=font_return(
            20)).grid(column=5, row=this_row)
        tk.Label(self, name='total_time', text='0', font=font_return(
            20), width=20).grid(column=6, row=this_row)

        this_row += 1
        tk.Label(self, text='Exercise Options',
                font=font_return(16)).grid(column=2, row=this_row)
        tk.Label(self, text='This Sequence',  font=font_return(
            16)).grid(column=4,  row=this_row)

        this_row += 1
        
        sequence_list_box = self.build_sequence_box(
            this_row, sequence_box_clicked)

        this_row = this_row+1

        tk.Label(
            self, image=self.the_image, name='picture_label').grid(row=this_row, column=1)

        exercise_list_box = ListScrollCombo(
            False, 20, 25, font_return(14), self, name='exercises')
        exercise_list_box.grid(column=2, row=this_row, sticky='n')
        exercise_list_box.config(width=350, height=450)
        #Not sure how to get both double click and single click to work
        #changed this to a button - see below
        #exercise_list_box.bind_double_click(exercised_double_clicked)
        exercise_list_box.bind_button_click(self.exercise_clicked)



        for one_exercise in image_object.the_exercises:
            exercise_list_box.add_item(one_exercise.exercise_name)

        this_row += 1

        self.button_frame = tk.Frame(self, name='button_frame')
        self.button_frame.grid(row=this_row, column=3, rowspan=2,
                          columnspan=3, sticky='news')
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        tk.Button(self.button_frame, name='button_save', width=13, command=save, text='Save',
                  font=font_return(16)).grid(row=1, column=1)
        tk.Button(self.button_frame, name='button_remove', anchor=tk.CENTER, width=13, command=remove, text='Remove',
                  font=font_return(16)).grid(row=1, column=2)
        tk.Button(self.button_frame, name='copy_remove', width=13, command=copy, text='Copy and Append',
                  font=font_return(16)).grid(row=1, column=3)
        self.button_frame.nametowidget('button_remove')['state'] = tk.DISABLED

        tk.Button(self.button_frame, name='button_edit', width=13, command=edit, text='Edit',
                  font=font_return(16)).grid(row=2, column=1)
        tk.Button(self.button_frame, name='button_cancel', width=13, command=cancel, text='Cancel',
                  font=font_return(16)).grid(row=2, column=2)
        tk.Button(self.button_frame, name='add_exercise', width=13, command=add_exercise, text='Add Exercise',
                  font=font_return(16)).grid(row=2, column=3)
        self.button_frame.nametowidget('button_edit')['state'] = tk.DISABLED
        self.button_frame.grid_rowconfigure(3, weight=1)
        self.button_frame.grid_columnconfigure(4, weight=1)


        # tk.Button(self, name='button_save', width=13, command=save, text='Save',
        #         font=font_return(16)).grid(column=3, row=this_row, sticky='W')
        # tk.Button(self, name='button_remove', anchor=tk.CENTER, width=13, command=remove, text='Remove',
        #         font=font_return(16)).grid(column=4, row=this_row, sticky='E')
        # tk.Button(self, name='copy_remove', width=13, command=copy, text='Copy and Append',
        #         font=font_return(16)).grid(column=5, row=this_row, sticky='E')
        # self.nametowidget('button_remove')['state'] = tk.DISABLED

        # this_row += 1
        # tk.Button(self, name='button_edit', width=13, command=edit, text='Edit',
        #           font=font_return(16)).grid(column=3, row=this_row, sticky='W')
        # tk.Button(self, name='button_cancel', width=13, command=cancel, text='Cancel',
        #           font=font_return(16)).grid(column=4, row=this_row, sticky='W')
        # tk.Button(self, name='add_exercise', width=13                           , command=add_exercise, text='Add Exercise',
        #           font=font_return(16)).grid(column=5, row=this_row, sticky='E')
        # self.nametowidget('button_edit')['state'] = tk.DISABLED
        this_row += 1
        self.grid_rowconfigure(this_row, weight=1)
        self.grid_columnconfigure(8, weight=1)

    def build_sequence_box(self, which_row, sequence_box_clicked):

        headers = ['exercise', 'number_of_reps',
                   'time_per_rep', 'pause', 'warning']
        sequence_list_box = MyMultiListBox(
            ExerciseClass_Sequence, self.image_object, 'shift', headers, self, name='sequence_list_box')
        sequence_list_box.set_font_size(14)
        sequence_list_box.set_height(20)
        sequence_list_box.set_selection_mode(tk.SINGLE)
        sequence_list_box.grid(column=3, row=which_row,
                               rowspan=2, columnspan=3)
        for one_column in headers[1:]:
            sequence_list_box.set_width(one_column, 7)

        sequence_list_box.change_button_text('number_of_reps', 'Reps')
        sequence_list_box.change_button_text('time_per_rep', 'Time\nper\nRep')
        sequence_list_box.change_button_text('pause', 'Time to\nPrepare')
        sequence_list_box.change_button_text('warning', 'Warning\nBeep')
        sequence_list_box.change_button_text('exercise', 'Exercise')

        sequence_list_box.change_button_font('number_of_reps', font_return(12))
        sequence_list_box.change_button_font('time_per_rep', font_return(12))
        sequence_list_box.change_button_font('pause', font_return(12))
        sequence_list_box.change_button_font('warning', font_return(12))
        sequence_list_box.change_button_font('exercise', font_return(12))

        sequence_list_box.box_clicked_override_bind(sequence_box_clicked)
        sequence_list_box.set_selection_mode(tk.MULTIPLE)

        return sequence_list_box

    def unselect_exercise(self):
        self.nametowidget('exercises').selection_clear()
        self.the_image = self.image_object.get_from_image_folder(
            'blank', self.dimensions)
        self.nametowidget('picture_label').configure(image=self.the_image)
            
    def exercise_clicked(self, event=None):
        exercise = self.nametowidget('exercises').get_selected_text()
        self.the_image = self.image_object.get_exercise_image(
            exercise, self.dimensions)
        self.nametowidget('picture_label').configure(image=self.the_image)

    def valid_file_name(self, file_name):

        if file_name == '':
            messagebox.showerror(
                    'File Error', 'Must enter a name for the sequence')
            return False

        if os.path.exists(os.getcwd() + '\\sequences\\' + file_name + '.seq'):
            MsgBox = messagebox.askquestion(
                'Overwrite', 'Sequences already exists.  Overwrite?')
            if MsgBox == 'no':
                return False
        
        return True

    def Calculate_Time_For_Sequence(self):
        sequence_list_box = self.nametowidget('sequence_list_box')

        number_of_exercises = sequence_list_box.numberitems()
        total_time = 0.0
        for index in range(number_of_exercises):
            total_time += float(sequence_list_box.get_item('number_of_reps', index)) *\
                float(sequence_list_box.get_item('time_per_rep', index)) +\
                float(sequence_list_box.get_item('pause', index))

        return total_time

    def set_time(self):
        total_time = self.Calculate_Time_For_Sequence()
        minutes = int(total_time/60)
        seconds = int(total_time - 60*minutes)
        
        self.nametowidget('total_time')['text'] = str(
            '%d minutes, %d seconds' % (minutes, seconds))

    def clear_sequence(self):

        self.nametowidget('sequence_name').delete(0, tk.END)
        self.nametowidget('sequence_list_box').clear_list_boxes()

    def time_for_this_exercise(self, which_exercise):
        return which_exercise.number_of_reps * which_exercise.time_per_rep + which_exercise.pause

    def load_sequence(self, which_sequence, this_sequence):
        self.clear_sequence()
        self.nametowidget('sequence_name').insert(0, which_sequence)

        self.total_time = 0

        for one_exercise in this_sequence:
            self.nametowidget('sequence_list_box').add_one_record(one_exercise)
            #self.total_time += self.time_for_this_exercise(one_exercise)

        #self.nametowidget('total_time')['text'] = self.time_text()
        self.set_time()

    def time_text(self):

        minutes = math.floor(self.total_time/60)
        seconds = self.total_time - 60*minutes

        return ('%d minutes, %d seconds' % (minutes, seconds))

    def get_sequence(self):
        the_sequence = []

        for index in range(self.nametowidget('sequence_list_box').numberitems()):
            the_sequence.append(self.get_one_exercise(index))

        return the_sequence

    def get_one_exercise(self, index):
        sequence_list_box = self.nametowidget('sequence_list_box')
        temp = ExerciseClass_Sequence()

        temp.exercise = sequence_list_box.get_item('exercise', index)
        temp.number_of_reps = int(
            sequence_list_box.get_item('number_of_reps', index))
        temp.time_per_rep = float(
            sequence_list_box.get_item('time_per_rep', index))
        temp.pause = float(sequence_list_box.get_item('pause', index))
        temp.warning = float(sequence_list_box.get_item('warning', index))

        return temp

    
