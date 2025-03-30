import argparse
import os
import sys
import subprocess

# Sample Hinglish programs for testing
SAMPLE_PROGRAMS = {
    "hello": """
# This is a simple Hello World program in Hinglish

vidhi main() {
    vakya msg = "Namaste, duniya!";
    likho(msg);
    wapas 0;
}
""",
    "calculator": """
# A simple calculator in Hinglish

vidhi sum(ank a, ank b) ank {
    wapas a + b;
}

vidhi subtract(ank a, ank b) ank {
    wapas a - b;
}

vidhi multiply(ank a, ank b) ank {
    wapas a * b;
}

vidhi divide(ank a, ank b) sankhya {
    wapas a / b;
}

vidhi main() {
    ank a = 10;
    ank b = 5;
    
    likho("Calculator Demo");
    likho("a = 10, b = 5");
    likho("Sum: ");
    likho(sum(a, b));
    
    likho("Difference: ");
    likho(subtract(a, b));
    
    likho("Product: ");
    likho(multiply(a, b));
    
    likho("Quotient: ");
    likho(divide(a, b));
    
    wapas 0;
}
""",
    "factorial": """
# Recursive factorial in Hinglish

vidhi factorial(ank n) ank {
    agar (n <= 1) {
        wapas 1;
    }
    wapas n * factorial(n - 1);
}

vidhi main() {
    likho("Factorial Calculator");
    
    ank number = 5;
    likho("Factorial of 5 is:");
    likho(factorial(number));
    
    wapas 0;
}
""",
    "loops": """
# Demonstrates loops and conditionals in Hinglish

vidhi main() {
    likho("Loop Demo");
    
    # While loop example
    likho("Counting down from 5:");
    ank count = 5;
    jabtak (count > 0) {
        likho(count);
        count = count - 1;
    }
    
    # For loop example
    likho("Even numbers from 1 to 10:");
    karo (ank i = 1; i <= 10; i = i + 1) {
        agar (i % 2 == 0) {
            likho(i);
        }
    }
    
    # Nested conditionals
    ank x = 15;
    agar (x > 10) {
        likho("x is greater than 10");
        agar (x > 20) {
            likho("x is also greater than 20");
        } nahi_to {
            likho("but x is not greater than 20");
        }
    } nahi_to {
        likho("x is not greater than 10");
    }
    
    wapas 0;
}
""",
    "strings": """
# String manipulation in Hinglish

vidhi main() {
    vakya name = "Bharat";
    akshar first = 'B';
    
    likho("String Demo");
    likho("Country: ");
    likho(name);
    
    likho("First letter: ");
    likho(first);
    
    ank count = 5;
    karo (ank i = 0; i < count; i = i + 1) {
        likho(name);
    }
    
    wapas 0;
}
"""
}

class HinglishToC:
    def __init__(self):
        pass
    
    def parse_source(self, source_code):
        """Parse the Hinglish code into an abstract syntax tree."""
        print("Parsing Hinglish code...")
        from lexer import Lexer
        from parser import Parser
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        return ast
    
    def analyze(self, ast):
        """Apply semantic analysis on the AST."""
        print("Performing semantic analysis...")
        from sem_analyser import SemanticAnalyzer
        
        analyzer = SemanticAnalyzer()
        analysis_result = analyzer.analyze(ast)
        
        if not analysis_result['success']:
            print("Semantic analysis found errors:")
            for error in analysis_result['errors']:
                print(f"  - {error}")
            # Continue anyway for now
        
        return {
            'ast': ast,
            'symbol_table': analysis_result['symbol_table']
        }
    
    def generate_code(self, result):
        """Generate C code from the AST."""
        print("Generating C code...")
        from generator import CodeGenerator
        
        ast = result['ast']
        symbol_table = result['symbol_table']
        
        generator = CodeGenerator(symbol_table)
        c_code = generator.generate(ast)
        return c_code
    
    def transpile(self, source_code):
        """Transpile Hinglish code to C."""
        ast = self.parse_source(source_code)
        result = self.analyze(ast)
        c_code = self.generate_code(result)
        return c_code


def compile_with_gcc(input_file, output_file=None):
    """Compile C code using GCC."""
    if not output_file:
        output_file = os.path.splitext(input_file)[0]
    
    try:
        print(f"Compiling {input_file} with GCC...")
        result = subprocess.run(
            ['gcc', input_file, '-o', output_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Compilation successful. Executable: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e.stderr.decode()}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Transpile Hinglish code to C')
    parser.add_argument('input_file', nargs='?', help='Input file containing Hinglish source code')
    parser.add_argument('--output', help='Output C file path (default: input_name.c or sample_name.c)')
    parser.add_argument('--compile', action='store_true', help='Compile the generated C code')
    parser.add_argument('--exe', help='Output executable name when compiling')
    parser.add_argument('--sample', choices=SAMPLE_PROGRAMS.keys(), 
                       help='Run a built-in sample program instead of reading from a file')
    parser.add_argument('--list-samples', action='store_true', help='List available sample programs')
    
    args = parser.parse_args()
    
    # List available samples if requested
    if args.list_samples:
        print("Available sample programs:")
        for name in SAMPLE_PROGRAMS:
            print(f"  - {name}")
        return 0
    
    # Handle sample program or file input
    if args.sample:
        source_code = SAMPLE_PROGRAMS[args.sample]
        base_name = args.sample
        print(f"Using built-in sample: {args.sample}")
    elif args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                source_code = f.read()
            base_name = os.path.splitext(args.input_file)[0]
        except FileNotFoundError:
            print(f"Error: Could not find input file '{args.input_file}'")
            return 1
    else:
        parser.print_help()
        print("\nError: You must provide either an input file or select a sample program.")
        return 1
    
    try:
        transpiler = HinglishToC()
        c_code = transpiler.transpile(source_code)
        
        output_file = args.output
        if not output_file:
            output_file = f"{base_name}.c"
        
        with open(output_file, 'w') as f:
            f.write(c_code)
        print(f"Generated C code written to {output_file}")
        
        # If compile flag is set, compile the output
        if args.compile:
            compile_with_gcc(output_file, args.exe)
            print("\nTo run the program, use:")
            print(f"  ./{args.exe if args.exe else base_name}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())