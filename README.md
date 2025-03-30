# Hinglish to C Transpiler

This project implements a transpiler that converts code written in "Hinglish" (a simple programming language with Hindi-English syntax) to C code. The transpiler supports a variety of programming constructs and provides a complete pipeline from lexical analysis to code generation.

## Overview

The transpiler follows a traditional compiler pipeline:

1. **Lexical Analysis**: Tokenizes the source code
2. **Parsing**: Converts tokens into an Abstract Syntax Tree (AST)
3. **Semantic Analysis**: Checks for semantic errors and builds a symbol table
4. **Code Generation**: Translates the AST into C code

## Language Features

The Hinglish programming language supports:

- Variable declarations (`ank` for integers, `sankhya` for floats, `vakya` for strings, `akshar` for characters)
- Function declarations with parameters and return types
- Control flow statements (`agar`/`nahi_to` for if-else, `jabtak` for while loops, `karo` for for loops)
- Arithmetic and logical expressions
- Print statements (`likho`)
- Nested blocks and scoping

## Example

