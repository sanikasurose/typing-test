# Name: engine.py
# Description: Contains the code related to analyzing typing, separated from printing it (main.py)
# Author: Sanika Surose

import random
import time
import json
import os

# constants
SESSION_FILE = "sessions.json"


# create_session: initializes and returns a new typing test session dictionary with all states
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

# get_performance_profile: classifies overall typing performance based on WPM and accuracy
def get_performance_profile(session):
    wpm = calculate_wpm(session)
    accuracy = calculate_accuracy(session)

    if wpm >= 60 and accuracy >= 95:
        return "Balanced"
    elif wpm >= 60 and accuracy < 95:
        return "Fast but inaccurate"
    elif wpm < 40 and accuracy >= 95:
        return "Accurate but slow"
    else: 
        return "Needs consistency"

# get_weak_keys: returns the most frequently mistyped characters
def get_weak_keys(session, limit=3):
    errors = session.get("char_errors", {})
    if not errors:
        return []

    return sorted(errors.items(), key=lambda x: x[1], reverse=True)[:limit]

# get_speed_feedback: analyzes typing consistency using key delay variance
def get_speed_feedback(session):
    delays = []
    for times in session.get("char_timings", {}).values():
        delays.extend(times)

    if len(delays) < 5:
        return "Not enough data"

    avg = sum(delays) / len(delays)
    variance = sum((d - avg) ** 2 for d in delays) / len(delays)

    if variance < 0.01:
        return "Consistent typing speed"
    else:
        return "Inconsistent typing speed"

# get_actionable_tip: provides a short recommendation based on accuracy and speed
def get_actionable_tip(session):
    wpm = calculate_wpm(session)
    accuracy = calculate_accuracy(session)

    if accuracy < 90:
        return "Slow down slightly to improve accuracy"
    elif wpm < 40:
        return "Focus on building speed with accuracy"
    elif accuracy >= 95 and wpm >= 60:
        return "Great balance — keep practicing consistency"
    else:
        return "Practice common word patterns and transitions"


# load_sessions: loads and returns the list of all saved typing test sessions from file
def load_sessions():
    if not os.path.exists(SESSION_FILE):
        return []
    with open(SESSION_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # File is empty or corrupt; treat as no sessions
            return []


# save_session: saves the current typing test session summary to the sessions file
def save_session(session):
    sessions = load_sessions()

    record = {
        "timestamp": time.time(),
        "wpm": calculate_wpm(session),
        "accuracy": calculate_accuracy(session),
        "mistakes": session["mistakes"]
    }

    sessions.append(record)

    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f, indent=2)


# get_progress_stats: computes and returns summary statistics about the user's typing progress across all sessions
def get_progress_stats():
    sessions = load_sessions()
    if not sessions:
        return None

    total = len(sessions)
    best_wpm = max(s["wpm"] for s in sessions)
    avg_wpm = round(sum(s["wpm"] for s in sessions) / total, 1)
    avg_acc = round(sum(s["accuracy"] for s in sessions) / total, 1)

    return {
        "total_tests": total,
        "best_wpm": best_wpm,
        "avg_wpm": avg_wpm,
        "avg_accuracy": avg_acc
    }