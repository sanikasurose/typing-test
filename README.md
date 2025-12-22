# 🧠 Typing Test (v1.0.0)

A lightweight, terminal‑based **speed typing test** built with Python and the `curses` library. 
It displays a target sentence, highlights your keystrokes in real time (green for correct, red for incorrect), and calculates your words‑per‑minute (WPM) as you type. 

---

## ✨ Features 
- Real‑time accuracy highlighting 
- Live WPM calculation 
- Randomized text selection from `text.txt` 
- Non‑blocking input handling for smooth UI 
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

- The program loads a random line of text from `text.txt` to use as the target phrase. 
- As you type, each character is compared to the corresponding character in the target text. 
- Correctly typed characters are shown in green; incorrect ones are shown in red. 
- WPM is calculated using the formula: 

    WPM = (characters_typed / 5) / minutes_elapsed 

- The program ends the test when: 
- The user presses **ESC**, or 
- The typed text exactly matches the target text in length and content. 

--- 

**Author:** Sanika Surose  
*Note:* v2.0.0 will be a GUI version