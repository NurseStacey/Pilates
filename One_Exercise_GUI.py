import tkinter as tk
from WidgetControls import font_return

class ExerciseClass_Sequence():

    def __init__(self):
        self.exercise = ''
        self.number_of_reps = 1
        self.time_per_rep = .3
        self.pause = 0
        self.is_an_exercise = True
        self.warning = 0
        

def is_number(this_char):
    return this_char.isnumeric()

def one_decimal_float(this_entry):

    if this_entry == '':
        return True

    try:
        x = float(this_entry)
        y = int(x*10)
        z = float(y/10)
        return x == z

    except ValueError:
        return False

class NewExerciseWindow(tk.Toplevel):
    def __init__(self, build_sequence_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.build_sequence_frame = build_sequence_frame
        self.reps = '2'
        self.time_per_rep = '4'
        self.pause = '2'
        self.warning = '0'

    def build_frame(self, this_exercise):

        def add_exercise():
            nonlocal this_exercise

            add_exercise = ExerciseClass_Sequence()
            add_exercise.number_of_reps = int(
                self.nametowidget('reps_entry').get())
            add_exercise.time_per_rep = float(
                self.nametowidget('time_per_rep_entry').get())
            add_exercise.pause = float(
                self.nametowidget('reps_pause_entry').get())
            add_exercise.exercise = this_exercise
            
            add_exercise.warning = float(
                self.nametowidget('warning_entry').get())

            self.build_sequence_frame.nametowidget('sequence_list_box').add_one_record(
                add_exercise)

            
            self.build_sequence_frame.set_time()
            self.destroy()

        def Cancel():
            self.destroy()

        self.geometry('350x200+0+0')
        this_row = 0
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        tk.Label(self, text=this_exercise[:30], font=font_return(
            16)).grid(column=1, row=this_row, columnspan=3)

        validation_float = self.register(one_decimal_float)
        validation_number = self.register(is_number)

        this_row += 1
        tk.Label(self, name='reps_label', text='Number of reps',
                 font=font_return(14)).grid(column=1, row=this_row)
        tk.Entry(self, name='reps_entry', validate="key", validatecommand=(
            validation_number, '%S'), font=font_return(14), width=5).grid(column=3, row=this_row)
        self.nametowidget('reps_entry').insert(0, self.reps)

        this_row += 1
        tk.Label(self, name='time_per_rep_label', text='Time Per Rep',
                 font=font_return(14)).grid(column=1, row=this_row)
        tk.Entry(self, name='time_per_rep_entry', validate="key", validatecommand=(
            validation_float, '%P'), font=font_return(14), width=5).grid(column=3, row=this_row)
        self.nametowidget('time_per_rep_entry').insert(0, self.time_per_rep)

        this_row += 1
        tk.Label(self, name='reps_pause_label', text='Time To Prepare',
                 font=font_return(14)).grid(column=1, row=this_row)
        tk.Entry(self, name='reps_pause_entry', validate="key", validatecommand=(
            validation_float, '%P'), font=font_return(14), width=5).grid(column=3, row=this_row)
        self.nametowidget('reps_pause_entry').insert(0, self.pause)

        this_row += 1
        tk.Label(self, name='warning_label', text='Warning',
                 font=font_return(14)).grid(column=1, row=this_row)
        tk.Entry(self, name='warning_entry', validate="key", validatecommand=(
            validation_float, '%P'), font=font_return(14), width=5).grid(column=3, row=this_row)
        self.nametowidget('warning_entry').insert(0, self.warning)

        this_row += 1
        tk.Button(self, name='done_button', command=add_exercise,
                  text='Add Exercise', font=font_return(14)).grid(column=1, row=this_row)
        tk.Label(self, text='      ').grid(column=2, row=this_row)
        tk.Button(self, name='cancel_button', command=Cancel,
                  text='Cancel', font=font_return(14)).grid(column=3, row=this_row)

        this_row += 1
        self.columnconfigure(4, weight=1)
        self.rowconfigure(this_row, weight=1)

class EditExerciseGUI(NewExerciseWindow):

    def __init__(self, build_sequence_frame, *args, **kwargs):
        super().__init__( build_sequence_frame, *args, **kwargs)
        self.build_sequence_frame = build_sequence_frame
        sequence_list_box = self.build_sequence_frame.nametowidget(
            'sequence_list_box')
        self.which_ones = sequence_list_box.get_selected_items()
        

        self.reps = sequence_list_box.get_item(
            'number_of_reps', self.which_ones[0])
        self.time_per_rep = sequence_list_box.get_item(
            'time_per_rep', self.which_ones[0])
        self.pause = sequence_list_box.get_item(
            'pause', self.which_ones[0])
        self.warning = sequence_list_box.get_item(
            'warning', self.which_ones[0])

    def build_frame(self, this_exercise):
        super().build_frame(this_exercise)

        def done():
            number_of_reps = int(self.nametowidget('reps_entry').get())
            time_per_rep = float(self.nametowidget('time_per_rep_entry').get())
            pause = float(self.nametowidget('reps_pause_entry').get())
            warning = float(self.nametowidget('warning_entry').get())
            sequence_list_box = self.build_sequence_frame.nametowidget(
                'sequence_list_box')

            for one_record in self.which_ones:
                sequence_list_box.change_values(
                    'number_of_reps', one_record,  number_of_reps)
                sequence_list_box.change_values(
                    'time_per_rep', one_record,  time_per_rep)
                sequence_list_box.change_values(
                    'pause', one_record,  pause)
                sequence_list_box.change_values(
                    'warning', one_record,  warning)

            sequence_list_box.deselect_all()
            self.build_sequence_frame.set_time()
            self.destroy()

        self.nametowidget('done_button').configure(text='Done', command=done)

