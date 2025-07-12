#!/usr/bin/env python3
"""
Script Lanzador para el Analizador Sintáctico
Autor: Edwin Espinal
Descripción: Proporciona opciones para ejecutar el analizador sintáctico en modo GUI o CLI
"""

import sys
import os
import subprocess
from pathlib import Path


def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("    ANALIZADOR SINTÁCTICO - Edwin Espinal")
    print("    Compiladores - UTESA")
    print("=" * 60)
    print()


def print_help():
    """Print help information"""
    print("USAGE:")
    print("  python run_analyzer.py [options] [file]")
    print()
    print("OPTIONS:")
    print("  -g, --gui          Launch GUI interface (default)")
    print("  -c, --cli <file>   Run CLI analysis on file")
    print("  -t, --test         Run tests on sample files")
    print("  -h, --help         Show this help message")
    print()
    print("EXAMPLES:")
    print("  python run_analyzer.py                    # Launch GUI")
    print("  python run_analyzer.py -g                 # Launch GUI")
    print("  python run_analyzer.py -c test.txt        # Analyze test.txt")
    print("  python run_analyzer.py -t                 # Run tests")
    print()


def run_gui():
    """Launch the GUI version"""
    print("Launching GUI interface...")
    try:
        import tkinter as tk
        from semantic_analyzer_gui import main
        main()
    except ImportError:
        print("Error: tkinter not available. Please install tkinter or use CLI mode.")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)


def run_cli(filename):
    """Run CLI analysis on a file"""
    if not filename:
        print("Error: Please specify a file to analyze")
        sys.exit(1)
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    
    print(f"Analyzing file: {filename}")
    print("-" * 40)
    
    try:
        from semantic_analyzer import main as cli_main
        # Temporarily modify sys.argv to pass the filename
        original_argv = sys.argv
        sys.argv = ['semantic_analyzer.py', filename]
        cli_main()
        sys.argv = original_argv
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


def run_tests():
    """Run tests on sample files"""
    print("Running tests on sample files...")
    print()
    
    test_files = [
        ("test_with_errors.txt", "File with semantic errors"),
        ("test_no_errors.txt", "File without errors")
    ]
    
    for filename, description in test_files:
        if os.path.exists(filename):
            print(f"Testing: {description}")
            print(f"File: {filename}")
            print("-" * 50)
            
            try:
                from semantic_analyzer import Lexer, SemanticAnalyzer
                
                with open(filename, 'r') as f:
                    source_code = f.read()
                
                # Tokenize
                lexer = Lexer(source_code)
                tokens = lexer.tokenize()
                
                # Analyze
                analyzer = SemanticAnalyzer(tokens)
                errors = analyzer.analyze()
                
                print(f"Tokens processed: {len(tokens)}")
                
                if errors:
                    print(f"Errors found: {len(errors)}")
                    for i, error in enumerate(errors[:5], 1):  # Show first 5 errors
                        print(f"  {i}. {error}")
                    if len(errors) > 5:
                        print(f"  ... and {len(errors) - 5} more errors")
                else:
                    print("✓ No semantic errors found!")
                
                print()
                
            except Exception as e:
                print(f"Error testing {filename}: {e}")
                print()
        else:
            print(f"Warning: Test file '{filename}' not found")
            print()


def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import tkinter
        gui_available = True
    except ImportError:
        gui_available = False
    
    return gui_available


def main():
    """Main launcher function"""
    print_banner()
    
    gui_available = check_dependencies()
    
    if not gui_available:
        print("Note: GUI interface not available (tkinter not found)")
        print("Only CLI mode is available.")
        print()
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments, launch GUI by default
        if gui_available:
            run_gui()
        else:
            print("No GUI available. Use -h for help.")
            sys.exit(1)
    
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ['-h', '--help']:
            print_help()
        elif arg in ['-g', '--gui']:
            if gui_available:
                run_gui()
            else:
                print("Error: GUI not available")
                sys.exit(1)
        elif arg in ['-t', '--test']:
            run_tests()
        elif arg.startswith('-'):
            print(f"Error: Unknown option '{arg}'")
            print("Use -h for help")
            sys.exit(1)
        else:
            # Assume it's a filename for CLI analysis
            run_cli(arg)
    
    elif len(sys.argv) == 3:
        option = sys.argv[1]
        filename = sys.argv[2]
        
        if option in ['-c', '--cli']:
            run_cli(filename)
        else:
            print(f"Error: Unknown option '{option}'")
            print("Use -h for help")
            sys.exit(1)
    
    else:
        print("Error: Too many arguments")
        print("Use -h for help")
        sys.exit(1)


if __name__ == "__main__":
    main()
