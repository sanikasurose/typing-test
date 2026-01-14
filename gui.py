# Name: gui.py
# Description: Contains the graphical user interface code for the typing test application
# Author: Sanika Surose

import customtkinter as ctk
import tkinter as tk
import engine
import time

"""
Tkinter Notes: 
- variable ==> how you specify that a certain button/action has an associated variable
- command ==> how you specify that a certain button/action has an associated function that gets called when you press it
"""

# -- App Config ---
ctk.set_appearance_mode("dark")                                     # set the appearance mode to dark (tuple of different colors)
ctk.set_default_color_theme("dark-blue")                            # set the default color theme to dark-blue


class TypingTest: 
    """
    App controller; owns the window and switches between screens
    """
    # __init__: initializes the main application window and creates all screen components
    def __init__(self): 
        self.root = ctk.CTk()                                       
        self.root.title("Typing Test v2.0.0")                       
        self.root.geometry("900x500")

        # Screens
        self.start_screen = StartScreen(self)
        self.typing_screen = TypingScreen(self)

        self.show_start()

        self.root.focus_force()
        self.start_screen.start_button.focus_set()

        self.root.mainloop()

    # show_start: shows the start screen
    def show_start(self): 
        self.typing_screen.hide()
        self.start_screen.show()

    # show_typing: shows the typing screen
    def show_typing(self): 
        self.start_screen.hide()
        self.typing_screen.start_test()
        self.typing_screen.show()


class StartScreen: 
    """
    Contains the code to display the welcome screen with a start button to begin the typing test
    """
    # __init__: initializes the start screen with title and start button
    def __init__(self, app): 
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Typing Test", font=ctk.CTkFont(size=32, weight="bold"))
        self.title.pack(pady=30)

        self.start_button = ctk.CTkButton(self.frame, text="Start", width=200, height=40, command=self.app.show_typing)
        self.start_button.pack(pady=30)

    # show: displays the start screen frame
    def show(self):
        self.frame.pack(fill="both", expand=True)

    # hide: hides the start screen frame
    def hide(self):
        self.frame.pack_forget()


class TypingScreen: 
    """
    Contains the code to display the typing screen
    """
    TEST_DURATION = 30 # seconds

    # __init__: intializes the typing screen
    def __init__(self, app): 
        self.app = app
        self.session = None
        self.start_time = None
        self.remaining_time = self.TEST_DURATION
        self.timer_running = False

        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Type the text below", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self.frame, text="Time: 30", font=ctk.CTkFont(size=16))
        self.timer_label.pack(pady=5)

        # tk.Text is used because CustomTkinter does not support per-character coloring
        self.text_display = tk.Text(self.frame, font=("Courier", 16), wrap=tk.WORD, width=70, height=5, state=tk.DISABLED)
        self.text_display.pack(pady=20)

        # character coloring
        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("incorrect", foreground="red")
        self.text_display.tag_config("untyped", foreground="gray")

        self.stats_label = ctk.CTkLabel(self.frame, text="WPM: 0", font=ctk.CTkFont(size=16))
        self.stats_label.pack(pady=10)

        app.root.bind("<Key>", self.on_key_press)

    # ---- Lifecycle ----
    def start_test(self):
        self.session = engine.create_session()
        self.start_time = time.time()
        self.remaining_time = self.TEST_DURATION
        self.timer_running = True

        self.update_display()
        self.update_wpm()
        self.update_timer()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def end_test(self):
        self.timer_running = False
        self.session["finished"] = True
        engine.save_session(self.session)
        self.show_results()

    # ---- Input Handling ----
    def on_key_press(self, event):
        if self.session is None:
            return

        if not self.frame.winfo_ismapped():
            return

        if self.session["finished"]:
            if event.keysym == "Return":
                self.start_test()
            return

        if event.keysym == "BackSpace":
            key = "\b"
        elif len(event.char) == 1:
            key = event.char
        else:
            return

        engine.process_key(self.session, key)
        self.update_display()

        if self.session["finished"]:
            engine.save_session(self.session)
            self.show_results()


    # ---- UI Updates ----
    def update_display(self):
        states = engine.build_char_states(self.session["target_text"], self.session["current_text"])

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)

        for char, state in states:
            self.text_display.insert(tk.END, char, state)

        self.text_display.config(state=tk.DISABLED)

    def update_wpm(self):
        if not self.session["finished"]:
            wpm = engine.calculate_wpm(self.session)
            self.stats_label.configure(text=f"WPM: {wpm}")
            self.app.root.after(500, self.update_wpm)

    def update_timer(self):
        if not self.timer_running: 
            return

        elapsed = int(time.time() - self.start_time)
        self.remaining_time = max(0, self.TEST_DURATION - elapsed)
        self.timer_label.configure(text=f"Time: {self.remaining_time}")

        if self.remaining_time == 0:
            self.end_test()
            return
        
        self.app.root.after(250, self.update_timer)

    def show_results(self):
        acc = engine.calculate_accuracy(self.session)
        wpm = engine.calculate_wpm(self.session)

        self.stats_label.configure(text=f"Done! WPM: {engine.calculate_wpm(self.session)} | Accuracy: {acc}% | Press Enter for new test")


# Run App
TypingTest()