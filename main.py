import tkinter as tk
from tkinter import messagebox
import _tkinter
import turtle as tr
import random


"""Data-------------------------------------------------------------------------------------------------------------"""


WELCOME_TEXT = "Hello! Welcome to my Composer Assistant program.\nThis program will help you find Chords for your Melody.\nThe code is dedicated to my dear friend Sasan Sattarzade, whom I wrote it for.\nEnjoy it!\n\nHadi Yousefi\njanuary 2023\n\nContact:\nHadi19941373@gmail.com"

FONT = "Lucida Sans"

TURTLE_CHORD_FONT = (FONT, 9, "normal")
TURTLE_MELODY_NOTE_FONT = (FONT, 18, "bold")
TURTLE_SMALL_TEXT_FONT = ("Consolas", 9, "bold")

TURTLE_SCREEN_WIDTH = 1250
TURTLE_SCREEN_HEIGHT = 640
TURTLE_BORDER_PADDING = 20

TURTLE_BOX_COLORS_LIST = ["#CB2525", "#2059C3", "#19A44E", "#E5C904", "#C203BA", "#03B4C2", "#FF7800"]
#                            red,       blue,     green,     yellow,   purple,  blue-green,   orange
TURTLE_RESERVE_BOX_COLORS_LIST = ["#F8BDBD", "#B1C7EE", "#9FE7BA", "#F3EAAD", "#F6BBF4", "#A5E7EC", "#FFCC9E"]
#                                    red,       blue,     green,     yellow,   purple,  blue-green,   orange

TKINTER_TEXT_FONT = (FONT, 16, "normal")
TKINTER_LABEL_ENTRY_FONT = (FONT, 10, "normal")
TKINTER_BUTTON_FONT = (FONT, 10, "bold")
TKINTER_SMALL_BUTTON_FONT = (FONT, 8, "normal")
TKINTER_SMALLER_BUTTON_FONT = (FONT, 7, "normal")
TKINTER_POSSIBLE_SCALES_FONT = (FONT, 12, "normal")
TKINTER_X_LARGE_CHORDS_FONT = ("Consolas", 12, "normal")
TKINTER_LARGE_CHORDS_FONT = ("Consolas", 10, "normal")
TKINTER_MIDDLE_CHORDS_FONT = ("Consolas", 8, "normal")
TKINTER_SMALL_CHORDS_FONT = ("Consolas", 7, "normal")
TKINTER_CHECK_BUTTON_FONT = ("Consolas", 9, "normal")
TKINTER_BASS_CHECK_BUTTON_FONT = ("Consolas", 10, "bold")
TKINTER_WRONG_NOTE_MESSAGE = "Please, check the Note names!\nSomething is incorrect in box no."
TKINTER_NO_NOTE_MESSAGE = "You have written no Notes!"
TKINTER_NO_TONALITY_MESSAGE = "You have chosen none of the Tonalities!"
TKINTER_NO_TONIC_MESSAGE = "You have chosen no Tonic note!"

buttons_list = ["<Tab>", "<Return>", "<Delete>", "<space>", "<a>", "<b>", "<c>", "<d>", "<e>", "<f>", "<g>", "<i>", "<a>", "<#>"]

notes_list = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

alt_names_dict = {
    "c": "do",
    "c#": "do#",
    "d": "re",
    "d#": "re#",
    "e": "mi",
    "f": "fa",
    "f#": "fa#",
    "g": "sol",
    "g#": "sol#",
    "a": "la",
    "a#": "la#",
    "b": "si",
}

better_notes_names_dict = {
    "c": "C",
    "c#": "C#",
    "d": "D",
    "d#": "Eb",
    "e": "E",
    "f": "F",
    "f#": "F#",
    "g": "G",
    "g#": "G#",
    "a": "A",
    "a#": "Bb",
    "b": "B",
}

turtle_color_dict = {
    # main
    "#CB2525": "#FEC0C0",
    "#2059C3": "#B3CEFE",
    "#19A44E": "#B3FBCF",
    "#E5C904": "#FFF6B4",
    "#C203BA": "#FEB2FB",
    "#03B4C2": "#B1F9FE",
    "#FF7800": "#FFC795",
    # reserve
    "#F8BDBD": "#FCE3E3",
    "#B1C7EE": "#D9E4F8",
    "#9FE7BA": "#DBF7E6",
    "#F3EAAD": "#FDF9E0",
    "#F6BBF4": "#FDE4FC",
    "#A5E7EC": "#D9F9FC",
    "#FFCC9E": "#FFEDDD",
}


with open("Files/Scales.txt") as scales_file:
    tonality_intervals_dict = dict((key, tuple([int(j) for j in value[1:-1].split(",")])) for [key, value, consonance, main_chords] in [i.split() for i in scales_file.readlines()][1:])

with open("Files/Scales.txt") as scales_file:
    tonality_consonance_dict = dict((key, int(consonance)) for [key, value, consonance, *args] in [i.split() for i in scales_file.readlines()][1:])

with open("Files/Scales.txt") as scales_file:
    scale_main_chords_dict = dict((key, tuple([int(j) for j in main_chords[1:-1].split(",")])) for [key, value, consonance, main_chords] in [i.split() for i in scales_file.readlines()][1:])

with open("Files/Chords.txt") as chords_file:
    chords_intervals_dict = dict((key, tuple([int(j) for j in value[1:-1].split(",")])) for [key, value, consonance] in [i.split() for i in chords_file.readlines()][1:])

with open("Files/Chords.txt") as chords_file:
    chords_consonance_dict = dict((key, int(consonance)) for [key, value, consonance] in [i.split() for i in chords_file.readlines()][1:])


"""Classes----------------------------------------------------------------------------------------------------------"""


class Chord:
    def __init__(self, my_bass_note, chords_type, column=0, row=0):
        self.bass_note = note_name_corrector(my_bass_note)
        self.chord_type = chords_type.lower()
        self.name = f"{self.bass_note} {self.chord_type}"
        self.consonance = chords_consonance_dict[self.chord_type]
        self.notes_list = [notes_list[(notes_list.index(self.bass_note) + i) % 12] for i in chords_intervals_dict[self.chord_type]]
        self.number_of_notes = len(self.notes_list)
        self.chosen_for_progression = False
        self.turtle_font = TURTLE_CHORD_FONT
        self.turtle_text = f"{better_notes_names_dict[self.bass_note]} {self.chord_type}\n     {'    '.join(self.notes_list)}"
        self.column = column
        self.row = row
        self.box_drawn = False
        self.over_sized_box = False

    def is_in_chord(self, note_name):
        if note_name in self.notes_list:
            return True
        else:
            return False

    def copy(self):
        return Chord(self.bass_note, self.chord_type, self.column, self.row)


class Melody_note:
    def __init__(self, name):
        self.number = 0
        self.name = note_name_corrector(name)
        self.alt_name = alt_names_dict[self.name]
        self.chords_list = [chord.copy() for chord in total_chords_list if chord.is_in_chord(self.name)]
        self.turtle_font = TURTLE_MELODY_NOTE_FONT
        self.turtle_text = self.name


class Scale:
    def __init__(self, my_bass_note, my_tonality_type):
        self.bass_note = note_name_corrector(my_bass_note)
        self.tonality_type = my_tonality_type.lower()
        self.name = f"{self.bass_note} {self.tonality_type}"
        self.notes_list = [notes_list[(notes_list.index(self.bass_note) + i) % 12] for i in tonality_intervals_dict[self.tonality_type]]
        self.consonance = tonality_consonance_dict[self.tonality_type]
        self.number_of_notes = len(self.notes_list)
        self.chord_progression_list = []

    def copy(self):
        return Scale(self.bass_note, self.tonality_type)


class TurtleWriter(tr.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)

    def draw_border_line(self):
        self.goto(TURTLE_SCREEN_WIDTH // 2 - TURTLE_BORDER_PADDING, TURTLE_SCREEN_HEIGHT // 2 - TURTLE_BORDER_PADDING)
        self.pendown()
        self.pensize(2)
        self.goto(-(TURTLE_SCREEN_WIDTH // 2 - TURTLE_BORDER_PADDING), TURTLE_SCREEN_HEIGHT // 2 - TURTLE_BORDER_PADDING)
        self.goto(-(TURTLE_SCREEN_WIDTH // 2 - TURTLE_BORDER_PADDING), -(TURTLE_SCREEN_HEIGHT // 2 - TURTLE_BORDER_PADDING))
        self.goto(TURTLE_SCREEN_WIDTH // 2 - TURTLE_BORDER_PADDING, -(TURTLE_SCREEN_HEIGHT // 2 - TURTLE_BORDER_PADDING))
        self.goto(TURTLE_SCREEN_WIDTH // 2 - TURTLE_BORDER_PADDING, TURTLE_SCREEN_HEIGHT // 2 - TURTLE_BORDER_PADDING)
        self.penup()

    def write_object_text(self, class_object):
        [x, y] = calculate_turtle_location(class_object.column, class_object.row)
        self.goto(x, y)
        self.write(class_object.turtle_text, font=class_object.turtle_font)

    def draw_lines(self, color, chords_list):
        self.pensize(1)
        self.pencolor(color)
        for i in range(len(chords_list) - 1):
            chord_1 = chords_list[i]
            chord_2 = chords_list[i + 1]
            if chord_1.column != chord_2.column:
                [x1, y1] = calculate_turtle_location(chord_1.column, chord_1.row)
                [x2, y2] = calculate_turtle_location(chord_2.column, chord_2.row)
                if not chord_1.over_sized_box and not chord_2.over_sized_box:
                    self.goto(x1 + 105, y1 + 15)
                    self.dot(5, color)
                    self.pendown()
                    self.goto(x2 - 5, y2 + 15)
                    self.dot(5, color)
                    self.penup()
                elif chord_1.over_sized_box and not chord_2.over_sized_box:
                    self.goto(x1 + 107, y1 + 15)
                    self.dot(7, color)
                    self.pendown()
                    self.goto(x2 - 5, y2 + 15)
                    self.dot(5, color)
                    self.penup()
                elif not chord_1.over_sized_box and chord_2.over_sized_box:
                    self.goto(x1 + 105, y1 + 15)
                    self.dot(5, color)
                    self.pendown()
                    self.goto(x2 - 7, y2 + 15)
                    self.dot(7, color)
                    self.penup()
                else:
                    self.goto(x1 + 107, y1 + 15)
                    self.dot(7, color)
                    self.pendown()
                    self.goto(x2 - 7, y2 + 15)
                    self.dot(7, color)
                    self.penup()
        # reset
        self.pensize(2)
        self.pencolor("black")

    def draw_boxes(self, color, chords_list):
        for chord in chords_list:
            if not chord.box_drawn:
                [x, y] = calculate_turtle_location(chord.column, chord.row)
                box_turtle = TurtleWriter()
                box_turtle.goto(x + 50, y + 15)
                box_turtle.shape("my_rectangle")
                box_turtle.color(turtle_color_dict[color])
                box_turtle.showturtle()
                self.pensize(1)
                self.goto(x - 5, y)
                self.pencolor(color)
                self.pendown()
                self.setheading(90)
                self.forward(32)
                self.right(90)
                self.forward(110)
                self.right(90)
                self.forward(34)
                self.right(90)
                self.forward(110)
                self.right(90)
                self.forward(3)
                chord.box_drawn = True
            else:
                [x, y] = calculate_turtle_location(chord.column, chord.row)
                self.pensize(1)
                self.goto(x - 7, y)
                self.pencolor(color)
                self.pendown()
                self.setheading(90)
                self.forward(34)
                self.right(90)
                self.forward(114)
                self.right(90)
                self.forward(38)
                self.right(90)
                self.forward(114)
                self.right(90)
                self.forward(5)
                chord.over_sized_box = True
            # reset
            self.setheading(0)
            self.penup()
            self.pencolor("black")
            self.pensize(2)

    def write_header(self):
        self.goto(-TURTLE_SCREEN_WIDTH // 2 + 21, TURTLE_SCREEN_HEIGHT // 2 - 18)
        self.write("ENTER: save an image of the screen    SCAPE: exit without saving", font=TURTLE_SMALL_TEXT_FONT)

    def write_image_saved(self):
        self.goto(TURTLE_SCREEN_WIDTH // 2 - 100, TURTLE_SCREEN_HEIGHT // 2 - 18)
        self.pencolor("red")
        self.write("Image saved!", font=TURTLE_SMALL_TEXT_FONT)
        self.pencolor("black")


"""Functions--------------------------------------------------------------------------------------------------------"""


def do_everything():

    global last_melody_text
    last_melody_text = ""

    global turtle_columns_number, turtle_rows_number

    if get_melody_notes():
        if len(melody_notes_list) == 0:
            tk.messagebox.showerror("No Melody?!", TKINTER_NO_NOTE_MESSAGE)
            return

        # check the checkboxes
        all_zero1 = True
        for var1 in bassnote_checkbox_var_list:
            if var1.get() == 1:
                all_zero1 = False
        if all_zero1:
            tk.messagebox.showerror("No Tonic?!", TKINTER_NO_TONIC_MESSAGE)
            return

        all_zero = True
        for var in checkbox_var_list:
            if var.get() == 1:
                all_zero = False
        if all_zero:
            tk.messagebox.showerror("No Tonality?!", TKINTER_NO_TONALITY_MESSAGE)
            return

        else:

            """Backing up Melodies"""
            last_melody_text = '  '.join([i.name for i in melody_notes_list])
            l_last_melody.config(text=f"Latest Melody:     {last_melody_text}{(43 - len(last_melody_text)) * ' '}")
            with open("Files/My_Melodies.txt", mode="a") as old_melodies_file:
                old_melodies_file.write(f"{get_melody_record_number()}-  {last_melody_text}\n")

            """Filter and Harmonic suggestions"""
            chord_deviation = int(spinbox_1_var.get())
            scale_deviation = int(spinbox_2_var.get())
            filter_chords(chord_deviation, scale_deviation)

            """Grid Ruler"""
            turtle_columns_number = len(melody_notes_list)
            turtle_rows_number = max([len(i.chords_list) for i in melody_notes_list]) + 3

            for note in melody_notes_list:
                note.column = note.number
                note.row = 0
                for chord in note.chords_list:
                    chord.column = note.number
                    chord.row = note.chords_list.index(chord) + 1 + round((turtle_rows_number / 50) * 3)

            """Turtle Screen and Writer"""
            try:
                screen = tr.Screen()
                screen.clear()
                screen.setup(width=TURTLE_SCREEN_WIDTH, height=TURTLE_SCREEN_HEIGHT, startx=10, starty=5)
                tr.TurtleScreen._RUNNING = True
                tr.register_shape("my_rectangle", ((-17, 55), (17, 55), (17, -55), (-17, -55)))
                writer_turtle = TurtleWriter()
                writer_turtle.write_header()
                writer_turtle.draw_border_line()

                s = random.randint(0, 6)
                for chord_progression in get_chord_progressions():
                    writer_turtle.draw_boxes(TURTLE_RESERVE_BOX_COLORS_LIST[s], chord_progression[1])
                    writer_turtle.draw_boxes(TURTLE_BOX_COLORS_LIST[s], chord_progression[0])
                    writer_turtle.draw_lines(TURTLE_BOX_COLORS_LIST[s], chord_progression[0])
                    s += 1
                    s = s % 6

                for note in melody_notes_list:
                    writer_turtle.write_object_text(note)
                    for chord in note.chords_list:
                        writer_turtle.write_object_text(chord)

                screen.listen()
                screen.onkeypress(save_turtle_screen_image, "Return")
                screen.onkeypress(screen.bye, "Escape")
                screen.mainloop()
            except _tkinter.TclError or tr.Terminator:
                pass

            clear_melody_notes_list()
    return


def get_melody_notes():

    global melody_notes_list
    clear_melody_notes_list()

    if e1.get() != "":
        note_name = note_name_corrector(e1.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "1")
            return False
    if e2.get() != "":
        note_name = note_name_corrector(e2.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "2")
            return False
    if e3.get() != "":
        note_name = note_name_corrector(e3.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "3")
            return False
    if e4.get() != "":
        note_name = note_name_corrector(e4.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "4")
            return False
    if e5.get() != "":
        note_name = note_name_corrector(e5.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "5")
            return False
    if e6.get() != "":
        note_name = note_name_corrector(e6.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "6")
            return False
    if e7.get() != "":
        note_name = note_name_corrector(e7.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "7")
            return False
    if e8.get() != "":
        note_name = note_name_corrector(e8.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "8")
            return False
    if e9.get() != "":
        note_name = note_name_corrector(e9.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "9")
            return False
    if e10.get() != "":
        note_name = note_name_corrector(e10.get())
        if note_name in notes_list:
            melody_notes_list.append(Melody_note(note_name))
            melody_notes_list[-1].number = len(melody_notes_list) - 1
        else:
            tk.messagebox.showerror("Wrong Note Names!", TKINTER_WRONG_NOTE_MESSAGE + "10")
            return False
    return True


def filter_chords(chord_deviation, scale_deviation):
    global main_appropriate_scales_list
    chosen_scales_list = modify_by_bass_note(make_chosen_scales_list())
    scale_least_members_in_common = len(melody_notes_list) - scale_deviation
    main_appropriate_scales_list = [scale.copy() for scale in chosen_scales_list if is_subscale_by_n([i.name for i in melody_notes_list], scale.notes_list, scale_least_members_in_common)]

    modify_notes_chords_list()

    for note in melody_notes_list:
        note_new_chords_list = []
        for chord in note.chords_list:
            chord_least_members_in_common = chord.number_of_notes - chord_deviation
            chord_availability = False
            for scale in main_appropriate_scales_list:
                if is_subchord_by_n(chord.notes_list, scale.notes_list, chord_least_members_in_common):
                    chord_availability = True
            if chord_availability:
                note_new_chords_list.append(chord.copy())
        note.chords_list = note_new_chords_list
    return


def make_chosen_scales_list():
    global chosen_tonality_list
    chosen_tonality_list = []
    checkbox_var_value_list = [var.get() for var in checkbox_var_list]

    d = 0
    for value in checkbox_var_value_list:
        if value == 1:
            chosen_tonality_list.append(list(tonality_intervals_dict.keys())[d])
        d += 1

    modify_chosen_tonality_list()

    chosen_scales_list = [scale.copy() for scale in total_scales_list if scale.tonality_type in chosen_tonality_list]
    return chosen_scales_list


def modify_chosen_tonality_list():
    global chosen_tonality_list
    [range_start, range_stop] = scale_widget_interpreter(scale_2)
    modified_chosen_tonality_list = [tonality for tonality in chosen_tonality_list if (tonality_consonance_dict[tonality] in range(range_start, range_stop))]
    chosen_tonality_list = modified_chosen_tonality_list
    return


def modify_notes_chords_list():
    global melody_notes_list
    [range_start, range_stop] = scale_widget_interpreter(scale_1)
    for note in melody_notes_list:
        new_note_chords_list = [chord for chord in note.chords_list if chord.consonance in range(range_start, range_stop)]
        note.chords_list = new_note_chords_list
    return


def modify_by_bass_note(scale_list):
    bassnote_checkbox_var_value_list = [var1.get() for var1 in bassnote_checkbox_var_list]
    possible_bassnote_list = []
    h = 0
    for value in bassnote_checkbox_var_value_list:
        if value == 1:
            possible_bassnote_list.append(notes_list[h])
        h += 1

    f = 0
    for value in bassnote_checkbox_var_value_list:
        if value == 1:
            possible_bassnote_list.append(notes_list[f])
        f += 1

    new_scale_list = [scale.copy() for scale in scale_list if scale.bass_note in possible_bassnote_list]
    return new_scale_list


def make_possible_scales_list():
    if get_melody_notes():
        global possible_scales_list
        possible_scales_list = [scale.copy() for scale in get_all_possible_scales_list() if ((is_subscale_by_n([note.name for note in melody_notes_list], scale.notes_list, (len(melody_notes_list) - int(spinbox_2_var.get())))) and (scale.tonality_type != "chromatic"))]
        return True
    else:
        return False


def get_chord_progressions():
    chord_progressions_list = []
    for scale in main_appropriate_scales_list:
        chord_progression = []
        reserve_chord_list = []
        for note in melody_notes_list:
            first_chord_chosen = False
            for main_note in [notes_list[(notes_list.index(scale.bass_note) + i) % 12] for i in scale_main_chords_dict[scale.tonality_type]]:
                for chord in note.chords_list:
                    if chord.bass_note == main_note and set(chord.notes_list).issubset(set(scale.notes_list)) and chord.number_of_notes == 3:
                        if not first_chord_chosen:
                            chord_progression.append(chord)
                            chord.chosen_for_progression = True
                            first_chord_chosen = True
                        else:
                            reserve_chord_list.append(chord)

        chord_progressions_list.append([chord_progression, reserve_chord_list])

    return chord_progressions_list


def get_all_possible_scales_list():
    [range_start, range_stop] = scale_widget_interpreter(scale_2)
    all_possible_scales_list = [scale for scale in total_scales_list if scale.consonance in range(range_start, range_stop)]
    return all_possible_scales_list


def clear_melody_notes_list():
    global melody_notes_list
    melody_notes_list = []
    return


def get_possible_scales_text():
    if make_possible_scales_list():
        return ["\n".join([f"{better_notes_names_dict[scale.bass_note]} {scale.tonality_type}{(26 - len(scale.name)) * ' '}" for scale in possible_scales_list]), len(possible_scales_list)]
    else:
        return False


def get_melody_text():
    melody_text = " ".join([i.name for i in melody_notes_list])
    return melody_text


def get_melody_record_number():
    with open("Files/My_Melodies.txt", mode="r") as old_melodies_file:
        melody_record_number = len(old_melodies_file.readlines()) + 1
    return melody_record_number


"""Calculators, Interpreters & Correctors"""


def note_name_corrector(note_name):
    note_name = note_name.lower()
    note_name = note_name.replace(" ", "")
    note_name = note_name.replace("sharp", "#")
    note_name = note_name.replace("flat", "b")
    if note_name not in notes_list:
        if note_name in [alt_names_dict[i] for i in notes_list]:
            return [i for i in alt_names_dict if alt_names_dict[i] == note_name][0]
        elif note_name in ["eb", "mib"]:
            return "d#"
        elif note_name in ["gb", "solb"]:
            return "f#"
        elif note_name in ["ab", "lab"]:
            return "g#"
        elif note_name in ["bb", "sib"]:
            return "a#"
    else:
        return note_name


def scale_widget_interpreter(scale_widget):
    scale_number = scale_widget.get()
    if scale_number < 0:
        return [0, 10 + scale_number + 1]
    elif scale_number >= 0:
        return [scale_number, 11]


def is_subchord_by_n(list_1, list_2, n):
    if len(list_1) == 0 or len(list_2) == 0:
        return False
    else:
        if n > len(list_1):
            return False
        elif n < 2:
            if list_1[0] in list_2:
                return True
            else:
                return False
        else:
            if len(list_1) <= n:
                if set(list_1).issubset(set(list_2)):
                    return True
                else:
                    return False
            else:
                is_sublist = False
                for i in [0, -1]:
                    new_list_1 = list_1.copy()
                    new_list_1.remove(list_1[i])
                    if is_subchord_by_n(new_list_1, list_2, n):
                        is_sublist = True
                return is_sublist


def is_subscale_by_n(list_1, list_2, n):
    if len(list_1) == 0 or len(list_2) == 0:
        return False
    else:
        if n > len(list_1):
            return False
        elif n < 2:
            if list_1[0] in list_2:
                return True
            else:
                return False
        else:
            if len(list_1) <= n:
                if set(list_1).issubset(set(list_2)):
                    return True
                else:
                    return False
            else:
                is_sublist = False
                for i in range(len(list_1)):
                    new_list_1 = list_1.copy()
                    new_list_1.remove(list_1[i])
                    if is_subscale_by_n(new_list_1, list_2, n):
                        is_sublist = True
                return is_sublist


"""Turtle & Tkinter"""


def calculate_turtle_location(column, row):
    global turtle_columns_number, turtle_rows_number
    x = round(column * ((TURTLE_SCREEN_WIDTH - 100) / turtle_columns_number) - ((TURTLE_SCREEN_WIDTH - 100) / 2)) - 5
    y = - round(row * ((TURTLE_SCREEN_HEIGHT - 50) / turtle_rows_number) - ((TURTLE_SCREEN_HEIGHT - 50) / 2)) - 30
    return [x, y]


def save_turtle_screen_image():
    turtle_writer = TurtleWriter()
    ps_file_path = f"Images/{get_melody_record_number() - 1}_'{get_melody_text()}'_melody_output_image.ps"
    turtle_writer.getscreen().getcanvas().postscript(file=ps_file_path)
    turtle_writer.write_image_saved()
    return


def make_checkboxes():
    global checkbox_list
    global checkbox_var_list
    global bassnote_checkbox_list
    global bassnote_checkbox_var_list

    i = 0
    for scale_type in tonality_intervals_dict.keys():
        var = tk.IntVar()
        ch = tk.Checkbutton(win, text=scale_type + ((23 - len(scale_type)) * " "), variable=var, onvalue=1, offvalue=0, bg="white", font=TKINTER_CHECK_BUTTON_FONT, highlightthickness=0)
        ch.grid(column=2, row=i + 8, columnspan=3, pady=1)
        checkbox_list.append(ch)
        checkbox_var_list.append(var)
        i += 1
    j = 0
    for note_name in notes_list:
        better_note_name = better_notes_names_dict[note_name]
        var1 = tk.IntVar()
        var1.set(1)
        ch1 = tk.Checkbutton(win, text=(better_note_name + (4 - len(better_note_name)) * " "), variable=var1, onvalue=1, offvalue=0, bg="white", font=TKINTER_BASS_CHECK_BUTTON_FONT, highlightthickness=0)
        ch1.grid(column=5 + (j // 3), row=20 + (j % 3), columnspan=1)
        bassnote_checkbox_list.append(ch1)
        bassnote_checkbox_var_list.append(var1)
        j += 1
    return


def tkinter_l_appropriate_scales_update(event=None):
    if make_possible_scales_list():
        number_of_lines = get_possible_scales_text()[1]
        if number_of_lines > 60:
            l_appropriate_scales.config(text=f"{get_possible_scales_text()[0]}", font=TKINTER_SMALL_CHORDS_FONT)
        elif number_of_lines > 30:
            l_appropriate_scales.config(text=f"{get_possible_scales_text()[0]}", font=TKINTER_MIDDLE_CHORDS_FONT)
        elif number_of_lines > 16:
            l_appropriate_scales.config(text=f"{get_possible_scales_text()[0]}", font=TKINTER_LARGE_CHORDS_FONT)
        else:
            l_appropriate_scales.config(text=f"{get_possible_scales_text()[0]}", font=TKINTER_X_LARGE_CHORDS_FONT)
    if event is not None:
        pass
    return


def select_all_tonalities():
    for var in checkbox_var_list[1:]:
        var.set(1)
    b3.config(text="Deselect All", command=deselect_all_tonalities)
    return


def deselect_all_tonalities():
    for var in checkbox_var_list:
        var.set(0)
    b3.config(text="Select All", command=select_all_tonalities)
    return


def select_all_bassnotes():
    for var1 in bassnote_checkbox_var_list:
        var1.set(1)
    b4.config(text="Deselect All", command=deselect_all_bassnotes)
    return


def deselect_all_bassnotes():
    for var1 in bassnote_checkbox_var_list:
        var1.set(0)
    b4.config(text="Select All", command=select_all_bassnotes)
    return


def reset_tkinter():
    global checkbox_var_list
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    e7.delete(0, tk.END)
    e8.delete(0, tk.END)
    e9.delete(0, tk.END)
    e10.delete(0, tk.END)
    e1.focus()
    l_appropriate_scales.config(text="")
    scale_1.set(0)
    scale_2.set(0)
    spinbox_1_var.set("0")
    spinbox_2_var.set("0")
    for var in checkbox_var_list:
        var.set(0)
    b3.config(text="Select All")
    for var1 in bassnote_checkbox_var_list:
        var1.set(1)
    b4.config(text="Deselect All")
    return


"""Main-------------------------------------------------------------------------------------------------------------"""


print(WELCOME_TEXT)

total_chords_list = []
for bass_note in notes_list:
    for chord_type in chords_intervals_dict.keys():
        total_chords_list.append(Chord(bass_note, chord_type))

total_scales_list = []
for bass_note in notes_list:
    for tonality_type in tonality_intervals_dict.keys():
        total_scales_list.append(Scale(bass_note, tonality_type))

checkbox_list = []
checkbox_var_list = []
melody_notes_list = []
possible_scales_list = []
main_appropriate_scales_list = []
chosen_tonality_list = []
bassnote_checkbox_list = []
bassnote_checkbox_var_list = []

last_melody_text = ""

turtle_columns_number = 0
turtle_rows_number = 0


""""UI Setup--------------------------------------------------------------------------------------------------------"""


win = tk.Tk()
win.title("Sasana")
win.config(padx=15, pady=10, bg="white")
win.geometry("%dx%d+%d+%d" % (win.winfo_screenheight() * 2, win.winfo_screenmmwidth() * 2, -10, 0))
for button in buttons_list:
    win.bind(button, tkinter_l_appropriate_scales_update)

make_checkboxes()

ivy_logo = tk.PhotoImage(file="Files/ivy_logo_small.png")
c1 = tk.Canvas(win, width=110, height=110, bg="white", highlightthickness=0)
c1.create_image(55, 55, image=ivy_logo)
c1.grid(column=0, row=1, padx=10, pady=10, rowspan=5, columnspan=2)

l0 = tk.Label(win, text="Write down your melody's notes in these boxes:   ", bg="white", font=TKINTER_TEXT_FONT, highlightthickness=0)
l0.grid(column=2, row=1, columnspan=7)

l1 = tk.Label(win, text="\n1.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l1.grid(column=2, row=2, padx=10)

l2 = tk.Label(win, text="\n2.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l2.grid(column=3, row=2, padx=10)

l3 = tk.Label(win, text="\n3.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l3.grid(column=4, row=2, padx=10)

l4 = tk.Label(win, text="\n4.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l4.grid(column=5, row=2, padx=10)

l5 = tk.Label(win, text="\n5.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l5.grid(column=6, row=2, padx=10)

l6 = tk.Label(win, text="\n6.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l6.grid(column=7, row=2, padx=10)

l7 = tk.Label(win, text="\n7.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l7.grid(column=8, row=2, padx=10)

l8 = tk.Label(win, text="\n8.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l8.grid(column=9, row=2, padx=10)

l9 = tk.Label(win, text="\n9.        ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l9.grid(column=10, row=2, padx=10)

l10 = tk.Label(win, text="\n10.       ", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l10.grid(column=11, row=2, padx=10)

l_last_melody = tk.Label(text="", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l_last_melody.grid(column=2, row=4, columnspan=7)

l_tonalities = tk.Label(text="Filter by Tonality: ", bg="white", font=TKINTER_BUTTON_FONT)
l_tonalities.grid(column=2, row=6, columnspan=2, pady=10)

l_chord_deviation = tk.Label(text="Chord Deviation:   ", bg="white", font=TKINTER_BUTTON_FONT)
l_chord_deviation.grid(column=5, row=6, columnspan=2, pady=10)

l_scale_deviation = tk.Label(text="Scale Deviation:   ", bg="white", font=TKINTER_BUTTON_FONT)
l_scale_deviation.grid(column=7, row=6, columnspan=2, pady=10)

l_chord_consonance = tk.Label(text="Chord Consonance Level:     ", bg="white", font=TKINTER_BUTTON_FONT)
l_chord_consonance.grid(column=5, row=10, columnspan=3, rowspan=2, pady=10)

l_scale_consonance = tk.Label(text="Scale Consonance Level:     ", bg="white", font=TKINTER_BUTTON_FONT)
l_scale_consonance.grid(column=5, row=14, columnspan=3, rowspan=2, pady=10)

l_filter_by_tonic = tk.Label(text="Filter by Tonic note:             ", bg="white", font=TKINTER_BUTTON_FONT)
l_filter_by_tonic.grid(column=5, row=18, columnspan=3, rowspan=2, pady=10)

l_appropriate_scales_title = tk.Label(text=" Possible Scales:", bg="white", font=TKINTER_POSSIBLE_SCALES_FONT)
l_appropriate_scales_title.grid(column=13, row=1)

l_appropriate_scales = tk.Label(text="", bg="white", font=TKINTER_LABEL_ENTRY_FONT)
l_appropriate_scales.place(x=950, y=40)

e1 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e1.grid(column=2, row=3, padx=10)
e1.focus()

e2 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e2.grid(column=3, row=3, padx=10)

e3 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e3.grid(column=4, row=3, padx=10)

e4 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e4.grid(column=5, row=3, padx=10)

e5 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e5.grid(column=6, row=3, padx=10)

e6 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e6.grid(column=7, row=3, padx=10)

e7 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e7.grid(column=8, row=3, padx=10)

e8 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e8.grid(column=9, row=3, padx=10)

e9 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e9.grid(column=10, row=3, padx=10)

e10 = tk.Entry(width=6, bg="#EBEBEB", font=TKINTER_LABEL_ENTRY_FONT)
e10.grid(column=11, row=3, padx=10)

spinbox_1_var = tk.StringVar()
spinbox_1_var.set("0")
spinbox_1 = tk.Spinbox(from_=0, to=2, width=5, bg="white", textvariable=spinbox_1_var, highlightthickness=0)
spinbox_1.grid(column=5, row=8, pady=10, rowspan=2, columnspan=1)

spinbox_2_var = tk.StringVar()
spinbox_2_var.set("0")
spinbox_2 = tk.Spinbox(from_=0, to=2, width=5, bg="white", highlightthickness=0, textvariable=spinbox_2_var, command=tkinter_l_appropriate_scales_update)
spinbox_2.grid(column=7, row=8, pady=10, rowspan=2, columnspan=1)

scale_1 = tk.Scale(from_=-5, to=5, sliderlength=25, width=25, length=247,  bg="white", orient="horizontal", highlightthickness=0)
scale_1.grid(column=5, row=11, pady=10, rowspan=3, columnspan=4)

scale_2 = tk.Scale(from_=-5, to=5, sliderlength=25, width=25, length=247,  bg="white", orient="horizontal", command=tkinter_l_appropriate_scales_update, highlightthickness=0)
scale_2.grid(column=5, row=15, pady=10, rowspan=3, columnspan=4)

b1 = tk.Button(text="Generate\nChords", width=9, height=3, font=TKINTER_BUTTON_FONT, bg="black", fg="white", activebackground="#333333", activeforeground="white", command=do_everything, highlightthickness=3)
b1.grid(column=12, row=2, padx=10, pady=20, rowspan=4)

b2 = tk.Button(text="Reset", width=10, font=TKINTER_SMALL_BUTTON_FONT, bg="black", fg="white", activebackground="#333333", activeforeground="white", command=reset_tkinter, highlightthickness=0)
b2.grid(column=12, row=6)

b3 = tk.Button(text="Select All", width=8, font=TKINTER_SMALLER_BUTTON_FONT, bg="black", fg="white", activebackground="#333333", activeforeground="white", command=select_all_tonalities, highlightthickness=0)
b3.grid(column=0, row=8, columnspan=3)

b4 = tk.Button(text="Deselect All", width=8, font=TKINTER_SMALLER_BUTTON_FONT, bg="black", fg="white", activebackground="#333333", activeforeground="white", command=deselect_all_bassnotes, highlightthickness=0)
b4.grid(column=5, row=23, columnspan=1, rowspan=2)

win.mainloop()
