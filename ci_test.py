from test import run_test, run_generator_test, tests, code_gen_tests
import sys
import xml.etree.ElementTree as ET
import datetime

def run_all_tests_with_junit():
    """Run all test cases and generate JUnit XML report"""
    # Initialize test counters
    passed = 0
    total = len(tests)
    
    syntax_passed = 0
    semantic_passed = 0
    semantic_total = sum(1 for test in tests if "expect_semantic_errors" in test)
    
    # Create JUnit XML structure
    test_suite = ET.Element("testsuite")
    test_suite.set("name", "Transpiler Tests")
    test_suite.set("timestamp", datetime.datetime.now().isoformat())
    
    # Run syntax and semantic tests
    for test in tests:
        test_case = ET.SubElement(test_suite, "testcase")
        test_case.set("name", test["name"])
        test_case.set("classname", "BasicTests")
        
        start_time = datetime.datetime.now()
        result = run_test(test["name"], test["source"], test["expected"], 
                         test.get("expect_semantic_errors"))
        end_time = datetime.datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        test_case.set("time", str(duration))
        
        if result:
            passed += 1
            if "expect_semantic_errors" in test:
                semantic_passed += 1
            else:
                syntax_passed += 1
        else:
            # Add failure element for failed tests
            failure = ET.SubElement(test_case, "failure")
            failure.set("message", f"Test {test['name']} failed")
    
    # Run code generation tests
    gen_passed = 0
    gen_total = len(code_gen_tests)
    
    for test in code_gen_tests:
        test_case = ET.SubElement(test_suite, "testcase")
        test_case.set("name", test["name"])
        test_case.set("classname", "CodeGenTests")
        
        start_time = datetime.datetime.now()
        result = run_generator_test(
            test["name"], 
            test["source"], 
            test.get("expected_output")
        )
        end_time = datetime.datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        test_case.set("time", str(duration))
        
        if result:
            gen_passed += 1
        else:
            # Add failure element for failed tests
            failure = ET.SubElement(test_case, "failure")
            failure.set("message", f"Code generation test {test['name']} failed")
    
    # Update test counts in XML
    test_suite.set("tests", str(total + gen_total))
    test_suite.set("failures", str((total - passed) + (gen_total - gen_passed)))
    
    # Print summary to console
    print(f"\n{'=' * 50}")
    print(f"BASIC TESTS SUMMARY: {passed}/{total} tests passed")
    print(f"  - Syntax:    {syntax_passed}/{total-semantic_total} tests passed")
    print(f"  - Semantics: {semantic_passed}/{semantic_total} tests passed")
    
    print(f"\n{'=' * 50}")
    print(f"CODE GENERATION SUMMARY: {gen_passed}/{gen_total} tests passed")
    
    print(f"\n{'=' * 50}")
    print(f"OVERALL SUMMARY: {passed + gen_passed}/{total + gen_total} tests passed")
    print(f"{'=' * 50}")
    
    # Write XML to file
    tree = ET.ElementTree(test_suite)
    tree.write("test-results.xml", encoding="utf-8", xml_declaration=True)
    
    # Return overall success/failure
    return (passed + gen_passed) == (total + gen_total)

if __name__ == "__main__":
    success = run_all_tests_with_junit()
    sys.exit(0 if success else 1)