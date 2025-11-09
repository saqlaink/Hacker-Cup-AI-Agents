# WebSearchAgent Integration Guide

## Overview

The **WebSearchAgent** enhances the Multi-Agent Problem Solver by automatically searching the web for algorithm hints and similar problems before generating optimal solutions. This feature uses the free DuckDuckGo API (no rate limits) to discover relevant competitive programming resources.

## Features

✅ **Automatic Algorithm Discovery**: Searches for relevant algorithms, data structures, and solution approaches  
✅ **Free & Unlimited**: Uses DuckDuckGo API with no rate limits or API keys required  
✅ **Smart Query Generation**: Extracts algorithmic keywords from problem statements  
✅ **Trusted Sources**: Prioritizes results from codeforces.com, leetcode.com, geeksforgeeks.org, cp-algorithms.com, usaco.guide  
✅ **Relevance Scoring**: Ranks results by domain authority and keyword matching  
✅ **Seamless Integration**: Automatically augments problem statement for first optimal attempt  

## How It Works

### Workflow Integration

1. **Step 1**: Generate or load test cases (TesterAgent)
2. **Step 1.5**: 🆕 **Search web for algorithm hints** (WebSearchAgent)
   - Extract algorithmic keywords from problem
   - Generate targeted search query
   - Search DuckDuckGo for relevant resources
   - Filter and rank results by relevance
   - Format top 3 results as hints
3. **Step 2**: Generate brute force solution (BruteAgent)
4. **Step 3**: Execute brute force and generate outputs
5. **Step 4**: Generate optimal solution with web hints (OptimalAgent, first attempt)

### Search Strategy

The WebSearchAgent:
- **Extracts keywords**: Identifies algorithm terms (e.g., "dynamic programming", "binary search", "graph")
- **Generates queries**: Combines keywords with site filters (e.g., `dp knapsack site:codeforces.com OR site:leetcode.com`)
- **Fetches results**: Uses DuckDuckGo text search API
- **Ranks results**: Scores by domain authority (codeforces +10, leetcode +10) and keyword matches (+3 title, +1 snippet)
- **Formats hints**: Returns top 3 results with title, source, link, snippet

## Configuration

### Enable/Disable Web Search

Edit `config.yaml`:

```yaml
execution:
  enable_web_search: true  # Set to false to disable
```

### Supported Domains

The agent prioritizes results from:
- **codeforces.com** - Competitive programming problems and editorials
- **leetcode.com** - Algorithm problems with solutions
- **geeksforgeeks.org** - Algorithm tutorials and explanations
- **cp-algorithms.com** - Comprehensive algorithm library
- **usaco.guide** - USACO training resources
- **stackoverflow.com** - Programming Q&A
- **atcoder.jp** - Japanese competitive programming
- **topcoder.com** - Algorithm competitions
- **hackerrank.com** - Coding challenges
- **codechef.com** - Competitive programming

## Installation

### Install Dependencies

```bash
pip install ddgs>=1.0.0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Usage

### Automatic (Default)

Web search is enabled by default. Simply run the solver:

```bash
python main.py --problem PROBLEM.txt
```

The WebSearchAgent will automatically:
1. Search for algorithm hints after test generation
2. Augment the problem statement with hints
3. Provide enhanced context to OptimalAgent on first attempt

### Manual Testing

Test the WebSearchAgent independently:

```bash
python test_web_search.py
```

This runs two test cases:
- **Basic Search**: Two Sum problem
- **Complex Problem**: Longest Increasing Subsequence (DP)

### Programmatic Usage

```python
from agents.web_search_agent import WebSearchAgent

# Initialize agent
agent = WebSearchAgent()

# Search for hints
problem = "Given an array, find the longest increasing subsequence..."
results = agent.search_algorithm_hints(problem, max_results=5)

# Get formatted hints
hints = agent.extract_hints(results)
print(hints)
```

## Example Output

```
================================================================================
STEP 1.5: Searching web for algorithm hints...
================================================================================
⠋ Searching for algorithm hints with WebSearchAgent
✓ Found 5 relevant resources
✓ Algorithm hints will be provided to OptimalAgent

=== Algorithm Hints from Web Search ===

The following resources may help with solving this problem:

1. Longest Increasing Subsequence - GeeksforGeeks
   Source: geeksforgeeks.org
   Link: https://www.geeksforgeeks.org/longest-increasing-subsequence-dp-3/
   Snippet: Learn how to find the longest increasing subsequence using dynamic programming...
   Relevance Score: 18

2. Longest Increasing Subsequence - CP-Algorithms
   Source: cp-algorithms.com
   Link: https://cp-algorithms.com/sequences/longest_increasing_subsequence.html
   Snippet: The longest increasing subsequence problem can be solved in O(n log n) time...
   Relevance Score: 16

3. LIS Tutorial - Codeforces
   Source: codeforces.com
   Link: https://codeforces.com/blog/entry/13257
   Snippet: Dynamic programming solution for finding longest increasing subsequence...
   Relevance Score: 15

Consider these algorithmic approaches when designing your solution.
==================================================
```

## Expected Improvements

- **30-50% improvement** on algorithm-heavy problems (DP, graphs, advanced data structures)
- **Faster convergence** - OptimalAgent gets hints on first attempt
- **Reduced attempts** - Better initial solution quality
- **Learning boost** - Discovers optimal approaches from community

## Troubleshooting

### No Results Found

**Symptom**: "No relevant algorithm hints found"

**Causes**:
- Very specific/unique problem with no online resources
- Network connectivity issues
- DuckDuckGo API temporary issues

**Solution**: The solver continues normally without hints (graceful fallback)

### Import Error

**Symptom**: `ModuleNotFoundError: No module named 'ddgs'`

**Solution**:
```bash
pip install ddgs>=1.0.0
```

### Search Timeout

**Symptom**: Search takes too long

**Solution**: The search has a built-in timeout and will continue without hints if it fails

## Disabling Web Search

To disable web search entirely:

1. **Method 1**: Edit `config.yaml`
   ```yaml
   execution:
     enable_web_search: false
   ```

2. **Method 2**: Remove ddgs dependency (search will be skipped automatically)

## Technical Details

### WebSearchAgent Class

```python
class WebSearchAgent:
    def search_algorithm_hints(problem_statement: str, max_results: int = 5) -> List[Dict]
    def _generate_query(problem_statement: str) -> str
    def _search_duckduckgo(query: str, max_results: int) -> List[Dict]
    def _filter_results(results: List[Dict], problem_statement: str) -> List[Dict]
    def extract_hints(search_results: List[Dict]) -> str
```

### Relevance Scoring

Results are scored based on:
- **Domain authority**: +10 for codeforces.com, leetcode.com, geeksforgeeks.org, etc.
- **Title match**: +3 per matching keyword in title
- **Snippet match**: +1 per matching keyword in snippet
- **Algorithm indicators**: +2 for "algorithm", "solution", "approach", "complexity", etc.

### Keyword Extraction

The agent recognizes 30+ algorithmic terms:
- Dynamic programming, greedy, binary search
- Graph algorithms (BFS, DFS, Dijkstra, Floyd-Warshall, etc.)
- Data structures (segment tree, fenwick tree, trie, etc.)
- Advanced techniques (sliding window, two pointers, etc.)

## Performance

- **Search time**: 1-3 seconds per query
- **API cost**: $0 (free DuckDuckGo API)
- **Rate limits**: None
- **Results**: Up to 5 per search (configurable)

## Future Enhancements

Potential improvements:
- [ ] Cache search results to avoid redundant queries
- [ ] Add more algorithm keyword patterns
- [ ] Support for multi-language problems
- [ ] Extract code snippets from search results
- [ ] Learn from successful searches to improve query generation

## Contributing

To improve the WebSearchAgent:

1. **Add more keywords**: Edit `algo_keywords` in `_generate_query()`
2. **Add more domains**: Edit `target_domains` in `__init__()`
3. **Improve scoring**: Modify `_filter_results()` logic
4. **Better formatting**: Enhance `extract_hints()` output

## License

This feature is part of the Meta HackerCup AI Starter Kit and follows the same MIT License.

---

**Questions?** See main README.md or open an issue on GitHub.
