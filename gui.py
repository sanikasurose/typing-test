# Name: gui.py
# Description: Contains the graphical user interface code for the typing test application
# Author: Sanika Surose

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

# -- Screen State Constants --
class ScreenState:
    """Explicit screen state constants for UI state management."""
    START = "start"
    TYPING = "typing"
    RESULTS = "results"
    PROGRESS = "progress"


class TypingTest: 
    """
    Central application controller managing screen lifecycle and navigation.
    
    Responsibilities:
    - Own the main application window (CustomTkinter CTk)
    - Create and manage all screen instances
    - Coordinate screen transitions
    - Track active screen state
    - Implement show/hide pattern for screen switching
    
    Architecture Pattern: Controller Pattern
    """
    def __init__(self): 
        self.root = ctk.CTk()                                       
        self.root.title("Typing Test v2.0.1")                       
        self.root.geometry("900x500")

        # Screen state tracking
        self.current_screen = None

        # Screens
        self.start_screen = StartScreen(self)
        self.typing_screen = TypingScreen(self)
        self.results_screen = ResultsScreen(self)
        self.progress_screen = ProgressScreen(self)

        self.show_start()

        self.root.focus_force()
        self.start_screen.start_button.focus_set()
        self.root.mainloop()

    def show_start(self): 
        """Transition to start screen (application entry point)."""
        self._hide_all()
        self.start_screen.show()
        self.current_screen = ScreenState.START

    def show_typing(self): 
        """Transition to typing screen (creates new session)."""
        self._hide_all()
        self.typing_screen.start_test()
        self.typing_screen.show()
        self.current_screen = ScreenState.TYPING

    def show_results(self, session): 
        """Transition to results screen with session data."""
        self._hide_all()
        self.results_screen.load_session(session)
        self.results_screen.show()
        self.current_screen = ScreenState.RESULTS

    def show_progress(self):
        """Transition to progress screen (refreshes stats)."""
        self._hide_all()
        self.progress_screen.refresh()
        self.progress_screen.show()
        self.current_screen = ScreenState.PROGRESS

    def _hide_all(self):
        """Utility method to hide all screens before showing a new one."""
        self.start_screen.hide()
        self.typing_screen.hide()
        self.results_screen.hide()
        self.progress_screen.hide()


class StartScreen: 
    """
    Welcome screen and application entry point.
    
    Responsibilities:
    - Display application title
    - Provide "Start" button to begin typing test
    - Initialize user session flow
    
    UI Elements:
    - Title label: "Typing Test"
    - Start button (triggers app.show_typing())
    
    Lifecycle:
    - Created once during TypingTest.__init__()
    - Shown on application launch
    - Hidden when transitioning to typing screen
    """
    def __init__(self, app): 
        self.app = app
        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Typing Test", font=ctk.CTkFont(size=32, weight="bold"))
        self.title.pack(pady=30)

        self.start_button = ctk.CTkButton(self.frame, text="Start", width=200, height=40, command=self.app.show_typing)
        self.start_button.pack(pady=30)

    def show(self):
        """Display the start screen frame."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the start screen frame."""
        self.frame.pack_forget()


class TypingScreen: 
    """
    Active typing test interface with real-time feedback.
    
    Responsibilities:
    - Display target text with per-character color coding
    - Handle keyboard input events
    - Update live WPM calculation
    - Manage typing session lifecycle
    - Transition to results screen on completion
    
    UI Elements:
    - Title: "Type the text below"
    - Text display widget (tk.Text) with character-level coloring:
      - Green: correct characters
      - Red: incorrect characters
      - Gray: untyped characters
    - Live WPM stat label (updates every 500ms)
    
    Key Methods:
    - start_test(): Creates new session via engine.create_session()
    - on_key_press(): Processes keystrokes through engine.process_key()
    - update_display(): Renders character states via engine.build_char_states()
    - update_wpm(): Polls engine.calculate_wpm() every 500ms
    
    Event Handling:
    - Binds <Key> events when shown
    - Unbinds when hidden to prevent input leakage
    - Converts Tkinter key events to engine-compatible format
    
    Session Management:
    - Owns self.session dictionary (created by engine)
    - Saves session via engine.save_session() on completion
    - Passes session to results screen on transition
    """
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

    def start_test(self):
        """Create new session and initialize display."""
        self.session = engine.create_session()
        self.update_display()
        self.update_wpm()

    def show(self):
        """Display screen and bind keyboard events."""
        self.frame.pack(fill="both", expand=True)
        self.app.root.bind("<Key>", self.on_key_press)

    def hide(self):
        """Hide screen and unbind keyboard events."""
        self.app.root.unbind("<Key>")
        self.frame.pack_forget()

    def on_key_press(self, event):
        """Process keyboard input and update session state."""
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

    def update_display(self):
        """Render character states with color coding."""
        states = engine.build_char_states(self.session["target_text"], self.session["current_text"])

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)

        for char, state in states:
            self.text_display.insert(tk.END, char, state)

        self.text_display.config(state=tk.DISABLED)

    def update_wpm(self):
        """Update WPM display every 500ms while test is active."""
        if not self.session["finished"]:
            wpm = engine.calculate_wpm(self.session)
            self.stats_label.configure(text=f"WPM: {wpm}")
            self.app.root.after(500, self.update_wpm)


class ResultsScreen: 
    """
    Display comprehensive test results and performance feedback.
    
    Responsibilities:
    - Show final WPM and accuracy
    - Display performance profile classification
    - Show typing consistency analysis
    - List weak keys (most frequently mistyped characters)
    - Display average key delay
    - Provide actionable improvement tip
    - Transition to progress screen
    
    UI Elements:
    - Title: "Performance Feedback"
    - Multi-line text label displaying:
      - WPM
      - Accuracy percentage
      - Performance profile
      - Typing consistency
      - Weak keys list
      - Average key delay
      - Actionable tip
    - Continue button (triggers app.show_progress())
    
    Key Methods:
    - load_session(session): Populates display with session data
    - Uses multiple engine analytics functions:
      - engine.calculate_wpm()
      - engine.calculate_accuracy()
      - engine.get_performance_profile()
      - engine.get_speed_feedback()
      - engine.get_weak_keys()
      - engine.get_average_key_delay()
      - engine.get_actionable_tip()
    
    Navigation:
    - Continue button → Progress screen
    - Enter key → Progress screen (keyboard shortcut)
    """
    def __init__(self, app):
        self.app = app
        self.session = None
        self.frame = ctk.CTkFrame(app.root)

        self.title = ctk.CTkLabel(self.frame, text="Performance Feedback", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.pack(pady=20)

        self.body = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=16), justify="left")
        self.body.pack(pady=10)

        self.continue_button = ctk.CTkButton(self.frame, text="Continue", width=200, height=40, command=self.app.show_progress)
        self.continue_button.pack(pady=30)

    def load_session(self, session): 
        """Load session data and populate display with analytics."""
        self.session = session

        wpm = engine.calculate_wpm(session)
        accuracy = engine.calculate_accuracy(session)

        profile = engine.get_performance_profile(session)
        consistency = engine.get_speed_feedback(session)
        weak_keys = engine.get_weak_keys(session)
        avg_delay = engine.get_average_key_delay(session)
        tip = engine.get_actionable_tip(session)

        weak_keys_str = ", ".join(k for k, _ in weak_keys) if weak_keys else "None"
        
        text = (
            f"WPM: {wpm}\n"
            f"Accuracy: {accuracy}%\n"
            f"Profile: {profile}\n"
            f"Typing Consistency: {consistency}\n\n"
            f"Weak Keys: {weak_keys_str}\n"
            f"Avg key delay: {avg_delay}s\n\nTip: {tip}"
        )
        self.body.configure(text=text)

    def show(self):
        """Display screen and bind Enter key for navigation."""
        self.frame.pack(fill="both", expand=True)
        self.app.root.bind("<Return>", self._continue)

    def hide(self):
        """Hide screen and unbind Enter key."""
        self.app.root.unbind("<Return>")
        self.frame.pack_forget()

    def _continue(self, event=None):
        """Handle Continue button or Enter key press."""
        self.app.show_progress()


class ProgressScreen: 
    """
    Display long-term progress statistics across all sessions.
    
    Responsibilities:
    - Show aggregate statistics from sessions.json
    - Display total tests completed
    - Show best WPM achieved
    - Display average WPM and accuracy
    - Provide "New Test" action to restart flow
    
    UI Elements:
    - Title: "Your Progress"
    - Multi-line stats label:
      - Total Tests
      - Best WPM
      - Average WPM
      - Average Accuracy
    - New Test button (triggers app.show_typing())
    
    Key Methods:
    - refresh(): Loads latest stats via engine.get_progress_stats()
    - Called automatically when screen is shown
    
    Data Source:
    - Reads from sessions.json via engine.get_progress_stats()
    - Handles empty state ("No data yet.")
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
        """Load latest progress statistics from engine."""
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
        """Display the progress screen."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Hide the progress screen."""
        self.frame.pack_forget()

# Run App
TypingTest()