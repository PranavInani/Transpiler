from lexer import Lexer
from parser import Parser
from sem_analyser import SemanticAnalyzer

def compile_code(source):
    # Lexical analysis
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print("Lexical analysis completed.")
    
    # Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parsing completed.")
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    success, errors = analyzer.analyze(ast)
    
    if not success:
        print("Semantic analysis failed:")
        for error in errors:
            print(f" - {error}")
        return None
    
    print("Semantic analysis completed successfully.")
    return ast

if __name__ == "__main__":
    source = """
    vidhi factorial(ank n) {
        agar (n <= 1) {
            wapas 1;
        } nahi_to {
            wapas n * factorial(n - 1);
        }
    }
    
    vidhi main() {
        ank result = factorial(5);
        likho(result);
        wapas 0;
    }
    """
    
    compile_code(source)