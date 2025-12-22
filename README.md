# 🧠 Typing Test (v1.1.0)

A lightweight, terminal-based speed typing test built with Python and the curses library.
This version focuses on clean architecture and separation of concerns, laying the foundation for future AI and cloud-deployed features.

The program displays a target sentence, highlights keystrokes in real time (green for correct, red for incorrect), and calculates words-per-minute (WPM) as you type.

---

## ✨ Features 
- Real‑time accuracy highlighting 
- Live WPM calculation 
- Randomized text selection from `text.txt` 
- Non‑blocking input handling for smooth UI 
- Modular codebase with separated logic and UI
- Simple, clean terminal interface

--- 

## 🎮 How to Play 

1. Press any key to begin the typing test. 
2. Type the displayed text exactly as it appears on the screen. 
3. Characters you type will be highlighted: 
    - **Green** for correct characters  
    - **Red** for incorrect characters 
4. Your WPM (words per minute) updates continuously as you type. 
5. When you finish typing the entire line correctly, the test ends and displays **Done!** 
6. Press any key to start a new test, or press **ESC** to exit the program.

--- 

## 🧩 How It Works

### Project Structure
- **`main.py`**
  - Handles all terminal UI rendering using the `curses` library  
  - Manages user input, screen updates, and overall program flow  
  
- **`engine.py`**
  - Contains the core typing logic  
  - Determines per-character typing states (`correct`, `incorrect`, `untyped`)  
  - Keeps business logic separate from UI logic  

This separation improves readability, maintainability, and makes future extensions (GUI, AI, cloud) much easier.

### Typing Logic
- A random line is loaded from `text.txt` and used as the target phrase  
- As the user types, each character is compared against the target text  
- Character states are computed in `engine.py` and rendered in `main.py`  
- WPM is calculated using: WPM = (characters_typed / 5) / minutes_elapsed
- The test ends when:
  - The user presses **ESC**, or  
  - The typed text exactly matches the target text  

---

## 🚀 Learning Goals & Future Vision

This project is designed as a **hands-on learning experience**, not just a small console application.

### What I’ve Learned So Far
- Structuring a project with clear separation of concerns  
- Designing reusable logic independent of UI implementation  
- Working with terminal-based UIs using `curses`  
- Writing meaningful commit messages, tags, and release notes  

### Future Enhancements
- **Personal AI Typing Coach**
  - Analyze typing patterns and common mistakes  
  - Suggest targeted practice exercises and improvements  

- **Cloud Deployment**
  - Deploy the final application on the cloud  
  - Enable user progress tracking and persistence  

- **GUI Version**
  - Transition from a terminal-based interface to a full graphical UI  

- **Internship-Ready Skills**
  - Modular design patterns  
  - Scalable architecture  
  - Real-world development workflows 

--- 

**Author:** Sanika Surose  
**Next milestone:** v1.2.0 → typing analytics & performance tracking
**Long-term goal:** cloud-hosted, AI-assisted typing platform