# Guía de Inicio Rápido - Analizador Sintáctico

## Edwin Espinal - Compiladores UTESA

### Quick Run Options

#### 1. Direct Command Line Usage
```bash
python3 semantic_analyzer.py test_with_errors.txt
```

#### 2. Using the Launcher (Recommended)
```bash
python3 run_analyzer.py -c test_with_errors.txt
```

#### 3. GUI Interface (if tkinter available)
```bash
python3 semantic_analyzer_gui.py
```

#### 4. Shell Script
```bash
./run.sh -c test_with_errors.txt
```

### Test Files Included

1. **test_with_errors.txt** - Contains 6 semantic errors for testing
2. **test_no_errors.txt** - Clean code without semantic errors

### Quick Test Commands

```bash
# Run all tests
python3 run_analyzer.py -t

# Test file with errors
python3 run_analyzer.py -c test_with_errors.txt

# Test clean file
python3 run_analyzer.py -c test_no_errors.txt

# Show help
python3 run_analyzer.py -h
```

### Expected Output for test_with_errors.txt

```
Found 6 semantic errors:
1. Error at line 8, column 18: Type mismatch: cannot assign string to int
2. Error at line 11, column 1: Undefined variable 'undefinedVar'
3. Error at line 18, column 15: Variable 'x' already declared in current scope
4. Error at line 33, column 1: Undefined variable 'localVar'
5. Error at line 46, column 8: Type mismatch: cannot assign int to string
6. Error at line 49, column 1: Undefined variable 'result'
```

### Expected Output for test_no_errors.txt

```
No semantic errors found!
```

### Project Structure

```
analizador-semantico-edwin/
├── semantic_analyzer.py      # Core analyzer (CLI executable)
├── semantic_analyzer_gui.py  # GUI version
├── run_analyzer.py          # Unified launcher
├── run.sh                   # Shell script launcher
├── test_with_errors.txt     # Test file with errors
├── test_no_errors.txt       # Test file without errors
├── README.md                # Full documentation
└── QUICKSTART.md           # This file
```

### Minimum Requirements

- Python 3.6+
- No external dependencies for CLI version
- tkinter for GUI version (usually included with Python)

### Features Implemented

✅ **Lexical Analysis** - Full tokenization  
✅ **Semantic Analysis** - Type checking, scope analysis  
✅ **Symbol Table** - Multi-scope symbol management  
✅ **Error Reporting** - Detailed error messages with line/column  
✅ **GUI Interface** - User-friendly graphical interface  
✅ **CLI Interface** - Command-line execution  
✅ **Test Cases** - Comprehensive test files  
✅ **Documentation** - Full README and quick start guide  

### Author
Edwin Espinal - Compiladores UTESA 2024
