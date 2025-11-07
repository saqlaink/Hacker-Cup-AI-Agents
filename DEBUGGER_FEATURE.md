# Debugger Agent - Enhanced Problem Solving

## Overview

The **Debugger Agent** is a new agent that automatically adds debug instrumentation to failing solutions and analyzes the execution trace to identify root causes of errors.

## How It Works

### 1. **Automatic Debug Instrumentation**
When an optimal solution produces incorrect output:
- The Debugger Agent adds strategic `print()` statements to stderr
- Debug points are placed at:
  - Input parsing
  - Intermediate calculations
  - Loop iterations
  - Decision branches
  - Final results

### 2. **Execution Trace Capture**
- The instrumented code is executed with the same test input
- Debug output (stderr) is captured separately from actual output (stdout)
- Output comparison remains unchanged

### 3. **Root Cause Analysis**
- The agent analyzes the debug trace
- Identifies where the logic diverges from expected behavior
- Provides specific guidance on what's wrong

### 4. **Enhanced Feedback**
- The next attempt receives:
  - Original diff
  - Debug analysis
  - Execution trace
  - Specific fix suggestions

## Integration

The Debugger Agent is automatically used by the orchestrator when:
1. An optimal solution executes successfully
2. But produces output that doesn't match the brute force solution

## Configuration

Add to `config.yaml`:

```yaml
models:
  debugger_agent: "google:gemini-2.5-flash"
```

If not specified, it defaults to the same model as `optimal_agent`.

## Example Workflow

```
Attempt 1: Output mismatch detected
  ↓
🔍 Running debug analysis...
  ↓
Adding debug print statements...
  ↓
Executing instrumented code...
  ↓
📋 Debug output captured (1234 chars)
  ↓
Analyzing execution trace...
  ↓
💡 Debug Analysis: "The loop is summing from 0 to n-1 instead of 1 to n, 
   causing all results to be off by 1. Change range(n) to range(1, n+1)."
  ↓
Enhanced feedback sent to Optimal Agent for Attempt 2
```

## Benefits

1. **Faster Convergence**: More specific feedback helps the agent fix issues quicker
2. **Better Understanding**: Debug traces reveal exactly where logic fails
3. **Reduced Attempts**: Targeted fixes instead of blind guessing
4. **Learning**: Analysis helps identify systematic errors

## Testing

Run the test script to see the debugger in action:

```bash
python test_debugger.py
```

This demonstrates:
- Debug instrumentation
- Execution with trace capture
- Root cause analysis

## Files Generated

For each failed attempt, the following files are created:

- `optimal_attempt_N.py` - Original failing code
- `optimal_attempt_N_debug.py` - Instrumented version
- `optimal_attempt_N_output.txt` - Actual output
- `optimal_attempt_N_debug_output.txt` - Output from debug version

## Implementation Details

### New Components

1. **`agents/debugger_agent.py`**: Core debugger agent
   - `add_debug_instrumentation()`: Adds debug prints
   - `analyze_debug_output()`: Analyzes traces

2. **`utils/executor.py`**: Enhanced executor
   - `execute_with_debug()`: Captures both stdout and stderr

3. **`orchestrator.py`**: Integration
   - Detects output mismatches
   - Runs debug analysis
   - Provides enhanced feedback

### Key Features

- **Non-invasive**: Only adds print statements to stderr
- **Preserves Logic**: Never modifies the algorithm
- **Smart Placement**: Debug points at critical locations
- **Concise Output**: Informative but not overwhelming

## Future Enhancements

Potential improvements:
- Variable value tracking across iterations
- Comparison with brute force intermediate states
- Automatic assertion generation
- Interactive debugging mode
- Breakpoint suggestions
