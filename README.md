# 🧠 Typing Test (v2.0.0)

A feature-rich **graphical typing trainer** built with Python and **CustomTkinter**, fully migrated from a terminal-based application into a modern, multi-screen GUI.

This version preserves **all analytics, feedback, and progress-tracking features** from v1.x while introducing a clean visual workflow with intentional screen transitions and improved usability.

---

## ✨ Features

- Full graphical user interface (CustomTkinter)
- Real-time per-character accuracy highlighting
- Live WPM (words per minute) calculation
- Typing accuracy percentage based on total keystrokes
- Mistake counting (not undone by backspacing)
- Per-character mistake analytics (top problem keys)
- Average keystroke delay tracking
- **Dedicated results screen**
- **Multi-screen feedback flow**
- Session-based progress tracking
- Persistent session history (`sessions.json`)
- Randomized text selection from `text.txt`
- Keyboard-driven input (no mouse required during typing)
- Modular architecture with clean separation of logic and UI
- Dark-mode, distraction-free interface

--- 

## 🎮 How to Play

1. Launch the application.
2. Click **Start** on the welcome screen.
3. Type the displayed sentence as it appears on the screen.
4. Characters you type are highlighted:
   - **Green** → correct character
   - **Red** → incorrect character
5. Your WPM updates continuously as you type.
6. The test ends automatically when you reach the end of the sentence.
7. A **dedicated results screen** appears showing:
   - Final WPM
   - Accuracy percentage
   - Total mistakes
8. Press **Enter** to continue to the **progress summary screen**, which displays long-term stats across all sessions.

---

## 🧠 Feedback & Analytics

Each test is analyzed to provide meaningful feedback beyond raw numbers.

- Performance profile classification:
  - Balanced
  - Fast but inaccurate
  - Accurate but slow
  - Needs consistency
- Weak-key detection (most frequently mistyped characters)
- Typing consistency analysis using keystroke timing variance
- Actionable improvement tips based on speed and accuracy

This ensures users understand **how** they type — not just **how fast**.

--- 

## 🧩 How It Works

### Project Structure

- **`gui.py`**
  - Handles all GUI rendering and screen transitions
  - Manages:
    - Start screen
    - Typing screen
    - Results screen
    - Progress summary screen
  - Handles keyboard events and UI updates
  - Controls application flow

- **`engine.py`**
  - Contains all typing logic and analytics
  - Tracks:
    - Keystrokes
    - Mistakes
    - Per-character errors
    - Keystroke timing
  - Calculates WPM, accuracy, and feedback
  - Manages persistent session storage (`sessions.json`)

This separation keeps the codebase clean, testable, and scalable.

---

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
- The test ends when the full target sentence is typed
- Results, feedback, and progress are displayed on **separate, focused screens**

---

## 🚀 Learning Goals & Future Vision

This project is intentionally designed as a **learning-focused, extensible application**, not just a typing test.

### What I’ve Learned So Far
- Designing clean application architecture with separation of concerns
- Managing application state independently of UI
- Event-driven input handling in GUI applications
- Persisting user data across sessions
- Building typing analytics (errors, timing, consistency)
- Designing intentional multi-screen UX flows
- Migrating a terminal application to a full GUI
- Using Git professionally (commits, tags, releases, README-driven development)

### Future Enhancements
- **Practice Mode**
  - Targeted drills based on weak keys
  - Focused repetition without timing pressure

- **Advanced Analytics Dashboard**
  - Long-term trends
  - Visual performance breakdowns

- **Intelligent Typing Coach**
  - Adaptive practice recommendations
  - Pattern detection across sessions

- **Cloud Deployment**
  - User accounts
  - Cross-device progress syncing
  - Leaderboards and shared stats

---

**Author:** Sanika Surose  
**Current version:** v2.0.0  
**Status:** Stable — Full GUI Migration  
**Next milestone:** v2.x → practice-driven training & intelligence  
**Long-term goal:** cloud-hosted, AI-assisted typing platform
