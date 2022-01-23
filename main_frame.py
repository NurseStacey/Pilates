from WidgetControls import font_return
from WidgetControls import ListScrollCombo
import tkinter as tk
from tkinter import messagebox
import os
import pickle

class main_dlg_class(tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.the_sequences = []
        self.load_sequences()

        def run_sequence():
            which_sequence = sequence_list_box.get_selected_text()
            if which_sequence == '':
                messagebox.showerror('Error', 'Must choose a sequence')
            else:
                self.winfo_toplevel().nametowidget('viewing_frame').bring_up_viewing_frame(self.load_sequence(which_sequence))

        def preview_sequence():
            which_sequence = sequence_list_box.get_selected_text()
            if which_sequence == '':
                messagebox.showerror('Error', 'Must choose a sequence')
                return

            self.winfo_toplevel().nametowidget('preview_frame').set_sequence(
                which_sequence, self.load_sequence(which_sequence))
                
            self.winfo_toplevel().nametowidget('preview_frame').tkraise()

        def build_sequence():
            
            self.winfo_toplevel().nametowidget('sequence_building_frame').clear_sequence()
            self.winfo_toplevel().nametowidget('sequence_building_frame').tkraise()

        def edit_sequence():
            which_sequence = sequence_list_box.get_selected_text()
            if which_sequence == '':
                messagebox.showerror('Error', 'Must choose a sequence')
            else:
                self.winfo_toplevel().nametowidget('sequence_building_frame').load_sequence(
                    which_sequence, self.load_sequence(which_sequence))

                self.winfo_toplevel().nametowidget('sequence_building_frame').tkraise()

            #self.winfo_toplevel().nametowidget('sequence_building_frame').tkraise()

        def delete_sequence():
            which_sequence = sequence_list_box.get_selected_text()
            if which_sequence == '':
                messagebox.showerror('Error', 'Must choose a sequence')
                return

            MsgBox = messagebox.askquestion(
                'Confirm', 'Are you sure that you want to delete the selected sequence?')
            if MsgBox == 'no':
                return

            current_directory = os.getcwd()
            sequence_directory = current_directory + '\\sequences\\'
            os.remove(sequence_directory + which_sequence + '.seq')
            sequence_list_box.delete_current_selection()

        def exit_program():
            quit()

        this_row=0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        this_row += 1
        tk.Label(self, text='The Prompter', font=font_return(
            26)).grid(row=this_row, column=2)

        this_row += 1
        tk.Button(self, text='Start Sequence', command=run_sequence, name='start_button',
                  font=font_return(14)).grid(column=1, row=this_row, pady=10)

        this_row += 1
        tk.Button(self, text='Preview Sequence', command=preview_sequence,
                  name='preview_button', font=font_return(14)).grid(column=1, row=this_row, pady=10)

        sequence_list_box = ListScrollCombo(
            False, 20, 25, font_return(14), self, name='sequences')
        sequence_list_box.set_selection_mode(tk.SINGLE)
        sequence_list_box.grid(row=this_row, column=3, rowspan = 4)
        sequence_list_box.config(width=350, height=450)

        for one_sequence in self.the_sequences:
            sequence_list_box.add_item(one_sequence)

        this_row += 1
        tk.Button(self, text='Build Sequence', command=build_sequence, name='build_button', font=font_return(14)).grid(column=1,row=this_row, pady=10)
        this_row += 1
        tk.Button(self, text='Edit Sequence', command=edit_sequence, name='edit_button', font=font_return(14)).grid(column=1,row=this_row, pady=10)
        this_row += 1
        tk.Button(self, text='Delete Sequence', command=delete_sequence, name='delete_button', font=font_return(14)).grid(column=1,row=this_row, pady=10)
        this_row += 1
        tk.Button(self, text='Exit', command=exit_program, name='exit_program',
                  font=font_return(14)).grid(column=1, row=this_row, pady=10)

        this_row += 1
        self.rowconfigure(this_row, weight=1)
        self.columnconfigure(4, weight=1)

    def load_sequence(self, which_sequence):
        file_name = os.getcwd() + '\\sequences\\' + which_sequence + '.seq'
        return pickle.load(open(file_name, 'rb'))


    def load_sequences(self):
        
        current_directory = os.getcwd()
        sequence_directory = current_directory + '\\sequences\\'

        for one_item in os.listdir(sequence_directory):
            if os.path.isfile(sequence_directory+one_item):
                this_file = one_item.partition('.')
                if this_file[2].lower() == 'seq':
                    self.the_sequences.append(this_file[0])
