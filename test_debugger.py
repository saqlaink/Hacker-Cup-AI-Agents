#!/usr/bin/env python3
"""
Test script to demonstrate the Debugger Agent functionality.
"""

import os
import sys
import yaml
from agents import DebuggerAgent
from utils import CodeExecutor

# Sample failing code (off-by-one error)
FAILING_CODE = """import sys

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        # BUG: Should sum from 1 to n, but sums from 0 to n-1
        total = sum(range(n))
        print(total)

if __name__ == "__main__":
    solve()
"""

TEST_INPUT = """3
5
10
1
"""

EXPECTED_OUTPUT = """15
55
1
"""

ACTUAL_OUTPUT = """10
45
0
"""

DIFF = """Expected vs Actual:
Line 1: 15 != 10 (difference: -5)
Line 2: 55 != 45 (difference: -10)
Line 3: 1 != 0 (difference: -1)
"""

def main():
    print("=" * 80)
    print("DEBUGGER AGENT TEST")
    print("=" * 80)
    
    # Load API key from config
    print("\n0. Loading configuration...")
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        google_key = config.get('api_keys', {}).get('google')
        if google_key and google_key != "your-google-api-key-here":
            os.environ['GOOGLE_API_KEY'] = google_key
            print("✓ Google API key loaded from config.yaml")
        else:
            print("✗ No valid Google API key found in config.yaml")
            print("Please set your API key in config.yaml")
            return
    except Exception as e:
        print(f"✗ Failed to load config: {e}")
        return
    
    # Initialize debugger agent
    print("\n1. Initializing Debugger Agent...")
    debugger = DebuggerAgent("google:gemini-2.5-flash")
    print("✓ Debugger Agent initialized")
    
    # Add debug instrumentation
    print("\n2. Adding debug instrumentation to failing code...")
    print("\nOriginal failing code:")
    print("-" * 40)
    print(FAILING_CODE)
    print("-" * 40)
    
    debug_code = debugger.add_debug_instrumentation(
        FAILING_CODE,
        TEST_INPUT,
        EXPECTED_OUTPUT,
        ACTUAL_OUTPUT,
        DIFF
    )
    
    print("\n✓ Debug instrumentation added")
    print("\nDebugged code:")
    print("-" * 40)
    print(debug_code)
    print("-" * 40)
    
    # Save and execute debug version
    print("\n3. Executing debug version...")
    os.makedirs("./test_workspace", exist_ok=True)
    
    debug_file = "./test_workspace/debug_test.py"
    input_file = "./test_workspace/test_input.txt"
    output_file = "./test_workspace/debug_output.txt"
    
    with open(debug_file, 'w') as f:
        f.write(debug_code)
    
    with open(input_file, 'w') as f:
        f.write(TEST_INPUT)
    
    executor = CodeExecutor(timeout=10)
    result = executor.execute_with_debug(debug_file, input_file, output_file)
    
    if result['success']:
        print("✓ Debug execution successful")
        print("\nDebug output (stderr):")
        print("-" * 40)
        print(result['stderr'])
        print("-" * 40)
        
        # Analyze debug output
        print("\n4. Analyzing debug output...")
        analysis = debugger.analyze_debug_output(
            result['stderr'],
            EXPECTED_OUTPUT,
            ACTUAL_OUTPUT
        )
        
        print("✓ Analysis complete")
        print("\n💡 Root Cause Analysis:")
        print("-" * 40)
        print(analysis)
        print("-" * 40)
    else:
        print(f"✗ Debug execution failed: {result['error_message']}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    
    # Cleanup
    import shutil
    if os.path.exists("./test_workspace"):
        shutil.rmtree("./test_workspace")

if __name__ == "__main__":
    main()
