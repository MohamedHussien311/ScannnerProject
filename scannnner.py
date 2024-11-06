import tkinter as tk
from tkinter import scrolledtext
import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class LexicalAnalyzer:
    def __init__(self, input_text):
        self.input = input_text
        self.current_char = input_text[0]
        self.position = 0 

    def advance(self):
        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None

    def is_whitespace(self, char):
        return re.match(r'\s', char)

    def is_letter(self, char):
        return re.match(r'[a-zA-Z]', char)

    def is_digit(self, char):
        return re.match(r'\d', char)

    def is_operator(self, char):
        operators = ['+', '-', '=', '<', '>', '!', '==', '!=', '<=', '>=']
        return char in operators

    def get_next_token(self):
        while self.current_char is not None:
            if self.is_whitespace(self.current_char):
                self.advance()
                continue

            elif self.is_letter(self.current_char):
                keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
                            'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'finally',
                            'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'None',
                            'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield']
                letter = ''
                while self.current_char and (self.is_letter(self.current_char) or self.is_digit(self.current_char)):
                    letter += self.current_char
                    self.advance()

                if letter in keywords:
                    return Token('KEYWORD', letter)
                else:
                    return Token('IDENTIFIER', letter)

            elif self.is_digit(self.current_char):
                number = ''
                while self.current_char and self.is_digit(self.current_char):
                    number += self.current_char
                    self.advance()
                return Token('NUMBER', number)
            
            elif self.is_operator(self.current_char):
                operator = self.current_char
                self.advance()
                if operator in ['=', '!', '<', '>'] and self.current_char == '=':
                    operator += self.current_char
                    self.advance()
                return Token('OPERATOR', operator)
            
            else:
                special_char = self.current_char
                self.advance()
                return Token('SPECIAL', special_char)

        return Token('EOF', None)

# Tkinter GUI setup
def analyze():
    input_text = entry.get("1.0", tk.END).strip()
    lexer = LexicalAnalyzer(input_text)

    # Tokenize input
    t_name, t_type = [], []
    token = lexer.get_next_token()
    while token.type != 'EOF':
        t_name.append(token.value)
        t_type.append(token.type)
        output_text.insert(tk.END, f"<Token Type: {token.type}, Value: {token.value}>\n")
        token = lexer.get_next_token()

root = tk.Tk()
root.title("Lexical Analyzer")

# Input text area
entry = scrolledtext.ScrolledText(root, width=60, height=10)
entry.pack(pady=10)

# Button to analyze input
analyze_button = tk.Button(root, text="Analyze", command=analyze)
analyze_button.pack()

# Output text area
output_text = scrolledtext.ScrolledText(root, width=60, height=15)
output_text.pack(pady=10)

root.mainloop()
