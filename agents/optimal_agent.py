from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validator import CodeValidator


class OptimalAgent:
    """Agent responsible for generating optimal/efficient solutions."""

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
        self.system_prompt = """You are an expert competitive programmer.

Generate COMPLETE, EFFICIENT Python solutions. Maximum 80 lines.

CRITICAL RULES:
1. MINIMAL COMMENTS (maximum 3 lines)
2. Code must be COMPLETE and RUNNABLE
3. Must have main execution block
4. Optimize for time/space complexity
5. Read from stdin, print to stdout
6. Clean, concise code

REQUIRED STRUCTURE:
```
def solve():
    # read input
    # compute answer efficiently
    return result

T = int(input())
for _ in range(T):
    print(solve())
```

ABSOLUTELY FORBIDDEN:
- Excessive comments
- Explanatory text
- Pseudocode
- Incomplete code

RESPOND WITH CODE ONLY. MINIMAL COMMENTS. COMPLETE SOLUTIONS."""

    def generate_solution(self, problem_statement: str, feedback: Optional[str] = None, attempt: int = 1) -> str:
        """Generate optimal solution for the given problem."""
        
        max_retries = 2
        validator = CodeValidator()
        
        for retry in range(max_retries):
            user_message = f"""Problem: {problem_statement}

Generate COMPLETE optimal Python code. MINIMAL COMMENTS (max 3 lines). Maximum 80 lines."""

            if feedback:
                user_message += f"""

FEEDBACK (attempt {attempt - 1}):
{feedback[:1000]}

Fix the bug. Generate COMPLETE corrected code."""

            if retry > 0:
                user_message += f"""

RETRY {retry + 1}/{max_retries}: Code was INCOMPLETE or too verbose.
Generate CONCISE, COMPLETE code."""

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]

            response = self.model.invoke(
                messages,
                max_tokens=3000  # Reasonable limit for optimal solutions
            )
            code = response.content.strip()

            # Remove markdown
            if code.startswith("```python"):
                code = code.split("```python")[1].split("```")[0].strip()
            elif code.startswith("```"):
                code = code.split("```")[1].split("```")[0].strip()

            # Remove excessive comments
            code_lines = code.split('\n')
            cleaned_lines = []
            comment_count = 0
            
            for line in code_lines:
                stripped = line.strip()
                if stripped.startswith('#'):
                    comment_count += 1
                    if comment_count <= 5:  # Allow max 5 comment lines for optimal
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            
            code = '\n'.join(cleaned_lines)
            
            # Check line count
            if len(code_lines) > 150:
                print(f"  ⚠️  Generated code too long ({len(code_lines)} lines) - retry {retry + 1}/{max_retries}")
                continue

            # Validate
            is_valid, error_msg = validator.is_complete(code)
            
            if is_valid:
                print(f"  ✓ Generated optimal solution ({len(code_lines)} lines)")
                return code
            else:
                print(f"  ⚠️  Validation failed (retry {retry + 1}/{max_retries}): {error_msg}")
                if retry < max_retries - 1:
                    print(f"  → Retrying...")
        
        print(f"  ⚠️  Using last generated code after {max_retries} retries")
        return code
