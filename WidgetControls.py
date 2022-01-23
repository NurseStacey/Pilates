import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont


def font_return(this_size):
    return tkfont.Font(family="Times", size=this_size)

class ListScrollCombo(tk.Frame):
    def __init__(self, show_forward_backward_buttons, this_height, this_width, this_font, *args, **kwargs):

        super().__init__(*args, **kwargs)
    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)

        if show_forward_backward_buttons:
            tk.Button(self, text='Backward ' + str(this_height), height=int(this_height/4), font=this_font,
                      command=lambda: self.jump(-1)).grid(row=2, column=1, sticky='n')

            tk.Button(self, text='Forward ' + str(this_height), height=int(this_height/4), font=this_font,
                      command=lambda: self.jump(1)).grid(row=3, column=1, sticky='n')

    # create a list widget
        self.listbox = tk.Listbox(self, name='list_box', width=this_width, font=this_font, height=this_height, exportselection=0)
        self.listbox.grid(row=1, column=2, rowspan=3,sticky="nsew")

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.listbox.yview)
        scrollb.grid(row=1, column=3, rowspan=3, sticky='ns')
        self.listbox['yscrollcommand'] = scrollb.set

    def jump(self, direction):
        self.listbox.yview_scroll(direction, "pages")

    def get_listbox(self):
        return self.nametowidget('list_box')
    
    def listboxclicked(self, event):
        pass

    def add_item(self, thistext):
        self.listbox.insert(tk.END, thistext)

    def add_indexed_item(self, thistext, index):
        self.listbox.insert(index, thistext)

    def get_item(self, which):
        return self.listbox.get(which)

    def get_selected_text(self):

        try:
            return(self.get_item(self.getselections()[0]))
        except IndexError:
            return('')

    def getselections(self):
        return self.listbox.curselection()


    def set_selected_items(self, item_list):

        for index in range(self.listbox.size()):
            if self.get_item(index) in item_list:
                self.listbox.selection_set(index)

    def set_selection_mode(self, which):
        self.listbox.config(selectmode=which)

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)

    def selection_clear(self):
        self.listbox.selection_clear(0, tk.END)

    def get_all_items(self):
        all_items = []
        for index in range(self.listbox.size()):
            all_items.append(self.listbox.get(index))

        return all_items

    def set_state(self, this_state):
        self.listbox.configure(state=this_state)

    def order_items(self):

        all_items = self.get_all_items()

        all_items.sort()
        self.clear_listbox()

        for this_item in all_items:
            self.add_item(this_item)

    def bind_button_click(self, this_function):
        self.listbox.bind('<ButtonRelease>', this_function)

    def bind_double_click(self, this_function):
        self.listbox.bind('<Double-Button-1>', this_function)

    def delete_current_selection(self):
        self.listbox.delete(self.listbox.curselection())

    def has_text(self, this_text):

        all_items = self.listbox.get(0, self.listbox.size())

        for one_item in all_items:
            if one_item==this_text:
                return True

        return False


class MyMultiListBox(tk.Frame):
    def __init__(self, record_class, image_object, type_of_button, fields_to_include, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.image_object = image_object
        self.record_class = record_class
        self.variable_types = {}
        temp = self.record_class()
        self.fields_to_include = fields_to_include
        headers = []
        
        for attribute in  vars(temp):
            if not (callable(getattr(temp, attribute))) and not attribute.startswith('__') and attribute in self.fields_to_include:
                headers.append(attribute)

        self.selection_mode_multi = False
        self.which_last_sort = ''
        self.direction_last_sort = -1

        self.number_columns = len(headers)
        self.list_boxes = []
        #self.list_box_grid_info = []
        self.header_button = []


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if type_of_button=='scroll':
            forward_button = tk.Button(self, text='Jump Forward', width=10, height=6,
                                    font=tkfont.Font(family="Times", size=16), wraplength=90,
                                    command=lambda: self.scrolljump(1))
            forward_button.grid(row=2, column=2)
            

            backward_button = tk.Button(self, text='Jump Backward', width=10, height=6,
                                    font=tkfont.Font(family="Times", size=16), wraplength=90,
                                    command=lambda: self.scrolljump(-1))
            backward_button.grid(row=1, column=2)
        elif type_of_button=='shift':
            tk.Label(self, text=' ').grid(row=1, column=2)
            tk.Button(self, image=self.image_object.double_up, command=lambda: self.shift(
                'double_up')).grid(row=2, column=2, sticky='n')

            tk.Button(self, image=self.image_object.up, command=lambda: self.shift(
                'up')).grid(row=3, column=2, sticky='n')

            tk.Button(self, image=self.image_object.down, command=lambda: self.shift(
                'down')).grid(row=4, column=2, sticky='s')

            tk.Button(self, image=self.image_object.double_down, command=lambda: self.shift(
                'double_down')).grid(row=5, column=2, sticky='s')

        self.listboxframe = tk.Frame(self)

        self.listboxframe.grid_rowconfigure(0, weight=1)
        self.listboxframe.grid_columnconfigure(0, weight=1)
        self.listboxframe.grid(row=1, column=1, rowspan=5)

        self.the_scrollbar = tk.Scrollbar(self.listboxframe)
        self.the_scrollbar.config(command=self.yview)


        this_row = 1
        for x in range(self.number_columns):
            temp = tk.Button(self.listboxframe, anchor='w', text=headers[x], name=headers[x] + 'button', command=lambda y=headers[x]:self.sort(y))
            temp.grid(row=this_row, column=x+1, sticky='news')
            self.header_button.append(temp)
            temp = My_List_Box(this_row+1, x+1, self.listboxframe, name=headers[x], exportselection=False, yscrollcommand=self.listboxscroll) #need to add a command for scrolling)
            temp.config(yscrollcommand=self.listboxscroll)
            temp.bind('<<ListboxSelect>>', self.listboxclicked)
            temp.grid(row=this_row+1, column=x+1, sticky='news')

            self.list_boxes.append(temp)

        self.the_scrollbar.grid(row=this_row+1, column=self.number_columns+2, sticky='ns')

        this_row = this_row + 1
        self.listboxframe.grid_rowconfigure(this_row, weight=1)
        self.listboxframe.grid_columnconfigure(self.number_columns+3, weight=1)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(6, weight=1)


    def shift(self, which):

        selection = self.list_boxes[0].curselection()
        if len(selection)==0:
            return

        selection = selection[0]

        number_of_items = self.list_boxes[0].size()

        if (which=='up' or which=='double_up') and selection==0:
            return

        if (which=='down' or which=='double_down') and selection==(number_of_items-1):
            return

        record_to_swap = 0
        if which=='up':
            record_to_swap=  selection - 1
        if which=='down':
            record_to_swap=  selection + 1
        if which=='double_down':
            record_to_swap=  number_of_items - 1

        item_one = []
        item_two = []

        for one_list_box in self.list_boxes:
            item_one.append(one_list_box.get(selection))
            item_two.append(one_list_box.get(record_to_swap))

        for index, one_list_box in enumerate(self.list_boxes):
            one_list_box.delete(selection)
            if which=='up' or which=='down':
                one_list_box.insert(selection, item_two[index])
                one_list_box.delete(record_to_swap)
                
            one_list_box.insert(record_to_swap, item_one[index])

        self.set_selection_by_index(record_to_swap)

    def set_selection_by_index(self,  index):

        for one_list_box in self.list_boxes:
            one_list_box.select_set(index)

    def disable_buttons(self):

        for one_button in self.header_button:
            one_button['state']='disabled'
    
    def set_height(self, this_height):
        for one_list_box in self.list_boxes:
            one_list_box.config(height=this_height)

    def set_font_size(self, font_size):
        this_font = tkfont.Font(family="Times", size=font_size)
        for one_list_box in self.list_boxes:
            one_list_box.config(font=this_font)

        for one_button in self.header_button:
            one_button['font']=font_return(14)

    def get_widget(self, which):
        return(self.listboxframe.nametowidget(which))

    def clear_list_boxes(self):
        for this_list_box in self.list_boxes:
            this_list_box.delete(0, tk.END)

    #this is to get only the first one selected
    def get_number_of_selections(self):

        return len(self.list_boxes[0].curselection())

    def get_current_selection_first(self, which):
        return self.listboxframe.nametowidget(which).get(self.listboxframe.nametowidget(which).curselection()[0])

    def get_selected_items(self):
        return self.list_boxes[0].curselection()

    def get_current_selection_all(self, which):
        selection_list = self.listboxframe.nametowidget(which).curselection()

        return_value = []
        for one_selection in selection_list:
            return_value.append(self.listboxframe.nametowidget(which).get(one_selection))

        return return_value

    def change_button_text(self, buttonname, newbuttontext):
        this_button = self.listboxframe.nametowidget(buttonname + 'button')

        this_button['text'] = newbuttontext

    def change_button_font(self, buttonname, new_font):
        this_button = self.listboxframe.nametowidget(buttonname + 'button')

        this_button['font'] = new_font


    def box_clicked_override_bind(self, this_function):

        for one_list_box in self.list_boxes:
            one_list_box.bind('<<ListboxSelect>>', this_function)

    def listboxclicked(self, event=None):

        selected_item = event.widget.curselection()
        if len(selected_item)==0:
            for temp in self.list_boxes:
                temp.select_clear(0, tk.END)
            return

        #which = event.widget.curselection()[0]

        for temp in self.list_boxes:
            
            temp.select_clear(0, tk.END)
            for which in selected_item:
                temp.select_set(which)

    #if you are to allow multiple lines to be selected
    def listboxclicked_multi(self, event=None):

        all_selections = event.widget.curselection()
        for temp in self.list_boxes:
            temp.select_clear(0, tk.END)
            for which in all_selections:
                temp.select_set(which)

    def hide_column(self, which):
        self.listboxframe.nametowidget(which).grid_remove()
        self.listboxframe.nametowidget(which + 'button').grid_remove()

    def set_width(self, which, this_width):
        this_listbox = self.listboxframe.nametowidget(which)
        this_button = self.listboxframe.nametowidget(which+'button')
        this_listbox.grid(row=this_listbox.this_row, column=this_listbox.this_column)
        this_listbox.configure(width=this_width)

        this_button.grid(row=this_listbox.this_row-1, column=this_listbox.this_column)
        this_button.configure(width=this_width)

    def listboxscroll(self, *args):
        for temp in self.list_boxes:
            temp.yview_moveto(args[0])

        self.the_scrollbar.set(*args)

    def yview(self, *args):
        for temp in self.list_boxes:
            temp.yview(*args)

    def scrolljump(self, direction):

        for this_listbox in self.list_boxes:
            this_listbox.yview_scroll(direction, "pages")

    def get_item(self, which, index):
        temp = self.listboxframe.nametowidget(which)
        return temp.get(index)

    def add_one_record(self, record):

        for attribute, value in vars(record).items():
            if not (callable(getattr(record, attribute))) and not attribute.startswith('__'):
                try:
                    temp = self.listboxframe.nametowidget(attribute)
                    temp.insert(tk.END, value)
                except KeyError:
                    pass

    def change_values(self, which, index, new_value):

        temp = self.listboxframe.nametowidget(which)
        temp.delete(index)
        temp.insert(index, new_value)
        

    def deselect_all(self):

        for one_list_box in self.list_boxes:
            #one_list_box.SelectedIndex=-1
            one_list_box.selection_clear(0, 'end')

    def change_position(self, which, whereto):
        swap = ""

        for temp in self.list_boxes:
            if temp.grid_info()['column'] == whereto:
                swap = temp.winfo_name()


        if swap == "":
            return

        this_row = self.listboxframe.nametowidget(which).grid_info()['row']
        fromwhere =  self.listboxframe.nametowidget(which).grid_info()['column']

        self.listboxframe.nametowidget(which).grid(row=this_row, column=whereto)
        self.listboxframe.nametowidget(swap).grid(row=this_row, column=fromwhere)
        self.listboxframe.nametowidget(which + 'button').grid(row=this_row-1, column=whereto)
        self.listboxframe.nametowidget(swap + 'button').grid(row=this_row-1, column=fromwhere)

    def numberitems(self):
        return self.list_boxes[0].size()

    def sort(self, which):

        direction = 1
        if which == self.which_last_sort:
            direction = -1 * self.direction_last_sort
        else:
            self.which_last_sort = which

        self.direction_last_sort = direction

        number_of_items = self.numberitems()
        temporary_records = []

        element_names=vars(self.record_class())

        for index in range(number_of_items):
            temp_record = self.record_class()
            for attribute in element_names:

                if not (callable(getattr(temp_record, attribute))) and not attribute.startswith('__') and attribute in self.fields_to_include:
                    this_value = self.listboxframe.nametowidget(attribute).get(index)
                    setattr(temp_record, attribute, this_value)

            temporary_records.append(temp_record)

        self.clear_list_boxes()

        def sort_function(one_record):
            nonlocal which
            return getattr(one_record, which)

        reverse_sort = not(self.direction_last_sort==1)

        temporary_records.sort(key=sort_function, reverse=reverse_sort)

        for one_record in temporary_records:
            self.add_one_record(one_record)



    def set_selection_mode(self, which):

        if which == tk.MULTIPLE:
            self.selection_mode_multi = True
            for one_list_box in self.list_boxes:
                one_list_box.config(selectmode=which)
                #one_list_box.bind('<<ListboxSelect>>', self.set_selection_mode)
        else:
            for one_list_box in self.list_boxes:
                one_list_box.config(selectmode=which)

    def clear_all_selections(self):

        for this_list_box in self.list_boxes:
            this_list_box.selection_clear(0, tk.END)        

    def unselect_item(self, which):

        for one_list_box in self.list_boxes:
            one_list_box.delete(which)

# making a list box with tkinter base class to store location  information
class My_List_Box(tk.Listbox):
    def __init__(self, this_row, this_column, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.this_row = this_row
        self.this_column = this_column