# Name: engine.py
# Description: Contains the code related to analyzing typing, separated from printing it (main.py)
# Author: Sanika Surose

import random
import time

# create_session: initializes and returns a new typing test session dictionary with all state
def create_session():
    return {
        "target_text": load_text(),
        "current_text": [],
        "start_time": time.time(),
        "finished": False
    }

# process_key: updates session state based on the given key input (handles typing and backspace)
def process_key(session, key):
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        if session["current_text"]:
            session["current_text"].pop()
    elif len(session["current_text"]) < len(session["target_text"]):
        session["current_text"].append(key)

    if (
        len(session["current_text"]) == len(session["target_text"])
        and "".join(session["current_text"]) == session["target_text"]
    ):
        session["finished"] = True

# calculate_wpm: calculates the wpm for the current session
def calculate_wpm(session):
    elapsed = max(time.time() - session["start_time"], 1)
    return round((len(session["current_text"]) / (elapsed / 60)) / 5)


# load_text: loads target text from text.txt file
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

# build_char_states: decides if current character user is typing is correct or not
def build_char_states(target_text, current_text): 
    char_states = []

    for i, target_char in enumerate(target_text):
        if i < len(current_text):
            if current_text[i] == target_char:
                char_states.append((target_char, "correct"))
            else: 
                char_states.append((target_char, "incorrect"))
        else: 
            char_states.append((target_char, "untyped"))

    return char_states