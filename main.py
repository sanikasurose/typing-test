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

    stdscr.addstr(row, 0, "Press any key to view feedback")
    stdscr.refresh()
    stdscr.getkey()


# show_feedback_screen: displays post-test feedback and personalized tips for improvement
def show_feedback_screen(stdscr, session):
    profile = engine.get_performance_profile(session)
    weak_keys = engine.get_weak_keys(session)
    speed_feedback = engine.get_speed_feedback(session)
    tip = engine.get_actionable_tip(session)
    avg_delay = engine.get_average_key_delay(session)

    stdscr.clear()
    row = 0

    stdscr.addstr(row, 0, "Performance Feedback")
    row += 2

    stdscr.addstr(row, 0, f"Profile: {profile}")
    row += 1

    stdscr.addstr(row, 0, f"Typing consistency: {speed_feedback}")
    row += 2

    if weak_keys:
        keys = ", ".join(char for char, _ in weak_keys)
        stdscr.addstr(row, 0, f"Weak keys: {keys}")
        row += 1
    else:
        stdscr.addstr(row, 0, "Weak keys: None 🎉")
        row += 1

    stdscr.addstr(row, 0, f"Avg key delay: {avg_delay:.2f}s")
    row += 2

    stdscr.addstr(row, 0, f"Tip: {tip}")
    row += 2

    stdscr.addstr(row, 0, "Press any key to continue")
    stdscr.refresh()
    stdscr.getkey()

# show_progress_screen: displays the user's typing progress and stats across all saved sessions
def show_progress_screen(stdscr):
    stats = engine.get_progress_stats()

    stdscr.clear()
    row = 0

    stdscr.addstr(row, 0, "Progress Summary")
    row += 2

    if not stats:
        stdscr.addstr(row, 0, "No history yet. Complete more tests!")
    else:
        stdscr.addstr(row, 0, f"Total tests: {stats['total_tests']}")
        row += 1
        stdscr.addstr(row, 0, f"Best WPM: {stats['best_wpm']}")
        row += 1
        stdscr.addstr(row, 0, f"Average WPM: {stats['avg_wpm']}")
        row += 1
        stdscr.addstr(row, 0, f"Average Accuracy: {stats['avg_accuracy']}%")

    row += 2
    stdscr.addstr(row, 0, "Press any key to continue")
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

    # save completed session
    if session["finished"]:
        engine.save_session(session)

    show_results(stdscr, session)
    show_feedback_screen(stdscr, session)
    show_progress_screen(stdscr)

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