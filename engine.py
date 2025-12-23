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
        "finished": False,
        "mistakes": 0,
        "total_keystrokes": 0, 

        # v1.2.0 analytics
        "char_errors": {},      
        "char_timings": {}, 
        "last_key_time": None
    }

# load_text: loads target text from text.txt file
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

# process_key: updates session state based on the given key input (handles typing and backspace)
def process_key(session, key):

    now = time.time()

    # timing analytics
    if session["last_key_time"] is not None: 
        delay = now - session["last_key_time"]
    else: 
        delay = None

    session["last_key_time"] = now

    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        if session["current_text"]:
            session["current_text"].pop()
        return 

    if len(session["current_text"]) >= len(session["target_text"]):
        return 

    expected = session["target_text"][len(session["current_text"])]
    session["current_text"].append(key)
    session["total_keystrokes"] += 1

    # record timing per character 
    if delay is not None: 
        session["char_timings"].setdefault(expected, []).append(delay)

    # mistake tracking
    if key != expected: 
        session["mistakes"] += 1
        session["char_errors"][expected] = session["char_errors"].get(expected, 0) + 1

    if len(session["current_text"]) == len(session["target_text"]):
        session["finished"] = True

# calculate_wpm: calculates the wpm for the current session
def calculate_wpm(session):
    elapsed = max(time.time() - session["start_time"], 1)
    return round((len(session["current_text"]) / (elapsed / 60)) / 5)

# calculate_accuracy: calculates and returns the typing accuracy percentage for the current session
def calculate_accuracy(session):
    if session["total_keystrokes"] == 0:
        return 100.0
    correct = session["total_keystrokes"] - session["mistakes"]
    return round((correct / session["total_keystrokes"]) * 100, 2)

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

# analytics helpers (for version v1.2.0)
# get_top_mistakes: returns the top 5 characters where users made most mistakes
def get_top_mistakes(session, limit=5): 
    return sorted(
        session["char_errors"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:limit]

# get_average_key_delay: calculates and returns the average delay (in seconds) between key presses for the current session
def get_average_key_delay(session): 
    delays = []
    for times in session["char_timings"].values(): 
        delays.extend(times)

    if not delays: 
        return 0.0

    return round(sum(delays) / len(delays), 3)