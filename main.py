# Name: Typing Test
# Description: A simple typing test application that measures typing speed and accuracy.
# Author: Sanika Surose

import curses
from curses import wrapper
import time 
import random
from engine import create_session, process_key, calculate_wpm, build_char_states

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


# wpm_test: handles the typing test and user input loop
def wpm_test(stdscr): 
    session = create_session()
    stdscr.nodelay(True)

    while True:
        wpm = calculate_wpm(session)
        char_states = build_char_states(session["target_text"], session["current_text"])

        display_text(stdscr, char_states, wpm)

        try: 
            key = stdscr.getkey()
        except: 
            time.sleep(0.01)
            continue
    
        if ord(key) == 27:
            break
    
        process_key(session, key)

        if session["finished"]:
            stdscr.nodelay(False)
            break
         
# main: entry point
def main(stdscr): 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # color pair 1: green on black
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # color pair 2: red on black
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)    # color pair 3: white on black

    start_screen(stdscr)

    while True: 
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "Done! Press any key to continue")
        key = stdscr.getkey()

        if ord(key) == 27: 
            break

# wrapper: takes a function and runs it in a curses window
wrapper(main)