import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import io
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.interpreter import Interpreter

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Code Editor with Output Terminal")
        self.create_menu()
        self.create_switch_frame()
        self.create_main_frames()
        self.create_widgets()
        self.bind_keys()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code, accelerator="F5")
        menu_bar.add_cascade(label="Run", menu=run_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_switch_frame(self):
        self.switch_frame = tk.Frame(self.root)
        self.switch_frame.pack(fill=tk.X)

        # Create a label for the switch selection
        switch_label = tk.Label(self.switch_frame, text="Select switch:")
        switch_label.pack(side=tk.LEFT, padx=5)

        # Create a variable and radio buttons for selecting the switch
        self.switch_var = tk.StringVar(value="None")
        self.create_switch_buttons()

    def create_switch_buttons(self):
        radio_none = tk.Radiobutton(self.switch_frame, text="None", variable=self.switch_var, value="None")
        radio_none.pack(side=tk.LEFT, padx=5)

        radio_ast = tk.Radiobutton(self.switch_frame, text="AST", variable=self.switch_var, value="AST")
        radio_ast.pack(side=tk.LEFT, padx=5)

        radio_st = tk.Radiobutton(self.switch_frame, text="ST", variable=self.switch_var, value="ST")
        radio_st.pack(side=tk.LEFT, padx=5)

    def create_main_frames(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the code editor on the left
        self.code_frame = tk.Frame(self.main_frame)
        self.code_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame for the output terminal on the right
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Create a scrolled text widget for the code editor
        self.code_editor = scrolledtext.ScrolledText(self.code_frame, wrap=tk.WORD, undo=True)
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Create a scrolled text widget for the output terminal
        self.output_terminal = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, undo=False)
        self.output_terminal.pack(fill=tk.BOTH, expand=True)
        self.output_terminal.config(state=tk.DISABLED)  # Initially disable the output terminal

        # Create a button to run the code at the bottom
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_keys(self):
        # Bind F5 key to run the code
        self.root.bind('<F5>', self.run_code)

    def run_code(self, event=None):
        code = self.code_editor.get("1.0", tk.END).strip()  # Get all code from the editor
        if not code:
            return  # Don't run empty code

        # Determine the selected switch
        switch = None
        if self.switch_var.get() == "AST":
            switch = "-ast"
        elif self.switch_var.get() == "ST":
            switch = "-st"

        # Capture the output of the interpreter
        output_capture = io.StringIO()
        sys.stdout = output_capture

        try:
            # Instantiate and run the custom interpreter
            interpreter = Interpreter(code, switch=switch)
            interpreter.interpret()  # This should print to stdout

            # Get the captured output
            result = output_capture.getvalue()
        except Exception as e:
            result = f"Error: {e}"
        finally:
            sys.stdout = sys.__stdout__  # Reset stdout

        # Display the output in the output terminal
        self.output_terminal.config(state=tk.NORMAL)
        self.output_terminal.delete("1.0", tk.END)
        self.output_terminal.insert(tk.END, result)
        self.output_terminal.config(state=tk.DISABLED)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("RPAL Files", "*.rpal"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert(tk.END, code)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".rpal", filetypes=[("RPAL Files", "*.rpal"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.code_editor.get("1.0", tk.END)
                file.write(code)

    def exit_app(self):
        self.root.quit()

    def show_about(self):
        messagebox.showinfo("About", "Simple Code Editor\nVersion 1.0\nCreated with Tkinter")

def create_gui():
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()
