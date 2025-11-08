#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Agent Programming Problem Solver

This system uses three specialized agents to solve programming problems:
1. TesterAgent: Generates small test cases
2. BruteAgent: Creates a correct but potentially inefficient solution
3. OptimalAgent: Iteratively develops an efficient solution
"""

import sys
import io
import argparse
from orchestrator import ProblemSolverOrchestrator

# Ensure UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Multi-Agent Programming Problem Solver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use auto-generated test cases (default)
  python main.py

  # Use custom test input file
  python main.py --custom-test my_tests.txt

  # Use custom problem file and custom tests
  python main.py --problem hard_problem.txt --custom-test hard_tests.txt
        """
    )
    parser.add_argument(
        '--problem', '-p',
        default='PROBLEM.txt',
        help='Path to problem statement file (default: PROBLEM.txt)'
    )
    parser.add_argument(
        '--custom-test', '-t',
        default=None,
        help='Path to custom test input file (overrides config and auto-generation)'
    )
    
    args = parser.parse_args()

    # Read problem statement from file
    problem_file = args.problem

    try:
        with open(problem_file, 'r', encoding='utf-8') as f:
            problem_statement = f.read().strip()
    except FileNotFoundError:
        print(f"Error: {problem_file} not found!")
        print(f"Please create a {problem_file} file with your problem statement.")
        return 1

    print("Multi-Agent Programming Problem Solver")
    print("=" * 80)
    print(f"\nProblem loaded from: {problem_file}")
    
    # Show custom test info if provided
    if args.custom_test:
        print(f"Custom test input: {args.custom_test}")
    
    print("\n" + problem_statement)
    print("\n")

    # Initialize orchestrator
    orchestrator = ProblemSolverOrchestrator()
    
    # Override config with CLI argument if provided
    if args.custom_test:
        orchestrator.config['execution']['custom_test_input'] = args.custom_test

    # Solve the problem
    success, optimal_code, metadata = orchestrator.solve(problem_statement)

    # Print results
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Success: {success}")
    print(f"Attempts used: {metadata['attempts']}/{orchestrator.max_attempts}")
    print(f"Custom test used: {metadata.get('custom_test_used', False)}")
    print(f"Test cases generated: {metadata['test_cases_generated']}")
    print(f"Brute force generated: {metadata['brute_force_generated']}")
    print(f"Brute force executed: {metadata['brute_force_executed']}")
    print(f"Optimal solution found: {metadata['optimal_solution_found']}")

    if metadata['errors']:
        print(f"\nErrors encountered: {len(metadata['errors'])}")
        for i, error in enumerate(metadata['errors'], 1):
            print(f"  {i}. {error}")

    if success and optimal_code:
        print("\n" + "=" * 80)
        print("OPTIMAL SOLUTION CODE:")
        print("=" * 80)
        print(optimal_code)
        print("\n")
        print(f"Solution saved to: {orchestrator.files['optimal_solution']}")
    else:
        print("\nFailed to find a working solution.")
        if orchestrator.files['brute_solution']:
            print(f"Brute force solution available at: {orchestrator.files['brute_solution']}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
