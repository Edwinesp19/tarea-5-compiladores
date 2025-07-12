#!/usr/bin/env python3
"""
Analizador Sintáctico - Edwin Espinal
Autor: Edwin Espinal
Descripción: Un analizador sintáctico que realiza verificación de tipos, análisis de alcance,
y verificación de declaración de variables para un lenguaje de programación simple.
"""

import re
import sys
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


class TokenType(Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    INT = "int"
    FLOAT_TYPE = "float"
    STRING_TYPE = "string"
    BOOL = "bool"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    FUNCTION = "function"
    RETURN = "return"
    VAR = "var"
    TRUE = "true"
    FALSE = "false"
    
    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # Delimiters
    SEMICOLON = ";"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    
    # Special
    EOF = "EOF"
    NEWLINE = "NEWLINE"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


class DataType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
    VOID = "void"
    UNKNOWN = "unknown"


@dataclass
class Symbol:
    name: str
    data_type: DataType
    line: int
    column: int
    is_function: bool = False
    parameters: List[Tuple[str, DataType]] = None
    return_type: DataType = DataType.VOID
    is_initialized: bool = False


class SemanticError:
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Error at line {self.line}, column {self.column}: {self.message}"


class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Stack of scopes
        self.current_scope = 0
    
    def enter_scope(self):
        """Enter a new scope"""
        self.scopes.append({})
        self.current_scope += 1
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def declare_symbol(self, symbol: Symbol) -> bool:
        """Declare a symbol in current scope"""
        current_scope_dict = self.scopes[self.current_scope]
        if symbol.name in current_scope_dict:
            return False  # Already declared in current scope
        current_scope_dict[symbol.name] = symbol
        return True
    
    def lookup_symbol(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in all scopes (from current to global)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def get_current_scope_symbols(self) -> Dict[str, Symbol]:
        """Get symbols in current scope"""
        return self.scopes[self.current_scope]


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT_TYPE,
            'string': TokenType.STRING_TYPE,
            'bool': TokenType.BOOL,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'function': TokenType.FUNCTION,
            'return': TokenType.RETURN,
            'var': TokenType.VAR,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    def peek_char(self) -> Optional[str]:
        peek_pos = self.position + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self):
        if self.position < len(self.text) and self.text[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        start_line, start_column = self.line, self.column
        num_str = ''
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break  # Second dot, stop
                is_float = True
            num_str += self.current_char()
            self.advance()
        
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, num_str, start_line, start_column)
    
    def read_string(self) -> Token:
        start_line, start_column = self.line, self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        string_value = ''
        while self.current_char() and self.current_char() != quote_char:
            string_value += self.current_char()
            self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line, start_column = self.line, self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Single character tokens
            single_char_tokens = {
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
            }
            
            # Two character tokens
            if char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char == '&' and self.peek_char() == '&':
                self.tokens.append(Token(TokenType.AND, '&&', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char == '|' and self.peek_char() == '|':
                self.tokens.append(Token(TokenType.OR, '||', self.line, self.column))
                self.advance()
                self.advance()
                continue
            elif char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, self.line, self.column))
                self.advance()
                continue
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.column))
                self.advance()
                continue
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, '<', self.line, self.column))
                self.advance()
                continue
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, '>', self.line, self.column))
                self.advance()
                continue
            elif char == '!':
                self.tokens.append(Token(TokenType.NOT, '!', self.line, self.column))
                self.advance()
                continue
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            else:
                # Unknown character, skip
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens


class SemanticAnalyzer:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_function_return_type = DataType.VOID
        self.in_function = False
    
    def current_token(self) -> Token:
        if self.position >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.position]
    
    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
    
    def peek_token(self) -> Token:
        if self.position + 1 >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.position + 1]
    
    def add_error(self, message: str, line: int = None, column: int = None):
        if line is None:
            line = self.current_token().line
        if column is None:
            column = self.current_token().column
        self.errors.append(SemanticError(message, line, column))
    
    def token_type_to_data_type(self, token_type: TokenType) -> DataType:
        mapping = {
            TokenType.INT: DataType.INT,
            TokenType.FLOAT_TYPE: DataType.FLOAT,
            TokenType.STRING_TYPE: DataType.STRING,
            TokenType.BOOL: DataType.BOOL,
        }
        return mapping.get(token_type, DataType.UNKNOWN)
    
    def get_expression_type(self, start_pos: int) -> DataType:
        """Simplified expression type inference"""
        saved_pos = self.position
        self.position = start_pos
        
        expr_type = DataType.UNKNOWN
        
        token = self.current_token()
        
        if token.type == TokenType.INTEGER:
            expr_type = DataType.INT
        elif token.type == TokenType.FLOAT:
            expr_type = DataType.FLOAT
        elif token.type == TokenType.STRING:
            expr_type = DataType.STRING
        elif token.type in [TokenType.TRUE, TokenType.FALSE]:
            expr_type = DataType.BOOL
        elif token.type == TokenType.IDENTIFIER:
            symbol = self.symbol_table.lookup_symbol(token.value)
            if symbol:
                expr_type = symbol.data_type
            else:
                self.add_error(f"Undefined variable '{token.value}'", token.line, token.column)
        
        self.position = saved_pos
        return expr_type
    
    def analyze_variable_declaration(self):
        """Analyze variable declaration: var type identifier = expression;"""
        var_token = self.current_token()
        self.advance()  # Skip 'var'
        
        # Get type
        type_token = self.current_token()
        if type_token.type not in [TokenType.INT, TokenType.FLOAT_TYPE, TokenType.STRING_TYPE, TokenType.BOOL]:
            self.add_error(f"Expected type, got '{type_token.value}'")
            return
        
        var_type = self.token_type_to_data_type(type_token.type)
        self.advance()
        
        # Get identifier
        id_token = self.current_token()
        if id_token.type != TokenType.IDENTIFIER:
            self.add_error(f"Expected identifier, got '{id_token.value}'")
            return
        
        var_name = id_token.value
        self.advance()
        
        # Create symbol
        symbol = Symbol(var_name, var_type, id_token.line, id_token.column)
        
        # Check for assignment
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()  # Skip '='
            
            # Get expression type
            expr_start = self.position
            expr_type = self.get_expression_type(expr_start)
            
            # Type compatibility check
            if expr_type != DataType.UNKNOWN and expr_type != var_type:
                # Allow int to float conversion
                if not (var_type == DataType.FLOAT and expr_type == DataType.INT):
                    self.add_error(f"Type mismatch: cannot assign {expr_type.value} to {var_type.value}")
            
            symbol.is_initialized = True
            
            # Skip to semicolon
            while self.current_token().type != TokenType.SEMICOLON and self.current_token().type != TokenType.EOF:
                self.advance()
        
        # Declare symbol
        if not self.symbol_table.declare_symbol(symbol):
            self.add_error(f"Variable '{var_name}' already declared in current scope")
    
    def analyze_assignment(self):
        """Analyze assignment: identifier = expression;"""
        id_token = self.current_token()
        var_name = id_token.value
        
        # Look up variable
        symbol = self.symbol_table.lookup_symbol(var_name)
        if not symbol:
            self.add_error(f"Undefined variable '{var_name}'")
            return
        
        self.advance()  # Skip identifier
        self.advance()  # Skip '='
        
        # Get expression type
        expr_start = self.position
        expr_type = self.get_expression_type(expr_start)
        
        # Type compatibility check
        if expr_type != DataType.UNKNOWN and expr_type != symbol.data_type:
            # Allow int to float conversion
            if not (symbol.data_type == DataType.FLOAT and expr_type == DataType.INT):
                self.add_error(f"Type mismatch: cannot assign {expr_type.value} to {symbol.data_type.value}")
        
        # Mark as initialized
        symbol.is_initialized = True
        
        # Skip to semicolon
        while self.current_token().type != TokenType.SEMICOLON and self.current_token().type != TokenType.EOF:
            self.advance()
    
    def analyze_function_declaration(self):
        """Analyze function declaration"""
        self.advance()  # Skip 'function'
        
        # Get return type
        return_type_token = self.current_token()
        if return_type_token.type not in [TokenType.INT, TokenType.FLOAT_TYPE, TokenType.STRING_TYPE, TokenType.BOOL]:
            self.add_error(f"Expected return type, got '{return_type_token.value}'")
            return
        
        return_type = self.token_type_to_data_type(return_type_token.type)
        self.advance()
        
        # Get function name
        name_token = self.current_token()
        if name_token.type != TokenType.IDENTIFIER:
            self.add_error(f"Expected function name, got '{name_token.value}'")
            return
        
        func_name = name_token.value
        self.advance()
        
        # Create function symbol
        func_symbol = Symbol(func_name, return_type, name_token.line, name_token.column, 
                           is_function=True, return_type=return_type, parameters=[])
        
        # Declare function
        if not self.symbol_table.declare_symbol(func_symbol):
            self.add_error(f"Function '{func_name}' already declared")
        
        # Enter function scope
        self.symbol_table.enter_scope()
        self.in_function = True
        self.current_function_return_type = return_type
        
        # Skip parameter list and function body for now
        paren_count = 0
        brace_count = 0
        
        while self.current_token().type != TokenType.EOF:
            token = self.current_token()
            
            if token.type == TokenType.LPAREN:
                paren_count += 1
            elif token.type == TokenType.RPAREN:
                paren_count -= 1
            elif token.type == TokenType.LBRACE:
                brace_count += 1
            elif token.type == TokenType.RBRACE:
                brace_count -= 1
                if brace_count == 0:
                    break
            
            self.advance()
        
        # Exit function scope
        self.symbol_table.exit_scope()
        self.in_function = False
        self.current_function_return_type = DataType.VOID
    
    def analyze_statement(self):
        """Analyze a single statement"""
        token = self.current_token()
        
        if token.type == TokenType.VAR:
            self.analyze_variable_declaration()
        elif token.type == TokenType.FUNCTION:
            self.analyze_function_declaration()
        elif token.type == TokenType.IDENTIFIER:
            # Check if it's an assignment
            if self.peek_token().type == TokenType.ASSIGN:
                self.analyze_assignment()
            else:
                # Skip expression statement
                while self.current_token().type != TokenType.SEMICOLON and self.current_token().type != TokenType.EOF:
                    self.advance()
        elif token.type == TokenType.IF:
            self.analyze_if_statement()
        elif token.type == TokenType.WHILE:
            self.analyze_while_statement()
        elif token.type == TokenType.LBRACE:
            self.analyze_block()
        else:
            # Skip unknown statements
            while self.current_token().type not in [TokenType.SEMICOLON, TokenType.EOF, TokenType.RBRACE, TokenType.NEWLINE]:
                self.advance()
            # Make sure we advance past the current token if it's not EOF
            if self.current_token().type != TokenType.EOF:
                self.advance()
    
    def analyze_if_statement(self):
        """Analyze if statement"""
        self.advance()  # Skip 'if'
        
        # Skip condition
        if self.current_token().type == TokenType.LPAREN:
            paren_count = 1
            self.advance()
            while paren_count > 0 and self.current_token().type != TokenType.EOF:
                if self.current_token().type == TokenType.LPAREN:
                    paren_count += 1
                elif self.current_token().type == TokenType.RPAREN:
                    paren_count -= 1
                self.advance()
        
        # Analyze then block
        if self.current_token().type == TokenType.LBRACE:
            self.analyze_block()
        else:
            self.analyze_statement()
        
        # Check for else
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            if self.current_token().type == TokenType.LBRACE:
                self.analyze_block()
            else:
                self.analyze_statement()
    
    def analyze_while_statement(self):
        """Analyze while statement"""
        self.advance()  # Skip 'while'
        
        # Skip condition
        if self.current_token().type == TokenType.LPAREN:
            paren_count = 1
            self.advance()
            while paren_count > 0 and self.current_token().type != TokenType.EOF:
                if self.current_token().type == TokenType.LPAREN:
                    paren_count += 1
                elif self.current_token().type == TokenType.RPAREN:
                    paren_count -= 1
                self.advance()
        
        # Analyze body
        if self.current_token().type == TokenType.LBRACE:
            self.analyze_block()
        else:
            self.analyze_statement()
    
    def analyze_block(self):
        """Analyze block statement"""
        self.advance()  # Skip '{'
        self.symbol_table.enter_scope()
        
        while self.current_token().type != TokenType.RBRACE and self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            self.analyze_statement()
            if self.current_token().type == TokenType.SEMICOLON:
                self.advance()
        
        if self.current_token().type == TokenType.RBRACE:
            self.advance()
        
        self.symbol_table.exit_scope()
    
    def analyze(self) -> List[SemanticError]:
        """Main analysis method"""
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
                continue
            
            # Store current position to detect infinite loops
            old_position = self.position
            
            self.analyze_statement()
            
            if self.current_token().type == TokenType.SEMICOLON:
                self.advance()
            
            # If position didn't change, force advance to prevent infinite loop
            if self.position == old_position and self.current_token().type != TokenType.EOF:
                self.advance()
        
        return self.errors
    
    def get_symbol_table_report(self) -> str:
        """Generate symbol table report"""
        report = "Reporte de Tabla de Símbolos:\n"
        report += "=" * 50 + "\n"
        
        symbols = self.symbol_table.get_current_scope_symbols()
        if not symbols:
            report += "No se encontraron símbolos en el alcance global.\n"
        else:
            for name, symbol in symbols.items():
                report += f"Nombre: {name}\n"
                report += f"  Tipo: {symbol.data_type.value}\n"
                report += f"  Línea: {symbol.line}, Columna: {symbol.column}\n"
                report += f"  Inicializado: {'Sí' if symbol.is_initialized else 'No'}\n"
                if symbol.is_function:
                    report += f"  Función: Sí\n"
                    report += f"  Tipo de Retorno: {symbol.return_type.value}\n"
                report += "-" * 30 + "\n"
        
        return report


def main():
    """Main function to run the semantic analyzer"""
    if len(sys.argv) != 2:
        print("Usage: python semantic_analyzer.py <source_file>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    try:
        with open(source_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Tokenize
    print("Tokenizando...")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    
    print(f"Se encontraron {len(tokens)} tokens")
    
    # Analyze
    print("\nRealizando análisis sintáctico...")
    analyzer = SemanticAnalyzer(tokens)
    errors = analyzer.analyze()
    
    # Report results
    print("\n" + "=" * 60)
    print("ANALIZADOR SINTÁCTICO - EDWIN ESPINAL")
    print("RESULTADOS DEL ANÁLISIS SINTÁCTICO")
    print("=" * 60)
    
    if errors:
        print(f"\nSe encontraron {len(errors)} errores sintácticos:")
        print("-" * 40)
        for error in errors:
            print(f"  {error}")
    else:
        print("\n¡No se encontraron errores sintácticos!")
    
    # Print symbol table
    print("\n" + analyzer.get_symbol_table_report())
    
    # Exit with appropriate code
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
