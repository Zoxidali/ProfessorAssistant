import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os


class ProfessorAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Assistant v2.0")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # application State Variables
        self.professor_name = ""
        self.question_bank = []
        self.file_name = ""

        # Start the application on the first screen
        self.show_welcome_screen()

    def clear_screen(self):
        """Removes all current widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Screen 1: Welcome and Name Input ---
    def show_welcome_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text="📚 Professor Assistant",
                         font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=30)

        version = tk.Label(self.root, text="Version 2.0 (Basic GUI)",
                           font=("Arial", 12), bg="#f0f0f0", fg="#666")
        version.pack()

        welcome = tk.Label(self.root, text="Welcome! Please enter your name to begin:",
                           font=("Arial", 14), bg="#f0f0f0")
        welcome.pack(pady=20)

        self.name_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.name_entry.pack(pady=10)

        continue_btn = tk.Button(self.root, text="Continue",
                                 font=("Arial", 12), bg="#03a9f4", fg="white",
                                 padx=30, pady=10, command=self.save_name)
        continue_btn.pack(pady=20)

    def save_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            return

        self.professor_name = name
        self.show_ask_create_screen()

    # --- Screen 2: Ask to Upload ---
    def show_ask_create_screen(self):
        self.clear_screen()

        title = tk.Label(self.root, text=f"Hello Professor {self.professor_name}!",
                         font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=30)

        question = tk.Label(self.root, text="Ready to upload your question bank file (.txt)?",
                            font=("Arial", 14), bg="#f0f0f0")
        question.pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        yes_btn = tk.Button(button_frame, text="Yes, Upload Now",
                            font=("Arial", 12), bg="#4CAF50", fg="white",
                            padx=40, pady=10, command=self.show_upload_screen)
        yes_btn.pack(side=tk.LEFT, padx=10)

        no_btn = tk.Button(button_frame, text="Exit",
                           font=("Arial", 12), bg="#f44336", fg="white",
                           padx=40, pady=10, command=self.quit_program)
        no_btn.pack(side=tk.LEFT, padx=10)

    # --- Screen 3: File Upload and Loading ---
    def show_upload_screen(self):
        self.clear_screen()

        # Use file dialog to select and load the file immediately
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Select Question Bank File"
        )

        if not file_path:
            # User cancelled, go back to ask screen
            self.show_ask_create_screen()
            return

        num_loaded = self.load_question_bank(file_path)

        if num_loaded > 0:
            messagebox.showinfo("Success", f"Loaded {num_loaded} questions from the bank!")
            self.show_details_screen(file_path)
        else:
            messagebox.showerror("Error", "Failed to load any questions. Check file format (Q/A on alternating lines).")
            self.show_ask_create_screen()

    def load_question_bank(self, file_path):
        """Loads questions based on the V1.0 alternating line format."""
        self.question_bank = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    question = lines[i].strip()
                    answer = lines[i + 1].strip()
                    if question and answer:
                        self.question_bank.append({
                            'question': question,
                            'answer': answer
                        })
        except FileNotFoundError:
            # Should be rare since it came from filedialog
            return 0
        except Exception:
            # Handles encoding or parsing errors
            return 0

        return len(self.question_bank)

    # --- Screen 4: Exam Details Input ---
    def show_details_screen(self, file_path):
        self.clear_screen()
        self.file_name = os.path.basename(file_path)

        tk.Label(self.root, text=f"Bank loaded from: {self.file_name}",
                 font=("Arial", 12), bg="#e3f2fd", fg="#1565c0").pack(pady=10)

        tk.Label(self.root, text=f"Total questions available: {len(self.question_bank)}",
                 font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.root, text="Enter number of questions for the exam:",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=15)

        self.num_entry = tk.Entry(self.root, font=("Arial", 14), width=10)
        self.num_entry.pack(pady=5)

        tk.Label(self.root, text="Enter output filename (e.g., Exam1.txt):",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=15)

        self.output_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.output_entry.insert(0, "Generated_Exam.txt")
        self.output_entry.pack(pady=5)

        generate_btn = tk.Button(self.root, text="Generate Exam",
                                 font=("Arial", 12), bg="#4CAF50", fg="white",
                                 padx=30, pady=10, command=self.generate_exam)
        generate_btn.pack(pady=30)

    def generate_exam(self):
        try:
            num_questions = int(self.num_entry.get())
            output_file = self.output_entry.get().strip()

            if num_questions <= 0 or num_questions > len(self.question_bank):
                messagebox.showerror("Error", f"Invalid number. Must be between 1 and {len(self.question_bank)}.")
                return

            if not output_file:
                messagebox.showerror("Error", "Please enter a valid output file name.")
                return

            # Core V1.0 randomization logic integrated
            selected = random.sample(self.question_bank, num_questions)

            exam_content = f"EXAM - Created by Professor {self.professor_name}\n"
            exam_content += "=" * 60 + "\n\n"
            for i, pair in enumerate(selected, 1):
                exam_content += f"Question {i}: {pair['question']}\n"
                exam_content += f"Answer: ______________________\n\n"  # Student copy (no answer)

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(exam_content)

            self.show_success_screen(output_file)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the number of questions.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # --- Screen 5: Success Message ---
    def show_success_screen(self, output_file):
        self.clear_screen()

        success_frame = tk.Frame(self.root, bg="#e8f5e9", bd=2, relief=tk.SOLID)
        success_frame.pack(pady=50, padx=30, fill=tk.BOTH, expand=True)

        tk.Label(success_frame, text="✅ Exam Successfully Generated!",
                 font=("Arial", 18, "bold"), bg="#e8f5e9", fg="#2e7d32").pack(pady=30)

        tk.Label(success_frame, text=f"File saved as: {output_file}",
                 font=("Arial", 14), bg="#e8f5e9", fg="#2e7d32").pack(pady=10)

        # Back to start button
        tk.Button(success_frame, text="Generate Another Exam",
                  font=("Arial", 12), bg="#03a9f4", fg="white",
                  padx=30, pady=10, command=self.show_welcome_screen).pack(pady=20)

    # --- Utility: Exit Program ---
    def quit_program(self):
        self.root.destroy()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessorAssistant(root)
    root.mainloop()