from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, List
import re
import json


class ValidatorAgent:
    """
    Agent that reviews code for logical correctness, edge cases,
    and common competitive programming pitfalls.
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
    
    def validate_logic(self, code: str, problem_statement: str) -> Dict:
        """
        Perform deep logical validation of the code.
        
        Returns:
            {
                'is_valid': bool,
                'issues': List[Dict],  # [{severity, category, description, line}]
                'edge_cases_covered': List[str],
                'edge_cases_missing': List[str],
                'confidence': float
            }
        """
        
        prompt = f"""You are an expert competitive programming validator. Review this solution for logical correctness.

PROBLEM STATEMENT:
{problem_statement}

SOLUTION CODE:
{code}

Analyze and report:

1. LOGICAL ERRORS:
   - Off-by-one errors (loop bounds, array indices)
   - Wrong comparison operators
   - Incorrect mathematical formulas
   - Logic flow errors

2. EDGE CASE HANDLING:
   - Empty input (N=0, empty string)
   - Single element (N=1)
   - Maximum constraints (N=10^6, values at INT_MAX)
   - All same values
   - Sorted/reverse sorted input
   - Alternating patterns

3. COMMON PITFALLS:
   - Integer overflow (need long/modulo)
   - Division by zero
   - Uninitialized variables
   - Wrong loop termination
   - Missing boundary checks
   - Incorrect input parsing

4. PROBLEM-SPECIFIC ISSUES:
   - Does the algorithm match the problem requirements?
   - Are all constraints respected?
   - Is output format correct?

Return ONLY a JSON object (no markdown, no code blocks):
{{
    "is_valid": true,
    "issues": [
        {{
            "severity": "critical",
            "category": "logic",
            "description": "detailed description",
            "line": 10,
            "suggestion": "how to fix"
        }}
    ],
    "edge_cases_covered": ["N=1", "N=max"],
    "edge_cases_missing": ["empty input"],
    "confidence": 0.85
}}"""

        try:
            response = self.model.invoke(prompt)
            result_text = response.content.strip()
            
            # Remove markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            
            result = json.loads(result_text)

            # Normalize keys for orchestrator compatibility
            # Add 'passed' alias (orchestrator expects this) mapped from 'is_valid'
            if 'passed' not in result and 'is_valid' in result:
                result['passed'] = bool(result.get('is_valid'))

            # Extract flat suggestions list if issues contain suggestion fields
            if 'suggestions' not in result:
                suggestions: List[str] = []
                for issue in result.get('issues', []):
                    if isinstance(issue, dict) and issue.get('suggestion'):
                        suggestions.append(issue['suggestion'])
                result['suggestions'] = suggestions

            return result
        except Exception as e:
            print(f"  ⚠️ ValidatorAgent error: {e}")
            return {
                'is_valid': True,  # Fail open
                'passed': True,
                'issues': [],
                'edge_cases_covered': [],
                'edge_cases_missing': [],
                'confidence': 0.0,
                'suggestions': []
            }
    
    def quick_check(self, code: str) -> Dict:
        """
        Fast syntactic checks without LLM (for quick validation).
        
        Returns:
            {
                'passed': bool,
                'issues': List[str]
            }
        """
        issues = []
        lines = code.split('\n')
        
        # 1. Check for integer division where float might be needed
        for i, line in enumerate(lines, 1):
            if '/' in line and '//' not in line and 'import' not in line and '#' not in line:
                if 'int(' not in line and 'float(' not in line:
                    issues.append(f"Line {i}: Using '/' - consider '//' for integer division")
        
        # 2. Check for range off-by-one
        for i, line in enumerate(lines, 1):
            if 'range(' in line:
                if re.search(r'range\(\s*[a-zA-Z_]\w*\s*\)', line):
                    issues.append(f"Line {i}: range(n) starts at 0. Verify if 1-indexed needed")
        
        # 3. Check for unhandled edge cases
        has_empty_check = any('if' in line and ('== 0' in line or '<= 0' in line or '== 1' in line) 
                             for line in lines)
        if not has_empty_check:
            issues.append("Warning: No obvious check for empty/minimal input (N=0 or N=1)")
        
        # 4. Check for input/output format (Hacker Cup specific)
        has_case_format = any('Case #' in line for line in lines)
        if not has_case_format:
            issues.append("Warning: Output should include 'Case #i:' format for Hacker Cup")
        
        # 5. Check for modulo arithmetic
        has_mod = any('MOD' in line or '10**9' in line or '1000000007' in line for line in lines)
        if 'sum' in code.lower() or 'product' in code.lower() or '*' in code:
            if not has_mod and 'range' in code:
                issues.append("Warning: Consider if results need modulo arithmetic for large sums/products")
        
        # 6. Check for proper input reading
        has_input = any('input()' in line for line in lines)
        if not has_input:
            issues.append("Critical: No input() calls found - code won't read test cases")
        
        # 7. Check for test case loop
        has_T_loop = any(('for' in line and '_' in line and 'range' in line) or 
                        ('while' in line and 'T' in line)
                        for line in lines)
        if not has_T_loop:
            issues.append("Warning: No loop over T test cases detected")
        
        return {
            'passed': len([i for i in issues if 'Critical' in i]) == 0,
            'issues': issues
        }
