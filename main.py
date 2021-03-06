from music21 import *
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
import inquirer
from functools import partial
import rtmidi
import time


# import music21


class PathGrabber:
    def __init__(self):
        self.path = None

    def set_path(self, path):
        self.path = path


n1 = note.Note("C4", quarterLength=1)
n2 = note.Note("A4", quarterLength=1)
s = stream.Stream()
s.append(n1)
s.append(n2)

import os

a = os.getenv('PYCHARM_HOSTED')
if a is not None:
    RUNNING_IN_PYCHARM = int(a)
else:
    RUNNING_IN_PYCHARM = False

Mode = Enum("Mode", "chord interval scale key")
ChordType = Enum("ChordType", "triad extended_triad seventh")
IntervalType = Enum("IntervalType", "diatonic chromatic")


# class AutoName(Enum):
#     def _generate_next_value_(name, start, count, last_values):
#         return name


# s.show('lily.svg')
# s.write('', fp='/Users/macbook/programming/python/music_theory/')

# c_minor.show('test.svg')


def get_major_chords(random_inversion=True):
    chords_description = [
        ['C4', 'E4', 'G4'],
        ['C4#', 'E4#', 'G4#'],
        ['D4-', 'F4', 'A4-'],
        ['D4', 'F4#', 'A4'],
        ['D4#', 'F4##', 'A4#'],
        ['E4-', 'G4', 'B4-'],
        ['E4', 'G4#', 'B4'],
        ['F4', 'A4', 'C5'],
        ['F4#', 'A4#', 'C5#'],
        ['G4-', 'B4-', 'D5-'],
        ['G4', 'B4', 'D5'],
        ['G4#', 'B4#', 'D5#'],
        ['A4-', 'C5', 'E5-'],
        ['A4', 'C5#', 'E5'],
        ['A4#', 'C5##', 'E5#'],
        ['B4-', 'D5', 'F5'],
        ['B4', 'D5#', 'F5#']
    ]
    chords = [chord.Chord(c) for c in chords_description]
    for c in chords:
        if not random_inversion:
            c.inversion(0)
        else:
            c.inversion(random.randint(0, 2))
    for (root, _, _), c in zip(chords_description, chords):
        should_be = f'{root[0] + root[2:].replace("-", "b")}-major triad'
        assert c.pitchedCommonName == should_be
    return chords


def get_minor_chords(random_inversion=True):
    chords_description = [
        ["C4", "E4-", "G4"],
        ["C4#", "E4", "G4#"],
        ["D4-", "F4-", "A4-"],
        ["D4", "F4", "A4"],
        ["D4#", "F4#", "A4#"],
        ["E4-", "G4-", "B4-"],
        ["E4", "G4", "B4"],
        ["F4", "A4-", "C5"],
        ["F4#", "A4", "C5#"],
        ["G4-", "B4--", "D5-"],
        ["G4", "B4-", "D5"],
        ["G4#", "B4", "D5#"],
        ["A4-", "C5-", "E5-"],
        ["A4", "C5", "E5"],
        ["A4#", "C5#", "E5#"],
        ["B4-", "D5-", "F5"],
        ["B4", "D5", "F5#"],
    ]
    chords = [chord.Chord(c) for c in chords_description]
    # for c in chords:
    #     for note in c:
    #         note.octave = 5
    for c in chords:
        if not random_inversion:
            c.inversion(0)
        else:
            c.inversion(random.randint(0, 2))
    for (root, _, _), c in zip(chords_description, chords):
        should_be = f'{root[0] + root[2:].replace("-", "b")}-minor triad'
        assert c.pitchedCommonName == should_be
    return chords


major_chords = get_major_chords()
minor_chords = get_minor_chords()


def wait_for_correct_answer(current_stack, correct_pitches):
    while True:
        time.sleep(0.03)
        clone_stack = current_stack.copy()
        current_stack_no_octave = set([c % 12 for c in clone_stack])
        # print(current_stack_no_octave, correct_pitches)
        if len(clone_stack) > 0:
            time.sleep(0)
            # print('ehila')
        if clone_stack == correct_pitches:
            return
        # else:
        #     print('NOT CORRECT')
    # input("Press [enter] to continue.")


def plot_chord(my_chord, title):
    my_chord.duration.type = "whole"
    path_grabber = PathGrabber()
    my_chord.show("lily.png", my_show=False, my_path_grabber=path_grabber)
    im = Image.open(path_grabber.path)
    x = np.array(im)
    black_pixels_012 = np.where(x != [255, 255, 255])
    third_is_0 = black_pixels_012[2] == 0
    black_pixels_0 = black_pixels_012[0][third_is_0]
    black_pixels_1 = black_pixels_012[1][third_is_0]
    green_x = x.copy()
    green_x[black_pixels_0, black_pixels_1, :] = [0, 255, 0]
    ax = plt.gca()
    if not RUNNING_IN_PYCHARM:
        # plt.figure()
        plt.ion()
        plt.show()
    plt.box(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    ax.imshow(x)
    plt.draw()
    plt.pause(0.001)

    def make_green():
        ax.imshow(green_x)
        plt.draw()
        plt.pause(0.001)

    return ax, make_green


def chord_training(chord_type, current_stack):
    random_chord = random.choice(minor_chords + major_chords)
    chord_name = random_chord.pitchedCommonName
    ax, make_green = plot_chord(random_chord, title=chord_name)
    correct_pitches = set()
    for c in random_chord._notes:
        correct_pitches.add(c.pitch.pitchClass + 12 * c.octave)
    wait_for_correct_answer(current_stack, correct_pitches)
    if not RUNNING_IN_PYCHARM:
        make_green()


def interval_training(interval_type: str, current_stack):
    c = random.sample('ABCDEFG', 1)[0]
    s = f"{c}4"
    print(s)
    random_note = note.Note(s, quarterLength=1)
    if interval_type == IntervalType.chromatic.name:
        i = np.random.random_integers(-11, 11, 1)[0]
    elif interval_type == IntervalType.diatonic.name:
        i = random.sample([-10, -8, -7, -5, -3, -1, 2, 4, 5, 7, 9, 11], 1)[0]
    else:
        raise ValueError()
    ii = interval.ChromaticInterval(i)
    jj = ii.getDiatonic()
    extra_name = f' ({jj.niceName})'

    other_note = random_note.transpose(ii)
    title = f'{s} {0 if i == 0 else ("+" if i > 0 else "-")}{abs(i)} semitones'f'{extra_name}'
    my_chord = chord.Chord([random_note, other_note])
    ax, make_green = plot_chord(my_chord, title=title)
    ax.set_title(title)
    correct_pitches = set()
    for c in my_chord._notes:
        correct_pitches.add(c.pitch.pitchClass + 12 * c.octave)
    wait_for_correct_answer(current_stack, correct_pitches)
    if not RUNNING_IN_PYCHARM:
        make_green()


def my_inquirer(questions):
    import termios

    try:
        answers = inquirer.prompt(questions)
        return answers["answer"]
    except termios.error as a:
        if a == (25, "Inappropriate ioctl for device"):
            pass
    return questions[0].choices[0]


def ask_mode():
    questions = [
        inquirer.List(
            "answer",
            message="what do you want to practice?",
            choices=[m.name for m in Mode],
        )
    ]
    answer = my_inquirer(questions)
    return answer


def ask_chord_type():
    questions = [
        inquirer.List(
            "answer",
            message="which chord type do you want to practice?",
            choices=[m.name for m in ChordType],
        )
    ]
    answer = my_inquirer(questions)
    return answer


def ask_interval_type():
    questions = [
        inquirer.List(
            "answer",
            message="which interval type do you want to practice?",
            choices=[m.name for m in IntervalType],
        )
    ]
    answer = my_inquirer(questions)
    return answer


# the second argument can be any python object which is passed by the calling function to make possible to access
# variables out of scope
def midi_in_callback(value, current_stack):
    # print(value)
    # key down
    if value[0][0] == 144:
        pitch = value[0][1]
        # problem with my keyboard?
        pitch -= 12
        assert pitch not in current_stack
        current_stack.add(pitch)
    # key up
    if value[0][0] == 128:
        pitch = value[0][1]
        # problem with my keyboard?
        pitch -= 12
        assert pitch in current_stack
        current_stack.remove(pitch)
    # print(current_stack)


if __name__ == "__main__":
    print("available ports:")
    print()
    print("\tInput:")
    print("\t", "ID", "Name", sep="\t")
    l = []
    for i in range(rtmidi.MidiIn().get_port_count()):
        s = rtmidi.MidiIn().get_port_name(i)
        print(i, s)
        l.append(i)
    if len(l) == 0:
        print("no midi devices detected!")
        import os

        os._exit(0)
    print("using the first midi device")
    current_stack = set()
    in_port = rtmidi.MidiIn()
    in_port.open_port(l[0])
    in_port.set_callback(midi_in_callback, current_stack)
    exit = False
    while not exit:
        if not RUNNING_IN_PYCHARM:
            mode = ask_mode()
        else:
            mode = 'interval'
        if mode == "chord":
            chord_type = ask_chord_type()
            trainer = partial(chord_training, chord_type)
        elif mode == "interval":
            interval_type = ask_interval_type()
            trainer = partial(interval_training, interval_type)
            pass
        elif mode == "scale":
            pass
        elif mode == "key":
            pass
        else:
            raise ValueError()
        try:
            while True:
                trainer(current_stack)
        except KeyboardInterrupt:
            print("back to main menu!")
            pass
        time.sleep(1)
