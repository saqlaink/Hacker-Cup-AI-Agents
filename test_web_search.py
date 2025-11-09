"""
Test script for WebSearchAgent
Verifies that web search functionality works correctly.

Additional regression test added to ensure orchestrator defers web search
until after two failed optimal attempts.
"""

from agents.web_search_agent import WebSearchAgent
from orchestrator import ProblemSolverOrchestrator

class _DummyOptimalAgent:
    """Deterministic failing optimal agent for testing deferred web search.
    Always returns code that raises an exception so we simulate failures and
    trigger web search after threshold.
    """
    def __init__(self):
        pass
    def generate_solution(self, problem_statement: str, feedback=None, attempt: int = 1):
        return "raise Exception('forced failure')"  # runtime error

def test_deferred_web_search_trigger():
    print("=" * 80)
    print("Testing deferred web search trigger (should activate after 2 failures)")
    print("=" * 80)
    # Create orchestrator but monkeypatch optimal_agent to deterministic failure
    orch = ProblemSolverOrchestrator()
    # Monkeypatch network/LLM-dependent agents with deterministic fakes
    orch.tester_agent.generate_combined_test_cases = lambda _p: "1\n5\n"
    orch.tester_agent.generate_test_cases = lambda _p: "1\n5\n"
    orch.brute_agent.generate_solution = lambda _p: "print('OK')\n"
    # Validator and complexity agents to fast-pass without LLM
    orch.validator_agent.quick_check = lambda code: {"passed": True}
    orch.complexity_agent.quick_complexity_estimate = lambda code: {
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "max_loop_depth": 0,
    }
    orch.complexity_agent.analyze_complexity = lambda code, ps: {
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "will_pass_time": True,
        "will_pass_space": True,
        "will_pass": True,
        "optimizations": [],
    }
    orch.validator_agent.validate_logic = lambda code, ps: {"passed": True, "confidence": 1.0}
    # Web search mocked to avoid network (keys must match extract_hints expectations)
    orch.web_search_agent.search_algorithm_hints = lambda ps: [
        {
            "title": "Dummy Hint",
            "link": "https://example.com/algorithms",
            "snippet": "Use X approach to optimize.",
            "source": "example.com",
            "relevance_score": 42,
        }
    ]
    # Force failing optimal agent and limit attempts
    orch.optimal_agent = _DummyOptimalAgent()
    orch.max_attempts = 3
    # Simple problem statement
    problem = "Find sum of two numbers."
    success, code, meta = orch.solve(problem)
    performed = meta.get('web_search_performed', False)
    attempts = meta.get('attempts', 0)
    if not performed:
        print("✗ Web search was never performed (expected after 2 failures)")
        return False
    if attempts < 2:
        print("✗ Web search performed too early (before two attempts)")
        return False
    print("✓ Web search performed after threshold failures as expected")
    return True


def test_basic_search():
    """Test basic web search functionality"""
    print("=" * 80)
    print("Testing WebSearchAgent - Basic Search")
    print("=" * 80)
    
    agent = WebSearchAgent()
    
    # Simple problem: Two Sum (common algorithmic problem)
    problem = """
    Given an array of integers nums and an integer target, return indices of the two numbers 
    such that they add up to target. You may assume that each input would have exactly one 
    solution, and you may not use the same element twice.
    
    Example:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    """
    
    print(f"\nProblem Statement:\n{problem}\n")
    print("Searching for algorithm hints...")
    print("-" * 80)
    
    try:
        # Search for hints
        results = agent.search_algorithm_hints(problem, max_results=5)
        
        if results:
            print(f"✓ Found {len(results)} relevant resources\n")
            
            # Display results
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']}")
                print(f"   Source: {result.get('source', 'N/A')}")
                print(f"   Link: {result['link']}")
                print(f"   Snippet: {result['snippet'][:150]}...")
                print(f"   Relevance: {result.get('relevance_score', 0)}")
                print()
            
            # Get formatted hints
            hints = agent.extract_hints(results)
            print("=" * 80)
            print("Formatted Hints for OptimalAgent:")
            print("=" * 80)
            print(hints)
            
            return True
        else:
            print("✗ No results found")
            return False
            
    except Exception as e:
        print(f"✗ Error during search: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complex_problem():
    """Test with a more complex algorithmic problem"""
    print("\n" + "=" * 80)
    print("Testing WebSearchAgent - Complex Problem (DP)")
    print("=" * 80)
    
    agent = WebSearchAgent()
    
    # Longest Increasing Subsequence
    problem = """
    Given an array of integers, find the length of the longest strictly increasing subsequence.
    
    A subsequence is a sequence derived from the array by deleting some or no elements 
    without changing the order of the remaining elements.
    
    Example:
    Input: nums = [10,9,2,5,3,7,101,18]
    Output: 4
    Explanation: The longest increasing subsequence is [2,3,7,101]
    """
    
    print(f"\nProblem Statement:\n{problem}\n")
    print("Searching for algorithm hints...")
    print("-" * 80)
    
    try:
        results = agent.search_algorithm_hints(problem, max_results=3)
        
        if results:
            print(f"✓ Found {len(results)} relevant resources\n")
            hints = agent.extract_hints(results)
            print(hints)
            return True
        else:
            print("✗ No results found")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "█" * 80)
    print("WebSearchAgent Test Suite")
    print("█" * 80 + "\n")
    
    # Run tests
    test1_passed = test_basic_search()
    test2_passed = test_complex_problem()
    test3_passed = test_deferred_web_search_trigger()
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Basic Search Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Complex Problem Test: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print(f"Deferred Trigger Test: {'✓ PASSED' if test3_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed! WebSearchAgent + deferred trigger working correctly.")
    else:
        print("\n⚠ Some tests failed. Please check the error messages above.")
