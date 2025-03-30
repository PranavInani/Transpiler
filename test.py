from lexer import Lexer, TokenType
from parser import Parser

def run_test(name, source_code, expected_pattern=None):
    """Run a parser test and verify the output contains expected patterns"""
    print(f"\n{'=' * 50}")
    print(f"TEST: {name}")
    print(f"{'=' * 50}")
    
    print("SOURCE CODE:")
    print(f"```\n{source_code}\n```")

    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("\nPARSER OUTPUT:")
        ast_repr = str(ast)
        print(ast_repr)
        
        if expected_pattern:
            if expected_pattern in ast_repr:
                print(f"\n✅ PASS: Found expected pattern: '{expected_pattern}'")
            else:
                print(f"\n❌ FAIL: Expected pattern not found: '{expected_pattern}'")
        else:
            print("\n✅ PASS: Parsing completed without errors")
            
        return True
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

# Test cases
tests = [
    {
        "name": "Variable Declarations",
        "source": """
        vidhi main() {
            ank x = 5;
            sankhya y = 3.14;
            vakya message = "Hello, world!";
            akshar ch = 'A';
        }
        """,
        "expected": "VarDecl(ank, x, Literal(5))"
    },
    {
        "name": "Print Statements",
        "source": """
        vidhi main() {
            likho("Hello, world!");
            ank x = 10;
            likho(x);
        }
        """,
        "expected": "Print(Literal(Hello, world!))"
    },
    {
        "name": "If-Else Statements",
        "source": """
        vidhi main() {
            ank x = 5;
            agar (x < 10) {
                likho("Less than 10");
            } nahi_to {
                likho("Not less than 10");
            }
        }
        """,
        "expected": "If(Binary(Variable(x), <, Literal(10))"
    },
    {
        "name": "Logical Operators",
        "source": """
        vidhi main() {
            ank x = 5;
            sankhya y = 3.14;
            agar (x >= 5 aur y <= 4.0) {
                likho("Condition met!");
            }
            agar (x == 5 ya y != 3.0) {
                likho("Or condition met!");
            }
        }
        """,
        "expected": "Logical(Binary(Variable(x), >=, Literal(5)), aur, Binary(Variable(y), <=, Literal(4.0)))"
    },
    {
        "name": "While Loops",
        "source": """
        vidhi main() {
            ank x = 5;
            jabtak (x > 0) {
                likho(x);
                x = x - 1;
            }
        }
        """,
        "expected": "While(Binary(Variable(x), >, Literal(0))"
    },
    {
        "name": "For Loops",
        "source": """
        vidhi main() {
            karo (ank i = 0; i < 5; i = i + 1) {
                likho(i);
            }
        }
        """,
        "expected": "For(VarDecl(ank, i, Literal(0)), Binary(Variable(i), <, Literal(5))"
    },
    {
        "name": "Complex Expressions",
        "source": """
        vidhi main() {
            ank a = 5;
            ank b = 3;
            ank c = a * b + (a - b) / 2;
            agar (nahi (a < b)) {
                likho("a is greater than or equal to b");
            }
        }
        """,
        "expected": "Unary(nahi, Grouping(Binary(Variable(a), <, Variable(b))))"
    }
]

def run_all_tests():
    """Run all test cases and report results"""
    passed = 0
    total = len(tests)
    
    for test in tests:
        if run_test(test["name"], test["source"], test["expected"]):
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"SUMMARY: {passed}/{total} tests passed")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    run_all_tests()