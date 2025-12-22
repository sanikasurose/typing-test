# Name: Typing Test
# Description: A simple typing test application that measures typing speed and accuracy.
# Author: Sanika Surose

import curses
from curses import wrapper
import time 
import random

# start_screen: display the start screen
def start_screen(stdscr): 
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()                                              


# display_text: displays the target and current text with color feedback for correctness
def display_text(stdscr, target, current, wpm):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")                        

    for i, char in enumerate(current): 
        correct_char = target[i]
        color = curses.color_pair(1)

        if char != correct_char: 
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)
     
# load_text: loads a random text from text.txt file
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

# wpm_test: handles the typing test and user input loop
def wpm_test(stdscr): 
    target_text = load_text()
    current_text = []  
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True: 
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()                                       
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        try: 
            key = stdscr.getkey()
        except: 
            time.sleep(0.01)
            continue

        if ord(key) == 27: 
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'): 
            if len(current_text) > 0: 
                current_text.pop()
        elif len(current_text) < len(target_text): 
            current_text.append(key)
            if len(current_text) == len(target_text) and "".join(current_text) == target_text:
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
        stdscr.nodelay(False)
        key = stdscr.getkey()

        if ord(key) == 27: 
            break

# wrapper: takes a function and runs it in a curses window
wrapper(main)