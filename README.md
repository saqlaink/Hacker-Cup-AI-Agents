# 🤖 Hacker Cup AI Agents - Multi-Agent Problem Solving System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange.svg)](https://ai.google.dev/)

An advanced multi-agent AI system designed to solve competitive programming problems through intelligent collaboration, iterative refinement, and comprehensive validation.

## 📖 Description

**Hacker Cup AI Agents** is a production-ready competitive programming assistant built on Meta's Hacker Cup AI Starter Kit. This enhanced implementation features seven specialized AI agents that work collaboratively to solve algorithmic challenges with unprecedented reliability and insight.

**Based on**: Meta Hacker Cup AI Starter Kit  
**Enhanced by**: AlgoUniversity Team

The system employs seven specialized AI agents working in concert:
- **TesterAgent** - Generates comprehensive test cases including adversarial scenarios
- **BruteAgent** - Creates guaranteed-correct reference solutions
- **OptimalAgent** - Iteratively develops efficient solutions with feedback learning
- **DebuggerAgent** - Instruments failing code and performs trace analysis
- **ValidatorAgent** - Validates logic, detects edge cases, provides confidence scoring
- **ComplexityAgent** - Analyzes time/space complexity with optimization suggestions
- **WebSearchAgent** - Intelligently searches for algorithm hints (deferred until needed)

This approach ensures correctness through differential testing, achieves optimal performance through AI-guided iteration, and provides deep introspection through validation and debugging pipelines.

## 🎯 Overview

### Key Features

✅ **Seven Specialized Agents** - TesterAgent, BruteAgent, OptimalAgent, DebuggerAgent, ValidatorAgent, ComplexityAgent, WebSearchAgent  
✅ **Deferred Web Search** - Intelligently searches for algorithm hints after 2 failed attempts (DuckDuckGo, free)  
✅ **Differential Testing** - Validates solutions against brute force baseline  
✅ **Iterative Refinement** - Up to 5 configurable attempts with enhanced feedback loops  
✅ **Pre-Execution Validation** - Complexity analysis and logic validation before running code  
✅ **Debug Instrumentation** - Automatic trace analysis for failing solutions  
✅ **Custom Test Input** - Provide your own test cases or auto-generate  
✅ **Environment-Based Configuration** - Secure API key management via .env files  
✅ **FREE Tier** - Uses Google Gemini (250 requests/day free)  
✅ **Interactive Viewer** - Beautiful HTML dashboard with comprehensive results  
✅ **Python-Only** - Clean codebase, extensively documented, easy to extend  

### Architecture

![Architecture Diagram](strategy.png)


## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/saqlaink/Hacker-Cup-AI-Agents.git
cd Hacker-Cup-AI-Agents
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Multi-agent orchestration framework
- `langchain-google-genai` - Google Gemini integration (FREE tier)
- `pyyaml` - Configuration management
- `ddgs` - Free web search for algorithm hints (DuckDuckGo)
- `python-dotenv` - Environment variable management for secure API keys

### Step 3: Configure Environment

Create a `.env` file for secure API key storage:

```bash
cp .env .env.local  # Or create new .env file
```

Edit `.env`:

```
GOOGLE_API_KEY=your-actual-api-key-here
```

**Get FREE API Key:**

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key (starts with `AIza...`)
4. Paste into `.env` file

> ⚠️ **Security Note**: Never commit `.env` to version control. The file is already in `.gitignore`.

## ⚙️ Configuration

### API Key Configuration

The system loads API keys from environment variables for security.

Edit `config.yaml`:

```yaml
api_keys:
  # Loaded from environment variable via .env file
  google: "${GOOGLE_API_KEY}"
```

Alternatively, set directly in your shell:

```bash
export GOOGLE_API_KEY="your-api-key"
```

### Choose Models

The system uses **FREE** Google Gemini models. Enhanced configuration with all agents:

```yaml
models:
  tester_agent: "google:gemini-2.5-flash"
  brute_agent: "google:gemini-2.5-flash"
  optimal_agent: "google:gemini-2.5-flash"
  debugger_agent: "google:gemini-2.5-flash"
  validator_agent: "google:gemini-2.0-flash"
  complexity_agent: "google:gemini-2.0-flash"

execution:
  max_optimal_attempts: 5
  timeout_seconds: 30
  custom_test_input: null
  enable_web_search: true  # Deferred until 2 failures
```

#### Available Google Gemini Models (FREE Tier)

Check https://ai.google.dev/gemini-api/docs/rate-limits for latest rate limits and free-tier quota.

- `google:gemini-2.5-flash` - Fast, efficient (250 free requests/day)
- `google:gemini-2.5-flash-lite` - Faster, cheaper (1000 free requests/day)
- `google:gemini-2.5-pro` - Most capable (100 free requests/day)


### Adjust Execution Parameters

```yaml
execution:
  max_optimal_attempts: 5      # Maximum retry attempts
  timeout_seconds: 30          # Code execution timeout
  enable_web_search: true      # Enable web search for algorithm hints (free)
  custom_test_input: null      # Path to custom test file (null = auto-generate)
```

### Customize Output Directory

```yaml
output:
  workspace_dir: "./workspace"           # Output directory
  preserve_intermediate: true            # Keep all generated files
```

## 📝 Usage

### Step 1: Define Your Problem

Create or edit `PROBLEM.txt` with your problem statement:

```
Given an array of integers, find the maximum sum of any contiguous subarray.

Input Format:
- First line: n (size of array)
- Second line: n space-separated integers

Output Format:
- Single integer: maximum subarray sum

Constraints:
- 1 <= n <= 10^5
- -10^4 <= array[i] <= 10^4

Example:
Input:
5
-2 1 -3 4 -1

Output:
4

Explanation: The subarray [4] has the maximum sum of 4.
```

### Step 2: Run the Solver

```bash
python main.py
```

**What Happens:**

1. **Loads Problem** - Reads `PROBLEM.txt`
2. **Generates Test Cases** - TesterAgent creates 3-5 small test inputs (or loads custom tests)
3. **Creates Brute Force** - BruteAgent generates a correct O(n²-n³) solution
4. **Executes Brute Force** - Saves expected outputs
5. **Optimizes Solution** - OptimalAgent attempts efficient O(n) solution
6. **Pre-Execution Validation** - ValidatorAgent and ComplexityAgent check solution quality
7. **(Deferred) Web Search** - After 2 failures, WebSearchAgent finds algorithm hints
8. **Debug Analysis** - On failures, DebuggerAgent instruments code and analyzes traces
9. **Validates & Retries** - Compares outputs, retries with enhanced feedback if needed
10. **Saves Results** - Generates `workspace/results.json` for the viewer

**Live Progress Indicators:**

```
⠋ Generating test cases with TesterAgent... (00:03)
⠙ Generating brute force solution with BruteAgent... (00:05)
⠹ Generating optimal solution (attempt 1/5)... (00:04)
```

### Step 3: View Results

#### Start HTTP Server

```bash
python -m http.server 8000
```

Then open: http://localhost:8000/viewer.html

*(HTTP server needed to avoid CORS restrictions)*


## 📁 Output Files

All files saved to `workspace/` (configurable):

```
```
workspace/
├── small_inputs.txt              # Generated test cases
├── small_outputs.txt             # Expected outputs (from brute force)
├── brute.py                      # Brute force solution
├── optimal_attempt_1.py          # First attempt at optimal solution
├── optimal_attempt_1_output.txt  # Output from first attempt
├── optimal_attempt_1_debug.py    # Instrumented version (if failed)
├── optimal_attempt_1_debug_output.txt  # Debug trace
├── optimal_attempt_2.py          # Second attempt (if needed)
├── optimal_attempt_2_output.txt
├── ...                           # Up to 5 attempts (configurable)
├── optimal.py                    # Final solution
├── op.txt                        # Final output
└── results.json                  # Complete metadata for viewer
```
└── results.json                  # Complete metadata for viewer
```


## 📦 Project Structure

```
Hacker-Cup-AI-Agents/
├── .env                          # Environment variables (gitignored, create from template)
├── .gitignore                    # Git exclusions
├── PROBLEM.txt                   # Your problem statement (REQUIRED)
├── config.yaml                   # Configuration file
├── main.py                       # Entry point
├── orchestrator.py               # Multi-agent coordinator with deferred web search
├── viewer.html                   # Web-based results viewer
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── QUICKSTART.md                 # Quick reference guide
├── PROJECT_OVERVIEW.md           # Comprehensive architecture & workflow documentation
├── WEBSEARCH_FEATURE.md          # WebSearchAgent documentation
├── DEBUGGER_FEATURE.md           # DebuggerAgent documentation
├── FINAL_SUMMARY.md              # Complete feature summary
├── test_web_search.py            # Web search test suite
├── test_debugger.py              # Debugger test suite
├── LICENSE                       # MIT License
├── agents/
│   ├── __init__.py
│   ├── tester_agent.py          # Test case generator
│   ├── brute_agent.py           # Brute force solution generator
│   ├── optimal_agent.py         # Optimal solution generator
│   ├── debugger_agent.py        # Solution debugger with trace analysis
│   ├── validator_agent.py       # Logic validator with confidence scoring
│   ├── complexity_agent.py      # Complexity analyzer with optimization suggestions
│   └── web_search_agent.py      # Web search for algorithm hints (deferred)
├── utils/
│   ├── __init__.py
│   ├── executor.py              # Code execution utility with debug capture
│   ├── comparator.py            # Output comparison utility
│   ├── progress.py              # Live progress indicators
│   └── validator.py             # Additional validation utilities
└── workspace/                    # Generated files (gitignored)
    └── ...
```

## 🤝 Contributing

Contributions are welcome! This project builds upon Meta's Hacker Cup AI Starter Kit with significant enhancements. See `PROJECT_OVERVIEW.md` for architecture details.

### Ways to Contribute
- Report bugs or suggest features via GitHub Issues
- Submit pull requests with improvements
- Enhance agent prompts and strategies
- Add support for additional programming languages
- Improve documentation and examples

## 💡 Advanced Customization Ideas

This system is production-ready but can be extended further:

- **Configurable Web Search Threshold** - Make the "2 attempts" deferred trigger configurable in `config.yaml`
- **Multi-Language Support** - Add C++, Java, Rust execution and validation
- **Parallel Attempt Generation** - Create multiple solution approaches simultaneously
- **Interactive Problems** - Handle problems requiring judge interaction
- **Complexity Analysis in Viewer** - Display time/space complexity estimates in the web UI
- **Test Case Amplification** - Auto-generate edge cases based on failure patterns
- **Semantic Code Diffing** - AST-based comparison for more precise feedback
- **Execution Metrics** - Track runtime and memory usage per attempt
- **Multi-File Solutions** - Support projects with dependencies and modules

## 📄 License

MIT License

Copyright (c) 2025 AlgoUniversity Team

Original Starter Kit: Copyright (c) 2025 Nikita Agarwal, Nalin Abrol, Manas Kumar Verma, Nikhil Tadigopulla, Vivek Verma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

### Core Team
- **AlgoUniversity Team** - Enhanced implementation with 7-agent architecture, deferred web search, validation pipeline, and comprehensive documentation

### Original Starter Kit
- **Meta Hacker Cup AI Starter Kit** - Original multi-agent framework foundation
- **Original Authors**: Nikita Agarwal, Nalin Abrol, Manas Kumar Verma, Nikhil Tadigopulla, Vivek Verma

### Technologies
- **LangChain** - Multi-agent orchestration framework
- **Google Gemini** - Free and powerful LLM API
- **DuckDuckGo** - Free web search API
- **KaTeX** - LaTeX math rendering
- **Prism.js** - Syntax highlighting

### Inspiration
- **Meta Hacker Cup** - Competitive programming competition that inspired this project
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

- **LangChain** - Multi-agent framework
- **Google** - Free Gemini API access
- **FlamesBlue** - Beautiful web viewer
- **KaTeX** - LaTeX rendering
- **Prism.js** - Syntax highlighting
- **Meta** - Inspiration from Hacker Cup

## 🔗 Links

- **GitHub Repository**: https://github.com/saqlaink/Hacker-Cup-AI-Agents
- **Google Gemini API**: https://ai.google.dev/
- **LangChain Documentation**: https://python.langchain.com/
- **Meta Hacker Cup**: https://www.facebook.com/codingcompetitions/hacker-cup
- **Original Starter Kit**: Meta Hacker Cup AI Starter Kit

---

**Built with ❤️ by AlgoUniversity Team**

*Enhanced multi-agent competitive programming assistant based on Meta Hacker Cup AI Starter Kit*

**Version**: 3.0  
**Status**: Production Ready  
**License**: MIT
