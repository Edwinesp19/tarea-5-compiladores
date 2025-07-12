# Analizador Sintáctico - Edwin Espinal

Un analizador sintáctico integral para un lenguaje de programación simple, desarrollado como parte del curso de Compiladores en UTESA.

## Features

- **Lexical Analysis**: Tokenizes source code into meaningful tokens
- **Semantic Analysis**: Performs comprehensive semantic checks including:
  - Type checking and compatibility
  - Variable declaration and scope analysis
  - Undefined variable detection
  - Redeclaration detection
  - Function declaration validation
- **Symbol Table Management**: Maintains symbol tables with scope tracking
- **Error Reporting**: Detailed error messages with line and column information
- **GUI Interface**: User-friendly graphical interface
- **Command Line Interface**: Terminal-based execution option

## Supported Language Features

### Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - String literals
- `bool` - Boolean values (true/false)

### Syntax Examples

```javascript
// Variable declarations
var int x = 10;
var float y = 3.14;
var string name = "Edwin";
var bool flag = true;

// Assignments
x = 20;
y = x;  // int to float conversion (allowed)

// Functions
function int add(int a, int b) {
    var int result = a + b;
    return result;
}

// Control flow
if (x > 10) {
    var string message = "x is greater than 10";
}

while (flag) {
    flag = false;
}

// Blocks with scope
{
    var int localVar = 100;
}
```

## Semantic Checks Performed

1. **Type Checking**
   - Verifies assignment compatibility
   - Allows safe type conversions (int to float)
   - Detects type mismatches

2. **Variable Analysis**
   - Checks variable declarations
   - Detects undefined variables
   - Prevents redeclaration in same scope

3. **Scope Management**
   - Tracks variable scope across blocks
   - Manages nested scopes properly
   - Validates variable accessibility

4. **Function Validation**
   - Validates function declarations
   - Checks return types
   - Prevents function redeclaration

## Installation and Usage

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Running the GUI Version
```bash
python semantic_analyzer_gui.py
```

### Running the Command Line Version
```bash
python semantic_analyzer.py <source_file>
```

Example:
```bash
python semantic_analyzer.py test_with_errors.txt
```

### Using the Launcher Script
```bash
python run_analyzer.py
```

## Files Structure

```
analizador-semantico-edwin/
├── semantic_analyzer.py      # Core analyzer implementation
├── semantic_analyzer_gui.py  # GUI interface
├── run_analyzer.py          # Launcher script
├── test_with_errors.txt     # Test file with semantic errors
├── test_no_errors.txt       # Test file without errors
└── README.md                # This file
```

## GUI Interface Usage

1. **Source Code Panel**: Enter or load source code
2. **File Operations**: Browse, Load, Save, and create New files
3. **Analysis Results**: View detailed analysis results
4. **Controls**:
   - **Analyze**: Perform semantic analysis
   - **Clear Results**: Clear the results panel
   - **Example Code**: Load example code
   - **Help**: Show help information

## Example Output

### With Errors
```
SEMANTIC ANALYSIS RESULTS
============================================================

Total tokens processed: 45
Analysis completed.

SEMANTIC ERRORS FOUND (4):
----------------------------------------
1. Error at line 7, column 13: Type mismatch: cannot assign string to int
2. Error at line 10, column 1: Undefined variable 'undefinedVar'
3. Error at line 17, column 5: Variable 'x' already declared in current scope
4. Error at line 31, column 1: Undefined variable 'localVar'

Symbol Table Report:
==================================================
Name: x
  Type: int
  Line: 2, Column: 5
  Initialized: True
------------------------------
Name: y
  Type: float
  Line: 3, Column: 7
  Initialized: True
------------------------------
```

### Without Errors
```
SEMANTIC ANALYSIS RESULTS
============================================================

Total tokens processed: 89
Analysis completed.

✓ NO SEMANTIC ERRORS FOUND!
The code passed all semantic checks.
```

## Technical Implementation

### Architecture
- **Lexer**: Tokenizes source code using finite automata
- **Parser**: Recursive descent parser for syntax analysis
- **Semantic Analyzer**: Multi-pass semantic analysis
- **Symbol Table**: Stack-based scope management
- **Error Handler**: Comprehensive error reporting

### Key Classes
- `Token`: Represents lexical tokens
- `Lexer`: Performs lexical analysis
- `Symbol`: Represents symbols in the symbol table
- `SymbolTable`: Manages scopes and symbol lookup
- `SemanticAnalyzer`: Main analysis engine
- `SemanticError`: Error representation

## Testing

The analyzer includes comprehensive test cases:

1. **test_with_errors.txt**: Contains various semantic errors
2. **test_no_errors.txt**: Valid code without errors

### Running Tests
```bash
# Test file with errors
python semantic_analyzer.py test_with_errors.txt

# Test file without errors
python semantic_analyzer.py test_no_errors.txt
```

## Error Types Detected

1. **Type Mismatch**: Incompatible type assignments
2. **Undefined Variables**: Using variables before declaration
3. **Redeclaration**: Declaring variables multiple times in same scope
4. **Scope Violations**: Accessing variables outside their scope
5. **Function Errors**: Invalid function declarations

## Author

**Edwin Espinal**
- Course: Compiladores
- Institution: UTESA
- Year: 2024

## License

This project is developed for educational purposes as part of the Compiladores course at UTESA.
