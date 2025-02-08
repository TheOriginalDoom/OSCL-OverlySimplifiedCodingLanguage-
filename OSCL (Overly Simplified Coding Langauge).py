import re
import tkinter as tk
from tkinter import scrolledtext

TOKEN_TYPES = {
    "NUMBER": r"\d+",
    "STRING": r'"[^"]*"',
    "IDENTIFIER": r"[a-zA-Z_]+",
    "ASSIGN": r"=",
}

def tokenize(code):
    tokens = []
    code = code.strip()
    while code:
        match = None
        for type_, pattern in TOKEN_TYPES.items():
            regex = re.match(pattern, code)
            if regex:
                match = regex.group(0)
                tokens.append((type_, match))
                code = code[len(match):].strip()
                break
        if not match:
            raise SyntaxError(f"Unexpected claw machine token, you should reset character NOW!!!: {code[0]}")
    return tokens

variables = {}

def parse(tokens):
    if not tokens:
        return None

    command = tokens[0][1]

    if command == "print":
        value = tokens[1][1].strip('"')
        return ("print", value)

    elif command in ("add", "mul", "sub", "div"):
        val1 = resolve_value(tokens[1][1])
        val2 = resolve_value(tokens[2][1])
        if isinstance(val1, int) and isinstance(val2, int):
            return (command, val1, val2)

    elif command == "let":
        if tokens[1][0] == "IDENTIFIER" and tokens[2][0] == "ASSIGN":
            value = resolve_value(tokens[3][1])
            return ("let", tokens[1][1], value)

    elif command == "repeat":
        repeat_count = resolve_value(tokens[1][1])
        if isinstance(repeat_count, int) and repeat_count > 0:
            return ("repeat", repeat_count, tokens[2:])

    raise SyntaxError(f"What the syntax??? You suck so bad u have bad syntax: {tokens}")

def resolve_value(value):
    if value.isdigit():
        return int(value)
    elif value in variables:
        return variables[value]
    return value

def interpret(ast):
    if ast is None:
        return ""

    command = ast[0]

    if command == "print":
        return str(variables.get(ast[1], ast[1]))

    elif command == "add":
        return str(ast[1] + ast[2])

    elif command == "mul":
        return str(ast[1] * ast[2])

    elif command == "sub":
        return str(ast[1] - ast[2])

    elif command == "div":
        return str(ast[1] / ast[2])

    elif command == "let":
        variables[ast[1]] = ast[2]
        return f"{ast[1]} = {ast[2]}"

    elif command == "repeat":
        output = []
        for _ in range(ast[1]):
            output.append(interpret(parse(ast[2])))
        return "\n".join(output)

    return "Unknown command."

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("O.S.C.L (Overly Simplified Coding Language) Code Editor")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Comic Sans MS", 12))
        self.text_area.pack(pady=10, padx=10)

        self.run_button = tk.Button(root, text="Run", command=self.run_code, font=("Comic Sans MS", 12))
        self.run_button.pack(pady=5)

        self.text_area.bind("<Control-Return>", self.run_code)

        self.output_window = OutputWindow()

    def run_code(self, event=None):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            return

        results = []
        for line in code.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.lower() in ["exit", "quit"]:
                self.root.quit()

            try:
                tokens = tokenize(line)
                ast = parse(tokens)
                result = interpret(ast)
                results.append(f">> {line}\n{result}")
            except Exception as e:
                results.append(f"Imagine having errors, -10000 aura frfr: {e}")

        self.output_window.display_output("\n".join(results))

class OutputWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("O.S.C.L (Overly Simplified Coding Language) Output Window")

        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=60, height=20, font=("Comic Sans MS", 12))
        self.text_area.pack(pady=10)
        self.text_area.config(state=tk.DISABLED)

    def display_output(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()
