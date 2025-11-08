from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, List
import re
import json


class ComplexityAgent:
    """
    Agent that analyzes time and space complexity of code
    and validates it against problem constraints.
    """
    
    def __init__(self, model_name: str):
        # Parse model name
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name
        
        if model.startswith("models/"):
            model = model[7:]
        
        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.1)
    
    def analyze_complexity(self, code: str, problem_statement: str) -> Dict:
        """
        Analyze time and space complexity and validate against constraints.
        
        Returns:
            {
                'time_complexity': str,
                'space_complexity': str,
                'will_pass': bool,
                'will_pass_time': bool,
                'will_pass_space': bool,
                'bottlenecks': List[str],
                'optimizations': List[str],
                'confidence': float
            }
        """
        
        prompt = f"""You are an expert in algorithm complexity analysis. Analyze this competitive programming solution.

PROBLEM STATEMENT (extract constraints like N ≤ 10^6):
{problem_statement}

SOLUTION CODE:
{code}

Perform detailed complexity analysis:

1. TIME COMPLEXITY:
   - Identify all loops (nested, sequential)
   - Identify recursive calls and their depth
   - Calculate Big-O notation
   - Estimate actual operation count for MAX input

2. SPACE COMPLEXITY:
   - Memory used by data structures
   - Recursion stack depth
   - Auxiliary space

3. CONSTRAINT VALIDATION:
   - Extract max N, M, T from problem
   - Calculate max operations (time limit typically allows ~10^8 operations/sec)
   - Will the solution TLE (Time Limit Exceeded)?
   - Will it MLE (Memory Limit Exceeded)?

4. BOTTLENECKS:
   - Which loops/operations dominate runtime?
   - Where is memory being allocated?

5. OPTIMIZATION SUGGESTIONS:
   - If too slow, suggest algorithmic improvements
   - If using too much memory, suggest space optimizations

Return ONLY a JSON object (no markdown):
{{
    "time_complexity": "O(N log N)",
    "space_complexity": "O(N)",
    "time_complexity_explained": "detailed breakdown",
    "space_complexity_explained": "detailed breakdown",
    "extracted_constraints": {{
        "N_max": 1000000,
        "T_max": 100
    }},
    "max_operations_estimate": 100000000,
    "operations_per_test": 1000000,
    "will_pass_time": true,
    "will_pass_space": true,
    "bottlenecks": ["nested loop at lines 20-25"],
    "optimizations": ["use prefix sums instead of nested loop"],
    "confidence": 0.9
}}"""

        try:
            response = self.model.invoke(prompt)
            result_text = response.content.strip()
            
            # Clean markdown
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            
            result = json.loads(result_text)
            
            # Overall pass/fail
            result['will_pass'] = result.get('will_pass_time', True) and result.get('will_pass_space', True)
            
            return result
        except Exception as e:
            print(f"  ⚠️ ComplexityAgent error: {e}")
            return {
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'will_pass': True,  # Fail open
                'will_pass_time': True,
                'will_pass_space': True,
                'reasoning': f'Analysis failed: {e}',
                'bottlenecks': [],
                'optimizations': [],
                'confidence': 0.0
            }
    
    def quick_complexity_estimate(self, code: str) -> Dict:
        """
        Fast heuristic-based complexity estimation without LLM.
        
        Returns:
            {
                'time_complexity': str,
                'space_complexity': str,
                'max_loop_depth': int,
                'has_recursion': bool
            }
        """
        lines = code.split('\n')
        
        # Count nested loops
        loop_depth = 0
        max_depth = 0
        indent_stack = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Track indentation
            indent = len(line) - len(line.lstrip())
            
            # Detect loop start
            if stripped.startswith('for ') or stripped.startswith('while '):
                loop_depth += 1
                max_depth = max(max_depth, loop_depth)
                indent_stack.append(indent)
            # Detect dedent
            elif indent_stack and indent <= indent_stack[-1]:
                while indent_stack and indent <= indent_stack[-1]:
                    indent_stack.pop()
                    loop_depth = max(0, loop_depth - 1)
        
        # Estimate time complexity based on nesting
        if max_depth == 0:
            time_complexity = "O(1) or O(N)"
        elif max_depth == 1:
            time_complexity = "O(N)"
        elif max_depth == 2:
            time_complexity = "O(N^2)"
        elif max_depth == 3:
            time_complexity = "O(N^3)"
        else:
            time_complexity = f"O(N^{max_depth})"
        
        # Check for sorting
        if '.sort' in code or 'sorted(' in code:
            time_complexity += " + O(N log N) sorting"
        
        # Check for recursion
        func_names = re.findall(r'def\s+(\w+)\s*\(', code)
        has_recursion = any(fname in code.split(f'def {fname}')[1] if f'def {fname}' in code else '' 
                           for fname in func_names)
        
        if has_recursion:
            time_complexity += " + recursion"
        
        # Rough space estimate
        if 'dict' in code or 'set(' in code or '{}' in code or 'defaultdict' in code:
            space_complexity = "O(N) - using hash structures"
        elif '[' in code and ']' in code and 'list' in code:
            space_complexity = "O(N) - using arrays/lists"
        else:
            space_complexity = "O(1) - constant space"
        
        return {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'max_loop_depth': max_depth,
            'has_recursion': has_recursion
        }
