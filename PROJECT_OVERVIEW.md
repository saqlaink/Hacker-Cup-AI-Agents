# Meta HackerCup AI Multi-Agent Starter Kit

A comprehensive overview of the multi-agent competitive programming assistant, its architecture, workflow, configuration, and extensibility.

---
## 1. Mission & Philosophy
This project demonstrates how **multiple specialized AI agents** can collaborate to solve algorithmic problems reliably:
- Embrace correctness first (brute-force baseline + differential testing)
- Iterate toward optimal performance (feedback-driven refinement)
- Automatically surface algorithmic strategies (web search hints)
- Provide deep introspection (debug traces, validation, complexity analysis)

Designed for rapid experimentation during contests like **Meta Hacker Cup**, while remaining extensible for research.

---
## 2. Core Agents
| Agent | Role | Key Methods |
|-------|------|-------------|
| TesterAgent | Generates small + adversarial test cases | `generate_test_cases`, `generate_combined_test_cases` |
| BruteAgent | Produces a guaranteed-correct (slow) solution | `generate_solution` |
| OptimalAgent | Iteratively attempts efficient solution | `generate_solution` |
| DebuggerAgent | Instruments failing optimal attempts and analyzes traces | `add_debug_instrumentation`, `analyze_debug_output` |
| ValidatorAgent | Performs logical/structural validation | `quick_check`, `validate_logic` |
| ComplexityAgent | Estimates time and space complexity | `quick_complexity_estimate`, `analyze_complexity` |
| WebSearchAgent | Searches and extracts algorithm hints (deferred after 2 failed attempts) | `search_algorithm_hints`, `extract_hints` |

---
## 3. Orchestration Workflow
High-level loop (in `orchestrator.py`):
1. Load / generate test cases
2. (Deferred) Perform web search only **after two failed optimal attempts**
3. Generate brute force solution
4. Execute brute force to produce expected outputs
5. For each optimal attempt:
   - Generate code (augmented with web hints if available)
   - Run validation + complexity analysis
   - Execute and compare outputs
   - On mismatch: instrument + analyze with DebuggerAgent
   - Provide aggregated feedback to next attempt
6. Persist structured metadata to `workspace/results.json`
7. Serve visual report via `viewer.html`

Key invariants:
- Brute force must run successfully before optimal attempts proceed
- Each attempt stored independently for traceability
- Web search is idempotent; triggers once after threshold

---
## 4. Deferred Web Search Logic
Implemented directly in `orchestrator.py`:
- `web_search_after_attempts = 2`
- Trigger condition: (attempt runtime error OR wrong answer) AND attempt >= 2 AND search not yet performed
- Once performed, hints injected into subsequent attempts’ prompt context

Advantages:
- Reduces early noise/hint overfitting
- Gives agent a chance to solve easy problems unaided
- Brings in external guidance only when progress stalls

---
## 5. Configuration (`config.yaml`)
```yaml
api_keys:
  google: "${GOOGLE_API_KEY}"  # Loaded from environment (.env)

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
  enable_web_search: true

output:
  workspace_dir: "./workspace"
  preserve_intermediate: true

files:
  test_inputs: "small_inputs.txt"
  brute_solution: "brute.py"
  brute_outputs: "small_outputs.txt"
  optimal_solution: "optimal.py"
  optimal_outputs: "op.txt"
```
Add a `.env` file (excluded via `.gitignore`):
```
GOOGLE_API_KEY=replace-with-your-real-key
```

---
## 6. Execution Artifacts
Directory: `workspace/`
- `small_inputs.txt` – test cases
- `brute.py` / `small_outputs.txt` – baseline solution + expected output
- `optimal_attempt_{N}.py` / `optimal_attempt_{N}_output.txt` – attempt code + output
- `optimal_attempt_{N}_debug.py` / `_debug_output.txt` – instrumented failure analysis
- `optimal.py` / `op.txt` – latest candidate solution
- `results.json` – structured report consumed by `viewer.html`

`results.json` essentials:
```json
{
  "problem_statement": "...",
  "test_input": "...",
  "test_output": "...",
  "optimal_attempts": [
    {
      "attempt_number": 1,
      "verdict": "Wrong Answer | Accepted | Runtime Error | Generation Failed",
      "code": "...",
      "output_match": false,
      "output_diff": "...",
      "validation": { /* quick_check, complexity, logic */ }
    }
  ],
  "success": false,
  "total_attempts": 5,
  "has_validation_data": true,
  "web_hints": "..." (if performed)
}
```

---
## 7. Validation & Complexity
Each attempt runs four diagnostics:
1. Quick syntactic / style issues
2. Shallow complexity estimate (structural heuristics)
3. Deep complexity + pass/fail prognostics
4. Logic validation (edge cases, missing scenarios)

Feedback synthesizes critical issues into a prompt augmentation for the next attempt.

---
## 8. Debugging Flow
When outputs mismatch:
1. Compute diff summary
2. Instrument code to stderr (no mutation of algorithm semantics)
3. Execute instrumented version
4. Analyze trace for divergences
5. Build enhanced feedback: diff + trace summary + suggestions

---
## 9. Web Viewer (`viewer.html`)
Features:
- Problem statement (supports KaTeX math)
- Test input/output
- Brute force solution
- Attempt cards (reverse chronological)
- Verdict badges & color coding
- Modal diff display
- Complexity & validation metadata ready for future expansion

---
## 10. Extensibility Ideas
| Enhancement | Description |
|-------------|-------------|
| Parallel Attempt Generation | Spawn multiple strategy hypotheses concurrently (DP vs Greedy vs Divide & Conquer) |
| Multi-Language Support | Add C++ executor for performance benchmarking |
| Adaptive Attempt Budget | Dynamically increase max attempts if convergence probability high |
| Intermediate State Comparison | Compare step-by-step states with brute force to localize logic error |
| Prompt Caching | Reuse reasoning chains to accelerate similar problems |
| Semantic Diffing | Use AST-based comparison for more precise feedback |
| Test Case Amplification | Auto-generate edge cases based on failure signatures |

---
## 11. Running & Usage
Basic run:
```bash
python main.py
```
Serve viewer:
```bash
python -m http.server 8000
open http://localhost:8000/viewer.html
```
Inject custom tests:
```yaml
execution:
  custom_test_input: ./my_tests.txt
```
Or supply at runtime with env vars:
```bash
GOOGLE_API_KEY=... python main.py
```

---
## 12. Testing
Key test: `test_web_search.py` now includes deferred trigger check ensuring web search only runs after two consecutive failures.
Add your own tests by mocking agents for deterministic runs.

---
## 13. Security & Secrets
- No secrets should be committed; `.env` is gitignored.
- Expandable `os.path.expandvars` ensures `${VAR}` patterns resolve safely.
- All dynamic code execution is sandboxed via subprocess + timeout.

---
## 14. Error Modes & Handling
| Stage | Failure Mode | Handling |
|-------|--------------|----------|
| Test Generation | LLM failure | Abort with metadata, return False |
| Brute Execution | Runtime error | Abort: cannot validate further |
| Optimal Generation | LLM exception | Record attempt with generation failure |
| Optimal Execution | Timeout / runtime | Feedback passed; proceed to next attempt |
| Output Comparison | Mismatch | Debugger instrumentation + hint search (if threshold reached) |
| Web Search | Network error | Graceful skip, continue without hints |

---
## 15. Performance Considerations
- Brute force kept minimal to guarantee correctness quickly
- Deferred web search reduces overhead on trivially solvable problems
- ComplexityAgent early flags high nesting / potential TLE/MLE

---
## 16. License
MIT License (see `LICENSE`)

---
## 17. FAQ
**Q: Why defer web search?**
To avoid unnecessary context injection for easy tasks and reduce token usage.

**Q: Can I change the threshold?**
Yes—replace hardcoded `web_search_after_attempts = 2` in `orchestrator.py` with a config key.

**Q: How do I add another agent?**
Create file under `agents/`, import in `agents/__init__.py`, instantiate in `orchestrator.py`.

**Q: Are external sites scraped?**
No—only metadata via DuckDuckGo search results.


**Built for reliability, introspection, and iterative improvement.**
