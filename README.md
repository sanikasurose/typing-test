# 🧠 Typing Test (v1.3.0)

A lightweight, terminal-based speed typing test built with Python and the `curses` library.  
This version introduces a **dedicated post-test feedback screen**, transforming raw typing metrics into **clear, coaching-style performance insights**.

The program displays a target sentence, highlights keystrokes in real time (green for correct, red for incorrect), calculates words-per-minute (WPM), and presents a clean results screen with accuracy, mistakes, and typing analytics after each session.

---

## ✨ Features
- Real-time per-character accuracy highlighting
- Live WPM (words per minute) calculation
- Typing accuracy percentage based on total keystrokes
- Mistake counting (not undone by backspacing)
- Per-character mistake analytics (top problem keys)
- Average keystroke delay tracking
- **Dedicated post-test feedback screen**
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
6. A **separate results screen** appears displaying:
   - Final WPM
   - Accuracy percentage
   - Total mistakes
   - Top mistyped characters
   - Average delay between key presses
7. Press any key to start a new test, or press **ESC** to exit.

--- 

## 🧩 How It Works

### Project Structure
- **`main.py`**
  - Handles all terminal UI rendering using the `curses` library
  - Manages screen transitions (typing screen → results screen)
  - Displays text, colors, live stats, and post-test feedback
  - Controls program flow and user input

- **`engine.py`**
  - Contains all typing logic and session state
  - Tracks keystrokes, mistakes, and per-character errors
  - Records timing between key presses
  - Calculates WPM, accuracy, and analytics
  - Exposes reusable helper functions for statistics

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
- Results are shown on a **clean, dedicated feedback screen**, not mixed with the typing UI


---

## 🚀 Learning Goals & Future Vision

This project is intentionally designed as a **learning-focused, scalable application**, not just a small script.

### What I’ve Learned So Far
- Designing clean project architecture with separation of concerns
- Managing application state independently of UI
- Implementing real-time input handling with `curses`
- Tracking meaningful performance metrics (WPM, accuracy, mistakes)
- Building typing analytics (error frequency, timing, weak keys)
- Creating clear user feedback through multi-screen terminal UI
- Using Git professionally (commits, tags, releases, README-driven development)

### Future Enhancements
- **Session History & Progress Tracking**
  - Store past results
  - Track improvement over time

- **Advanced Typing Analytics**
  - Per-character accuracy heatmaps
  - Weak-key trend analysis

- **Personal AI Typing Coach**
  - Analyze typing behavior
  - Recommend targeted practice sessions

- **GUI Version**
  - Transition from terminal UI to a graphical interface (Tkinter / PyQt / Web)

- **Cloud Deployment**
  - User accounts
  - Saved progress
  - Leaderboards and statistics

--- 

**Author:** Sanika Surose     
**Current version:** v1.3.0  
**Next milestone:** v1.4.0 → practice mode & targeted drills  
**Long-term goal:** cloud-hosted, AI-assisted typing platform  