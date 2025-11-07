from langchain_google_genai import ChatGoogleGenerativeAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validator import CodeValidator


class BruteAgent:
    """Agent responsible for generating brute force solutions."""

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
        self.system_prompt = """You are an expert at writing concise, correct Python code.

Generate a COMPLETE brute force solution. Maximum 50 lines of code.

CRITICAL RULES:
1. NO COMMENTS ALLOWED (except 1-2 if absolutely necessary)
2. Code must be COMPLETE and RUNNABLE
3. Must have main execution block
4. Must read from stdin and print to stdout
5. Simple, straightforward logic only
6. Each test case output on new line

REQUIRED STRUCTURE:
```
def solve():
    # read input
    # compute answer
    return result

T = int(input())
for _ in range(T):
    print(solve())
```

ABSOLUTELY FORBIDDEN:
- Explanatory comments
- Pseudocode
- Incomplete functions
- Long explanations
- Markdown formatting

RESPOND WITH CODE ONLY. NO TEXT. NO COMMENTS. JUST CODE."""

    def generate_solution(self, problem_statement: str) -> str:
        """Generate brute force solution for the given problem."""
        
        max_retries = 3
        validator = CodeValidator()
        
        for attempt in range(max_retries):
            user_message = f"""Problem: {problem_statement}

Generate COMPLETE Python code. NO COMMENTS. Maximum 50 lines."""

            if attempt > 0:
                user_message += f"""

RETRY {attempt + 1}/{max_retries}: Previous code was INCOMPLETE or had too many comments.
Generate CONCISE, COMPLETE code with NO EXPLANATORY COMMENTS."""

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]

            # Set reasonable token limit to force concise code
            response = self.model.invoke(
                messages,
                max_tokens=2000  # Lower limit forces concise code
            )
            code = response.content.strip()

            # Remove markdown code blocks if present
            if code.startswith("```python"):
                code = code.split("```python")[1].split("```")[0].strip()
            elif code.startswith("```"):
                code = code.split("```")[1].split("```")[0].strip()

            # Remove excessive comments (keep only minimal ones)
            code_lines = code.split('\n')
            cleaned_lines = []
            comment_count = 0
            
            for line in code_lines:
                stripped = line.strip()
                # Skip pure comment lines (allow inline comments)
                if stripped.startswith('#'):
                    comment_count += 1
                    if comment_count <= 3:  # Allow max 3 comment lines
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            
            code = '\n'.join(cleaned_lines)
            
            # Check line count
            if len(code_lines) > 100:
                print(f"  ⚠️  Generated code too long ({len(code_lines)} lines) - retry {attempt + 1}/{max_retries}")
                continue

            # Validate code completeness
            is_valid, error_msg = validator.is_complete(code)
            
            if is_valid:
                print(f"  ✓ Generated concise brute force ({len(code_lines)} lines)")
                return code
            else:
                print(f"  ⚠️  Code validation failed (attempt {attempt + 1}/{max_retries}): {error_msg}")
                if attempt < max_retries - 1:
                    print(f"  → Retrying...")
        
        # If all retries failed, return the last attempt anyway
        print(f"  ⚠️  Warning: Using last generated code after {max_retries} attempts")
        return code
