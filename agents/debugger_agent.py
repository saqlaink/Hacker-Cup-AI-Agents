from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict


class DebuggerAgent:
    """Agent responsible for adding debugging instrumentation to failed solutions."""

    def __init__(self, model_name: str):
        # Parse model name (format: "google:model-name")
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name

        # Remove 'models/' prefix if present - LangChain adds it automatically
        if model.startswith("models/"):
            model = model.replace("models/", "")

        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.2)
        self.system_prompt = """You are an expert debugging assistant for competitive programming.

Your task is to add strategic debug print statements to understand why a solution is failing.

Guidelines:
- Add print statements to STDERR using `print(..., file=sys.stderr)`
- NEVER modify the stdout output - it must remain unchanged for testing
- Add debug prints at critical points:
  1. After parsing input to show what was read
  2. At the start of main logic to show initial state
  3. Inside loops to show iteration variables and intermediate results
  4. Before computing final answer to show calculation steps
  5. At decision points (if/else branches)
- Use descriptive labels like `DEBUG: variable_name = value`
- Keep debug output concise but informative
- Show data structures (lists, dicts) when relevant
- DO NOT change the logic or algorithm, only add debugging

CRITICAL REQUIREMENT: Your response MUST contain ONLY valid, runnable Python code.
Do NOT include any surrounding text, explanations, comments, markdown formatting like ```python, or any sentences introducing the code.
Start your response immediately with `import sys` or the first necessary line of Python code.

Output ONLY the Python code with debug statements added, no markdown, no explanations.
"""

    def add_debug_instrumentation(self, code: str, test_input: str, expected_output: str, 
                                   actual_output: str, diff: str) -> str:
        """Add debug print statements to help understand where logic fails."""
        
        user_message = f"""Add debug instrumentation to this failing solution:

=== CURRENT CODE ===
{code}

=== TEST INPUT ===
{test_input}

=== EXPECTED OUTPUT ===
{expected_output}

=== ACTUAL OUTPUT ===
{actual_output}

=== DIFF ===
{diff}

Add strategic debug print statements (to stderr) to trace:
1. What input values are being parsed
2. Intermediate calculation steps
3. Loop iterations and counters
4. Decision branch selections
5. Final values before output

Remember: Print to stderr, never modify stdout. Keep the algorithm logic identical.

Return the complete code with debug statements added.
"""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = self.model.invoke(messages)
        code = response.content.strip()

        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()

        return code

    def analyze_debug_output(self, debug_stderr: str, expected_output: str, 
                           actual_output: str) -> str:
        """Analyze debug output to identify where logic diverges."""
        
        user_message = f"""Analyze this debug output to identify the root cause of the error:

=== DEBUG OUTPUT (from stderr) ===
{debug_stderr}

=== EXPECTED OUTPUT ===
{expected_output}

=== ACTUAL OUTPUT ===
{actual_output}

Based on the debug trace:
1. Identify where the logic first goes wrong
2. Explain what should happen vs what is happening
3. Suggest specific fixes to the algorithm

Provide a clear, concise analysis in 2-3 sentences focusing on the root cause.
"""

        messages = [
            {"role": "user", "content": user_message}
        ]

        response = self.model.invoke(messages)
        return response.content.strip()

