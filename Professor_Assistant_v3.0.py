import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os


# --- 1. Configuration Class (For Constants) ---
class CONFIG:
    """Central location for configuration constants."""
    BG_PRIMARY = "#f0f0f0"
    BG_ACCENT = "#e3f2fd"
    FG_TEXT = "#333"
    BTN_PRIMARY = "#03a9f4"
    BTN_SUCCESS = "#4CAF50"
    FONT_TITLE = ("Arial", 24, "bold")
    FONT_HEADER = ("Arial", 18, "bold")
    FONT_BODY = ("Arial", 12)
    QUESTION_DELIMITER = "---"  # Robust separator for questions


# --- 2. Exam Generator Class (Decoupled Logic) ---
class ExamGenerator:
    """Handles all data loading, parsing, and random selection logic."""

    def __init__(self, delimiter=CONFIG.QUESTION_DELIMITER):
        self.question_bank = []
        self.delimiter = delimiter

    def load_bank_robust(self, file_path):
        """
        Loads questions using a specific delimiter, making the parser
        more robust than the V2.0 alternating line method.
        """
        self.question_bank = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split content by the robust delimiter "---"
            raw_pairs = content.split(self.delimiter)

            for pair in raw_pairs:
                # Get non-empty lines, strip whitespace
                parts = [line.strip() for line in pair.split('\n') if line.strip()]

                if len(parts) >= 2:
                    # Assume first non-empty line is question, second is answer
                    self.question_bank.append({
                        'question': parts[0],
                        'answer': parts[1]
                    })

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Failed to read file due to format error: {e}")

        return len(self.question_bank)

    def generate_content(self, num_questions, professor_name):
        """Generates exam content based on V1.0 logic."""
        if num_questions > len(self.question_bank):
            raise ValueError("Requested questions exceed bank size.")

        selected = random.sample(self.question_bank, num_questions)

        exam_content = f"EXAM (STUDENT COPY) - Created by Professor {professor_name}\n"
        exam_content += "=" * 60 + "\n\n"

        for i, pair in enumerate(selected, 1):
            exam_content += f"Question {i}: {pair['question']}\n"
            exam_content += f"Answer: ______________________\n\n"

        return exam_content


# --- 3. Main Application Class (Handles State and Frame Switching) ---
class ProfessorAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professor Assistant v3.0 (Advanced Structure)")
        self.geometry("600x500")
        self.configure(bg=CONFIG.BG_PRIMARY)

        # State and Logic (Decoupled)
        self.professor_name = ""
        self.file_name = ""
        self.generator = ExamGenerator()  # Instantiate the logic handler

        # Container Frame: All screens will be placed here
        container = tk.Frame(self, bg=CONFIG.BG_PRIMARY)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create all screens as Frame objects
        for F in (WelcomeFrame, AskCreateFrame, UploadFrame, DetailsFrame, SuccessFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            # Place all frames in the same grid spot (0,0)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeFrame")

    def show_frame(self, frame_name):
        """Frame-per-Screen Logic: Raises the desired frame to the top."""
        frame = self.frames[frame_name]
        frame.tkraise()

    def quit_program(self):
        self.destroy()


# --- 4. Specialized Frame Classes (The Views) ---

class WelcomeFrame(tk.Frame):
    """Screen 1: Welcome and Name Input"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CONFIG.BG_PRIMARY)
        self.controller = controller

        # Title
        title = tk.Label(self, text="📚 Professor Assistant",
                         font=CONFIG.FONT_TITLE, bg=CONFIG.BG_PRIMARY, fg=CONFIG.FG_TEXT)
        title.pack(pady=30)

        version = tk.Label(self, text="Version 3.0 (Robust Structure)",
                           font=CONFIG.FONT_BODY, bg=CONFIG.BG_PRIMARY, fg="#666")
        version.pack()

        # ... (rest of the welcome screen widgets) ...
        name_label = tk.Label(self, text="Please Enter Your Name:",
                              font=CONFIG.FONT_BODY, bg=CONFIG.BG_PRIMARY, fg=CONFIG.FG_TEXT)
        name_label.pack(pady=10)

        self.name_entry = tk.Entry(self, font=CONFIG.FONT_BODY, width=30)
        self.name_entry.pack(pady=10)

        continue_btn = tk.Button(self, text="Continue",
                                 font=CONFIG.FONT_BODY, bg=CONFIG.BTN_PRIMARY, fg="white",
                                 padx=30, pady=10, command=self.save_name)
        continue_btn.pack(pady=20)

    def save_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            return

        self.controller.professor_name = name
        self.controller.show_frame("AskCreateFrame")


class AskCreateFrame(tk.Frame):
    """Screen 2: Ask to Upload"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CONFIG.BG_PRIMARY)
        self.controller = controller

        tk.Label(self, text=f"Hello Professor!",  # Name will be updated dynamically later
                 font=CONFIG.FONT_HEADER, bg=CONFIG.BG_PRIMARY, fg=CONFIG.FG_TEXT).pack(pady=30)

        tk.Label(self, text="Ready to upload your question bank file (.txt)?",
                 font=CONFIG.FONT_BODY, bg=CONFIG.BG_PRIMARY).pack(pady=20)

        button_frame = tk.Frame(self, bg=CONFIG.BG_PRIMARY)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Yes, Upload Now",
                  font=CONFIG.FONT_BODY, bg=CONFIG.BTN_SUCCESS, fg="white",
                  padx=40, pady=10, command=lambda: self.controller.show_frame("UploadFrame")).pack(side=tk.LEFT,
                                                                                                    padx=10)

        tk.Button(button_frame, text="Exit",
                  font=CONFIG.FONT_BODY, bg="#f44336", fg="white",
                  padx=40, pady=10, command=self.controller.quit_program).pack(side=tk.LEFT, padx=10)


class UploadFrame(tk.Frame):
    """Screen 3: File Upload and Loading"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CONFIG.BG_PRIMARY)
        self.controller = controller

        # Button to trigger file dialog
        tk.Button(self, text="Select Question Bank (.txt)",
                  font=CONFIG.FONT_HEADER, bg=CONFIG.BTN_PRIMARY, fg="white",
                  padx=40, pady=20, command=self.load_question_bank).pack(pady=50)

    def load_question_bank(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Select Question Bank File"
        )

        if not file_path:
            # User cancelled, go back
            self.controller.show_frame("AskCreateFrame")
            return

        try:
            # Use the decoupled generator logic
            num_loaded = self.controller.generator.load_bank_robust(file_path)

            if num_loaded > 0:
                self.controller.file_name = os.path.basename(file_path)
                messagebox.showinfo("Success",
                                    f"Loaded {num_loaded} questions from the bank! (Using DELIMITER: {CONFIG.QUESTION_DELIMITER})")
                self.controller.show_frame("DetailsFrame")
            else:
                messagebox.showerror("Error",
                                     f"Loaded 0 questions. Check file format, ensure Q/A pairs are separated by '{CONFIG.QUESTION_DELIMITER}'.")
                self.controller.show_frame("AskCreateFrame")

        except Exception as e:
            messagebox.showerror("File Error", str(e))
            self.controller.show_frame("AskCreateFrame")


class DetailsFrame(tk.Frame):
    """Screen 4: Exam Details Input"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CONFIG.BG_PRIMARY)
        self.controller = controller

        # Layout will be dynamic, so we focus on the buttons here
        self.pack_propagate(False)  # Keep frame size fixed when content changes

        # Widgets
        tk.Label(self, text="Enter number of questions for the exam:",
                 font=CONFIG.FONT_BODY, bg=CONFIG.BG_PRIMARY).pack(pady=15)

        self.num_entry = tk.Entry(self, font=CONFIG.FONT_BODY, width=10)
        self.num_entry.pack(pady=5)

        tk.Label(self, text="Enter output filename (e.g., Exam1.txt):",
                 font=CONFIG.FONT_BODY, bg=CONFIG.BG_PRIMARY).pack(pady=15)

        self.output_entry = tk.Entry(self, font=CONFIG.FONT_BODY, width=30)
        self.output_entry.insert(0, "Generated_Exam.txt")
        self.output_entry.pack(pady=5)

        generate_btn = tk.Button(self, text="Generate Exam",
                                 font=CONFIG.FONT_BODY, bg=CONFIG.BTN_SUCCESS, fg="white",
                                 padx=30, pady=10, command=self.generate_exam)
        generate_btn.pack(pady=30)

    def generate_exam(self):
        try:
            num_questions = int(self.num_entry.get())
            output_file = self.output_entry.get().strip()
            total_available = len(self.controller.generator.question_bank)

            if num_questions <= 0 or num_questions > total_available:
                messagebox.showerror("Error", f"Invalid number. Must be between 1 and {total_available}.")
                return

            if not output_file:
                messagebox.showerror("Error", "Please enter a valid output file name.")
                return

            # Use the decoupled generator logic
            exam_content = self.controller.generator.generate_content(
                num_questions,
                self.controller.professor_name
            )

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(exam_content)

            self.controller.file_name = output_file
            self.controller.show_frame("SuccessFrame")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the number of questions.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during generation: {e}")


class SuccessFrame(tk.Frame):
    """Screen 5: Success Message"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=CONFIG.BG_PRIMARY)
        self.controller = controller

        # Widgets are packed here but will be updated when the frame is raised (V4.0 will improve this)
        success_frame = tk.Frame(self, bg="#e8f5e9", bd=2, relief=tk.SOLID)
        success_frame.pack(pady=50, padx=30, fill=tk.BOTH, expand=True)

        tk.Label(success_frame, text="✅ Exam Successfully Generated!",
                 font=CONFIG.FONT_HEADER, bg="#e8f5e9", fg="#2e7d32").pack(pady=30)

        # Placeholder for file name
        tk.Label(success_frame, text="File saved successfully.",
                 font=CONFIG.FONT_BODY, bg="#e8f5e9", fg="#2e7d32").pack(pady=10)

        tk.Button(success_frame, text="Generate Another Exam",
                  font=CONFIG.FONT_BODY, bg=CONFIG.BTN_PRIMARY, fg="white",
                  padx=30, pady=10, command=lambda: self.controller.show_frame("WelcomeFrame")).pack(pady=20)


# --- Main Execution ---
if __name__ == "__main__":
    # Note: To test this version, ensure your question bank file has questions
    # separated by the delimiter: "---"

    # Example file content for V3.0:
    # Question 1: What is the capital of France?
    # Answer: Paris
    # ---
    # Question 2: Who wrote Hamlet?
    # Answer: Shakespeare
    # ---

    app = ProfessorAssistant()
    app.mainloop()