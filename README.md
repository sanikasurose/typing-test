# 🧠 Typing Test (v1.4.0)

A lightweight, terminal-based speed typing test built with Python and the `curses` library.  
This version introduces **practice mode and targeted drills**, allowing users to actively improve weak keys instead of just viewing performance stats.

The program displays a target sentence, highlights keystrokes in real time (green for correct, red for incorrect), calculates words-per-minute (WPM), and presents **multiple post-test screens**, including detailed feedback and optional focused practice.

---

## ✨ Features

- Real-time per-character accuracy highlighting
- Live WPM (words per minute) calculation
- Typing accuracy percentage based on total keystrokes
- Mistake counting (not undone by backspacing)
- Per-character mistake analytics (top problem keys)
- Average keystroke delay tracking
- **Dedicated post-test feedback screen**
- **Practice mode with targeted drills**
- Weak-key–focused text generation
- Session-based progress tracking
- Randomized text selection from `text.txt`
- Non-blocking input handling for smooth UI
- Modular architecture with clean separation of logic and UI
- Simple, clean terminal interface

--- 

## 🎮 How to Play 

1. Press any key to begin the typing test.
2. Type the displayed sentence as it appears on the screen.
3. Characters you type are highlighted:
   - **Green** → correct character
   - **Red** → incorrect character
4. Your WPM updates continuously as you type.
5. The test ends automatically when you reach the end of the sentence, regardless of mistakes.
6. A **dedicated results screen** appears showing:
   - Final WPM
   - Accuracy percentage
   - Total mistakes
   - Top mistyped characters
   - Average delay between key presses
7. From the results screen, you may:
   - Start a **targeted practice session**
   - Begin a new typing test
   - Exit the program

---

## 🧠 Practice Mode

Practice mode uses your typing history to generate **focused drills** targeting your weakest keys.

- Text is dynamically generated based on:
  - Most frequently mistyped characters
  - Error patterns from past sessions
- Helps reinforce muscle memory
- Turns analytics into **actionable improvement**

This transforms the project from a typing test into a **learning tool**.

--- 

## 🧩 How It Works

### Project Structure
- **`main.py`**
  - Handles all terminal UI rendering using the `curses` library
  - Manages screen transitions:
    - Typing screen
    - Results screen
    - Practice screen
  - Displays live stats, feedback, and coaching prompts
  - Controls program flow and user input

- **`engine.py`**
  - Contains all typing logic and session state
  - Tracks keystrokes, mistakes, and per-character errors
  - Records timing between key presses
  - Calculates WPM, accuracy, and analytics
  - Generates practice drills based on weak keys
  - Manages session persistence (`sessions.json`)

This separation keeps the codebase readable, maintainable, and easy to extend.

### Typing Logic
- A random line is loaded from `text.txt` and used as the target phrase
- Each keystroke:
  - Advances the cursor
  - Is counted toward total keystrokes
  - Is compared against the expected character
  - Records timing data for analytics
- Mistakes are counted immediately and **not undone by backspacing**
- Accuracy is calculated using:  
  **accuracy = (correct_keystrokes / total_keystrokes) × 100**
- WPM is calculated using:  
  **WPM = (characters_typed / 5) / minutes_elapsed**
- The test ends when:
  - The user presses **ESC**, or
  - The user types the full length of the target sentence
- Results and practice options are displayed on **separate, clean UI screens**


---

## 🚀 Learning Goals & Future Vision

This project is intentionally designed as a **learning-focused, scalable application**, not just a small script.

### What I’ve Learned So Far
- Designing clean project architecture with separation of concerns
- Managing application state independently of UI
- Implementing real-time input handling with `curses`
- Tracking meaningful performance metrics (WPM, accuracy, mistakes)
- Building typing analytics (error frequency, timing, weak keys)
- Designing multi-screen terminal UIs
- Turning analytics into interactive practice workflows
- Using Git professionally (commits, tags, releases, README-driven development)

### Future Enhancements
- **Advanced Analytics Dashboard**
  - Per-key accuracy heatmaps
  - Long-term improvement trends

- **Personal AI Typing Coach**
  - Pattern detection across sessions
  - Adaptive practice recommendations

- **GUI Version**
  - Transition from terminal UI to a graphical interface (Tkinter / PyQt / Web)

- **Cloud Deployment**
  - User accounts
  - Cross-device progress syncing
  - Leaderboards and performance stats

--- 

**Author:** Sanika Surose   
**Current version:** v1.4.0  
**Next milestone:** v2.0.0 → GUI-based typing application  
**Long-term goal:** cloud-hosted, AI-assisted typing platform  