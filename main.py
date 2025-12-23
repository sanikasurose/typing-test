# Name: main.py
# Description: The entry point to a simple typing test application that measures typing speed and accuracy
# Author: Sanika Surose

import curses
from curses import wrapper
import time 
import random
import engine

# start_screen: display the start screen
def start_screen(stdscr): 
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()                                              

# display_text: displays the target and current text with color feedback for correctness
def display_text(stdscr, char_states, wpm):
    stdscr.clear()
    stdscr.addstr(1, 0, f"WPM: {wpm}")                        

    for i, (char, state) in enumerate(char_states): 
        if state == "correct": 
            color = curses.color_pair(1)
        elif state == "incorrect": 
            color = curses.color_pair(2)
        else: 
            color = curses.color_pair(3)
        stdscr.addstr(0, i, char, color)

    stdscr.refresh()

# show_results: displays final statistics after a test finishes
def show_results(stdscr, session):
    accuracy = engine.calculate_accuracy(session)
    top_mistakes = engine.get_top_mistakes(session)
    avg_delay = engine.get_average_key_delay(session)

    stdscr.clear()
    row = 0

    stdscr.addstr(row, 0, "Done!")
    row += 1

    stdscr.addstr(row, 0, f"WPM: {engine.calculate_wpm(session)}")
    row += 1

    stdscr.addstr(row, 0, f"Accuracy: {accuracy}%")
    row += 1

    stdscr.addstr(row, 0, f"Mistakes: {session['mistakes']}")
    row += 2

    stdscr.addstr(row, 0, "Top Mistakes:")
    row += 1

    if top_mistakes:
        for char, count in top_mistakes:
            stdscr.addstr(row, 2, f"'{char}' → {count}")
            row += 1
    else:
        stdscr.addstr(row, 2, "No mistakes 🎉")
        row += 1

    row += 1
    stdscr.addstr(row, 0, f"Avg key delay: {avg_delay:.2f}s")
    row += 2

    height, _ = stdscr.getmaxyx()
    if row < height:
        stdscr.addstr(row, 0, "Press any key to continue")
    else:
        stdscr.addstr(height - 1, 0, "Press any key to continue")

    stdscr.refresh()
    stdscr.getkey()

# is_escape: returns if the key pressed was escape or not
def is_escape(key):
    return (len(key) == 1 and ord(key) == 27) or key == '\x1b' or key.startswith('\x1b')

# wpm_test: runs a single typing test session
def wpm_test(stdscr):
    session = engine.create_session()
    stdscr.nodelay(True)
    quit_early = False

    while True:
        wpm = engine.calculate_wpm(session)
        char_states = engine.build_char_states(
            session["target_text"],
            session["current_text"]
        )
        display_text(stdscr, char_states, wpm)
        try:
            key = stdscr.getkey()
        except:
            time.sleep(0.01)
            continue
        # ESC ends test early
        if is_escape(key):
            quit_early = True
            break
        engine.process_key(session, key)
        # end when sentence length reached
        if session["finished"]:
            break
    stdscr.nodelay(False)
    show_results(stdscr, session)
    return quit_early

# main: entry point
def main(stdscr): 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # color pair 1: green on black
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # color pair 2: red on black
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)    # color pair 3: white on black

    start_screen(stdscr)

    while True:
        quit_early = wpm_test(stdscr)
        if quit_early:
            break
        key = stdscr.getkey()
        if is_escape(key):
            break

# wrapper: takes a function and runs it in a curses window
wrapper(main)