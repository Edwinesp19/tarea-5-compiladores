#!/bin/bash

# Semantic Analyzer Launcher Script
# Author: Edwin Espinal
# Usage: ./run.sh [options] [file]

echo "============================================================"
echo "    SEMANTIC ANALYZER - Edwin Espinal"
echo "    Compiladores - UTESA"
echo "============================================================"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "semantic_analyzer.py" ]; then
    echo "Error: semantic_analyzer.py not found in current directory"
    echo "Please run this script from the project directory"
    exit 1
fi

# Run the launcher
$PYTHON run_analyzer.py "$@"
