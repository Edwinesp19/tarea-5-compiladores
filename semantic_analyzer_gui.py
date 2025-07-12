#!/usr/bin/env python3
"""
Interfaz Gráfica para el Analizador Sintáctico
Autor: Edwin Espinal
Descripción: Una interfaz gráfica de usuario para el analizador sintáctico
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
from semantic_analyzer import Lexer, SemanticAnalyzer


class SemanticAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico - Edwin Espinal")
        self.root.geometry("1000x800")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Analizador Sintáctico - Edwin Espinal", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # File operations frame
        file_frame = ttk.LabelFrame(main_frame, text="Operaciones de Archivo", padding="5")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # File path
        ttk.Label(file_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="Explorar", command=self.browse_file).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(file_frame, text="Cargar", command=self.load_file).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(file_frame, text="Guardar", command=self.save_file).grid(row=0, column=4, padx=(0, 5))
        ttk.Button(file_frame, text="Nuevo", command=self.new_file).grid(row=0, column=5)
        
        # Main content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Source code frame
        source_frame = ttk.LabelFrame(content_frame, text="Código Fuente", padding="5")
        source_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        source_frame.columnconfigure(0, weight=1)
        source_frame.rowconfigure(0, weight=1)
        
        # Source code text area
        self.source_text = scrolledtext.ScrolledText(source_frame, wrap=tk.WORD, 
                                                   width=40, height=20,
                                                   font=("Courier", 10))
        self.source_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results frame
        results_frame = ttk.LabelFrame(content_frame, text="Resultados del Análisis", padding="5")
        results_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                    width=40, height=20,
                                                    font=("Courier", 10),
                                                    state=tk.DISABLED)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Analizar", command=self.analyze_code,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Limpiar Resultados", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Código de Ejemplo", command=self.load_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Ayuda", command=self.show_help).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Load example code on startup
        self.load_example()
    
    def browse_file(self):
        """Browse for a file"""
        filename = filedialog.askopenfilename(
            title="Select Source Code File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def load_file(self):
        """Load file content"""
        filename = self.file_path_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            self.source_text.delete(1.0, tk.END)
            self.source_text.insert(1.0, content)
            self.status_var.set(f"Loaded: {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def save_file(self):
        """Save file content"""
        filename = self.file_path_var.get()
        if not filename:
            filename = filedialog.asksaveasfilename(
                title="Save Source Code",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                self.file_path_var.set(filename)
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.source_text.get(1.0, tk.END))
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def new_file(self):
        """Create new file"""
        self.source_text.delete(1.0, tk.END)
        self.file_path_var.set("")
        self.clear_results()
        self.status_var.set("New file created")
    
    def analyze_code(self):
        """Analyze the source code"""
        source_code = self.source_text.get(1.0, tk.END).strip()
        
        if not source_code:
            messagebox.showwarning("Warning", "Please enter some source code to analyze")
            return
        
        self.status_var.set("Analyzing...")
        self.root.update()
        
        try:
            # Tokenize
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            # Analyze
            analyzer = SemanticAnalyzer(tokens)
            errors = analyzer.analyze()
            
            # Generate report
            report = "SEMANTIC ANALYSIS RESULTS\n"
            report += "=" * 60 + "\n\n"
            
            report += f"Total tokens processed: {len(tokens)}\n"
            report += f"Analysis completed.\n\n"
            
            if errors:
                report += f"SEMANTIC ERRORS FOUND ({len(errors)}):\n"
                report += "-" * 40 + "\n"
                for i, error in enumerate(errors, 1):
                    report += f"{i}. {error}\n"
            else:
                report += "✓ NO SEMANTIC ERRORS FOUND!\n"
                report += "The code passed all semantic checks.\n"
            
            report += "\n" + analyzer.get_symbol_table_report()
            
            # Show results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, report)
            self.results_text.config(state=tk.DISABLED)
            
            # Update status
            if errors:
                self.status_var.set(f"Analysis complete - {len(errors)} errors found")
            else:
                self.status_var.set("Analysis complete - No errors found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_var.set("Analysis failed")
    
    def clear_results(self):
        """Clear the results area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Results cleared")
    
    def load_example(self):
        """Load example code"""
        example_code = """// Example code with semantic errors and correct code
var int x = 10;
var float y = 3.14;
var string name = "Edwin";
var bool flag = true;

// Type mismatch error
var int badInt = "not a number";

// Using undefined variable
undefinedVar = 5;

// Correct assignment
x = 20;
y = x;  // int to float conversion (allowed)

// Redeclaring variable in same scope
var int x = 30;  // Error: already declared

// Function declaration
function int add(int a, int b) {
    var int result = a + b;
    return result;
}

// Block with new scope
{
    var int localVar = 100;
    x = localVar;  // OK: can access outer scope
}

// localVar is out of scope here
localVar = 200;  // Error: undefined variable

// Conditional statement
if (x > 10) {
    var string message = "x is greater than 10";
}

// Loop
while (flag) {
    flag = false;
}
"""
        
        self.source_text.delete(1.0, tk.END)
        self.source_text.insert(1.0, example_code)
        self.status_var.set("Example code loaded")
    
    def show_help(self):
        """Show help information"""
        help_text = """Semantic Analyzer Help

SUPPORTED LANGUAGE FEATURES:
• Variable declarations: var type identifier = value;
• Data types: int, float, string, bool
• Assignments: identifier = expression;
• Functions: function returnType name(params) { ... }
• Control flow: if/else, while loops
• Blocks with scope: { ... }

SEMANTIC CHECKS PERFORMED:
• Type checking (assignment compatibility)
• Variable declaration checking
• Scope analysis
• Undefined variable detection
• Redeclaration detection
• Function declaration validation

EXAMPLE SYNTAX:
var int x = 10;
var float y = 3.14;
var string name = "Hello";
var bool flag = true;

x = 20;  // Assignment
y = x;   // int to float (allowed)

function int add(int a, int b) {
    return a + b;
}

HOW TO USE:
1. Enter or load source code
2. Click "Analyze" to perform semantic analysis
3. View results in the right panel
4. Errors will be highlighted with line numbers

Author: Edwin Espinal
Course: Compiladores - UTESA
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x500")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, 
                                                   font=("Courier", 10))
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SemanticAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
