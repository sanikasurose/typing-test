# Name: gui.py
# Description: Contains the graphical user interface code for the typing test application
# Author: Sanika Surose

from re import T
import customtkinter as ctk
import tkinter as tk
import engine

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
        self.results_screen = ResultsScreen(self)
        self.progress_screen = ProgressScreen(self)

        self.show_start()

        self.root.focus_force()
        self.start_screen.start_button.focus_set()
        self.root.mainloop()

    # show_start: shows the start screen
    def show_start(self): 
        self._hide_all()
        self.start_screen.show()

    # show_typing: shows the typing screen
    def show_typing(self): 
        self._hide_all()
        self.typing_screen.start_test()
        self.typing_screen.show()

    # show_results: shows the results screen
    def show_results(self): 
        self._hide_all()
        self.results_screen.load_session(session)
        self.results_screen.show()

    # show_progress: shows the progress screen
    def show_progress(self):
        self._hide_all()
        self.progress_screen.refresh()
        self.progress_screen.show()

    # helper function to hide all
    def _hide_all(self):
        self.start_screen.hide()
        self.typing_screen.hide()
        self.results_screen.hide()
        self.progress_screen.hide()


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
    # __init__: intializes the typing screen
    def __init__(self, app): 
        self.app = app
        self.session = None

        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Type the text below", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.pack(pady=10)

        # tk.Text is used because CustomTkinter does not support per-character coloring
        self.text_display = tk.Text(self.frame, font=("Courier", 16), wrap=tk.WORD, width=70, height=5, state=tk.DISABLED)
        self.text_display.pack(pady=20)

        # character coloring
        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("incorrect", foreground="red")
        self.text_display.tag_config("untyped", foreground="gray")

        self.stats_label = ctk.CTkLabel(self.frame, text="WPM: 0", font=ctk.CTkFont(size=16))
        self.stats_label.pack(pady=10)

    # ---- Lifecycle ----
    def start_test(self):
        self.session = engine.create_session()
        self.update_display()
        self.update_wpm()

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.app.root.bind("<Key>", self.on_key_press)

    def hide(self):
        self.app.root.unbind("<Key>")
        self.frame.pack_forget()

    # ---- Input Handling ----
    def on_key_press(self, event):
        if not self.session or not self.frame.winfo_ismapped():
            return

        if self.session["finished"]:
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
            self.app.show_results(self.session)

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

    def show_results(self):
        acc = engine.calculate_accuracy(self.session)
        wpm = engine.calculate_wpm(self.session)

        self.stats_label.configure(text=f"Done! WPM: {engine.calculate_wpm(self.session)} | Accuracy: {acc}% | Press Enter for new test")


class ResultsScreen: 
    """
    Results screen definition
    """
    # __init__: constructor function
    def __init__(self, app):
        self.app = app
        self.session = None
        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Performance Feedback", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.pack(pady=20)

        self.body = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=16, justify="left"))
        self.body.pack(pady=10)

        self.continue_button = ctk.CTkButton(self.frame, text="Continue", width=200, height=40, command=self.app.show_progress)
        self.continue_button.pack(pady=30)

    def load_session(self, session): 
        self.session = session

        profile = engine.get_performance_profile(session)
        consistency = engine.get_speed_feedback(session)
        weak_keys = engine.get_weak_keys(session)
        avg_delay = engine.get_average_key_delay(session)
        tip = engine.get_actionable_tip(session)

        weak_keys_str = ", ".join(k for k, _ in weak_keys) if weak_keys else "None"
        
        text = (
            f"Profile: {profile}\n"
            f"Typing Consistency: {consistency}\n\n"
            f"Weak Keys: {weak_keys_str}\n"
            f"Avg key delay: {avg_delay}s\n\nTip: {tip}"
        )
        self.body.configure(text=text)

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.app.root.bind("<Return>", self._continue)

    def hide(self):
        self.app.root.unbind("<Return>")
        self.frame.pack_forget()

    def _continue(self, event=None):
        self.app.show_progress()


class ProgressScreen: 
    """
    Loads the progress/feedback screen
    """
    def __init__(self, app): 
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Your Progress", font=ctk.CTkFont(size=28, weight="bold"))
        self.title.pack(pady=20)

        self.stats_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=16), justify="left")
        self.stats_label.pack(pady=10)

        self.continue_button = ctk.CTkButton(self.frame, text="New Test", width=200, height=40, command=self.app.show_typing)
        self.continue_button.pack(pady=30)

    def refresh(self):
        stats = engine.get_progress_stats()
        if not stats:
            self.stats_label.configure(text="No data yet.")
            return

        text = (
            f"Total Tests: {stats['total_tests']}\n"
            f"Best WPM: {stats['best_wpm']}\n"
            f"Average WPM: {stats['avg_wpm']}\n"
            f"Average Accuracy: {stats['avg_accuracy']}%"
        )
        self.stats_label.configure(text=text)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

# Run App
TypingTest()