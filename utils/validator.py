"""Utility to validate generated code for completeness."""

import ast


class CodeValidator:
    """Validates that generated code is complete and well-formed."""
    
    @staticmethod
    def is_complete(code: str) -> tuple[bool, str]:
        """
        Check if code is complete and valid Python.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Code is empty"
        
        # Check for syntax errors
        try:
            ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        
        # Check for common signs of incomplete code
        lines = code.strip().split('\n')
        last_line = lines[-1].strip()
        
        # Check if code ends mid-comment
        if last_line.startswith('#'):
            # Check if there are multiple comment lines at the end
            comment_count = 0
            for line in reversed(lines):
                if line.strip().startswith('#') or not line.strip():
                    comment_count += 1
                else:
                    break
            
            if comment_count > 5:  # Too many trailing comments suggests incomplete code
                return False, "Code appears to end with excessive comments (possibly truncated)"
        
        # Check for incomplete statements
        incomplete_patterns = [
            'def ',
            'class ',
            'if ',
            'for ',
            'while ',
            'elif ',
            'else:',
            'try:',
            'except',
            'finally:',
            'with ',
        ]
        
        # Get last non-empty, non-comment line
        last_code_line = None
        for line in reversed(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                last_code_line = stripped
                break
        
        if last_code_line:
            for pattern in incomplete_patterns:
                if last_code_line.endswith(':') and any(pattern in last_code_line for pattern in incomplete_patterns):
                    return False, f"Code ends with incomplete block: {last_code_line}"
        
        # Check for main execution block
        has_main_block = any(
            'if __name__' in line or
            'for _ in range(int(input' in line or
            'T = int(input' in line or
            't = int(input' in line
            for line in lines
        )
        
        if not has_main_block:
            return False, "Code missing main execution block (no input/output handling)"
        
        # Check for output statements
        has_output = any(
            'print(' in line
            for line in lines
        )
        
        if not has_output:
            return False, "Code has no output statements (no print())"
        
        return True, ""
    
    @staticmethod
    def extract_main_code(code: str) -> str:
        """
        Extract main code, removing excessive comments and explanations.
        """
        lines = code.split('\n')
        cleaned_lines = []
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines at the start
            if not cleaned_lines and not stripped:
                continue
            
            # Handle multiline strings/comments
            if '"""' in line or "'''" in line:
                in_multiline_comment = not in_multiline_comment
                continue
            
            if in_multiline_comment:
                continue
            
            # Skip lines that are pure comments (but keep inline comments)
            if stripped.startswith('#'):
                # Only keep comments that seem structural (TODO, NOTE, etc.)
                if any(marker in stripped.upper() for marker in ['TODO', 'NOTE', 'FIXME', 'BUG']):
                    cleaned_lines.append(line)
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
