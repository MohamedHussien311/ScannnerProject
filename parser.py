import tkinter as tk
from tkinter import simpledialog, messagebox

class TopDownParser:
    def __init__(self):
        self.grammar = {}
        self.start_symbol = None

    def set_grammar(self, root):
        """Allows the user to define the grammar via Tkinter dialogs."""
        self.grammar = {}
        non_terminals = set()

        rule_number = 1  # عداد للقواعد

        while len(self.grammar) < 4:  # Ensure at least 4 rules
            grammar_display = self.display_grammar_with_numbers()
            rule = simpledialog.askstring(
                "Input", 
                f"Current Rules:\n{grammar_display}\n\nEnter rule {rule_number} (or 'done' to finish):", 
                parent=root
            )
            if not rule or rule.lower() == 'done':
                if len(self.grammar) < 4:
                    messagebox.showerror("Error", "Grammar must have at least 4 rules.")
                    continue
                break
            try:
                lhs, rhs = rule.split("->")
                lhs = lhs.strip()
                productions = [p.strip() for p in rhs.split("|")]
                if lhs not in self.grammar:
                    self.grammar[lhs] = []
                self.grammar[lhs].extend(productions)
                non_terminals.add(lhs)
                rule_number += 1  # تحديث رقم القاعدة
            except ValueError:
                messagebox.showerror("Error", "Invalid rule format. Use the format: NonTerminal -> production1 | production2")

        self.start_symbol = simpledialog.askstring("Input", "Enter the start symbol:", parent=root)

    def display_grammar_with_numbers(self):
        """Creates a formatted string representation of the grammar with rule numbers."""
        grammar_display = ""
        rule_number = 1
        for lhs, productions in self.grammar.items():
            grammar_display += f"{rule_number}. {lhs} -> {' | '.join(productions)}\n"
            rule_number += 1
        return grammar_display

    def is_simple_grammar(self):
        """Checks if the grammar is simple (no recursion or left recursion)."""
        for lhs, productions in self.grammar.items():
            for prod in productions:
                if lhs in prod.split():
                    return False, f"Left recursion detected in rule: {lhs} -> {prod}"
        return True, "Grammar is simple."

    def parse(self, sequence):
        """Parses the sequence using the grammar."""
        def recursive_parse(symbols, seq):
            if not symbols and not seq:
                return True
            if not symbols or not seq:
                return False

            current_symbol = symbols[0]
            rest_symbols = symbols[1:]

            if current_symbol in self.grammar:  # Non-terminal
                for production in self.grammar[current_symbol]:
                    if recursive_parse(production.split() + rest_symbols, seq):
                        return True
            else:  # Terminal
                if seq[0] == current_symbol:
                    return recursive_parse(rest_symbols, seq[1:])
            return False

        return recursive_parse([self.start_symbol], list(sequence))

    def display_grammar(self):
        """Creates a formatted string representation of the grammar."""
        grammar_display = "Grammar:\n"
        for lhs, productions in self.grammar.items():
            grammar_display += f"{lhs} -> {' | '.join(productions)}\n"
        grammar_display += f"\nStart Symbol: {self.start_symbol}"
        return grammar_display

    def run(self):
        """Runs the parser using a Tkinter GUI."""
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        while True:
            grammar_info = self.display_grammar() if self.grammar else "Grammar not set."
            choice = simpledialog.askstring(
                "Menu", 
                f"{grammar_info}\n\n1. Set Grammar\n2. Check if Grammar is Simple\n3. Parse a Sequence\n4. Exit\nEnter your choice:", 
                parent=root
            )

            if not choice:
                break

            if choice == '1':
                self.set_grammar(root)
                # Check if the grammar is simple after setting it
                is_simple, message = self.is_simple_grammar()
                while not is_simple:
                    messagebox.showerror("Error", message)
                    self.set_grammar(root)
                    is_simple, message = self.is_simple_grammar()
                messagebox.showinfo("Grammar Check", message)
            elif choice == '2':
                is_simple, message = self.is_simple_grammar()
                messagebox.showinfo("Grammar Check", message)
            elif choice == '3':
                sequence = simpledialog.askstring("Input", "Enter the sequence to parse:", parent=root)
                if sequence:
                    if self.parse(sequence):
                        messagebox.showinfo("Parse Result", "Sequence is Accepted.")
                    else:
                        messagebox.showinfo("Parse Result", "Sequence is Rejected.")
            elif choice == '4':
                break
            else:
                messagebox.showerror("Error", "Invalid choice. Please try again.")

if __name__ == "__main__":
    parser = TopDownParser()
    parser.run()
