import subprocess
import os
from typing import Tuple, Dict


class CodeExecutor:
    """Utility to execute Python code with given input."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(self, code_file: str, input_file: str, output_file: str) -> Tuple[bool, str]:
        """
        Execute Python code with input from file and save output to file.

        Args:
            code_file: Path to Python file to execute
            input_file: Path to input file
            output_file: Path to save output

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        if not os.path.exists(code_file):
            return False, f"Code file not found: {code_file}"

        if not os.path.exists(input_file):
            return False, f"Input file not found: {input_file}"

        try:
            with open(input_file, 'r') as f_in:
                input_data = f_in.read()

            result = subprocess.run(
                ['python3', code_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode != 0:
                error_msg = f"Execution failed with return code {result.returncode}\n"
                error_msg += f"STDERR: {result.stderr}\n"
                error_msg += f"STDOUT: {result.stdout}"
                return False, error_msg

            # Save output
            with open(output_file, 'w') as f_out:
                f_out.write(result.stdout)

            return True, ""

        except subprocess.TimeoutExpired:
            return False, f"Execution timed out after {self.timeout} seconds"
        except Exception as e:
            return False, f"Execution error: {str(e)}"

    def execute_with_debug(self, code_file: str, input_file: str, output_file: str) -> Dict:
        """
        Execute Python code and capture both stdout and stderr.

        Args:
            code_file: Path to Python file to execute
            input_file: Path to input file
            output_file: Path to save output

        Returns:
            Dict with keys: success, stdout, stderr, error_message
        """
        if not os.path.exists(code_file):
            return {
                'success': False,
                'stdout': '',
                'stderr': '',
                'error_message': f"Code file not found: {code_file}"
            }

        if not os.path.exists(input_file):
            return {
                'success': False,
                'stdout': '',
                'stderr': '',
                'error_message': f"Input file not found: {input_file}"
            }

        try:
            with open(input_file, 'r') as f_in:
                input_data = f_in.read()

            result = subprocess.run(
                ['python3', code_file],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            # Save output
            with open(output_file, 'w') as f_out:
                f_out.write(result.stdout)

            if result.returncode != 0:
                return {
                    'success': False,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'error_message': f"Execution failed with return code {result.returncode}"
                }

            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'error_message': ''
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': '',
                'error_message': f"Execution timed out after {self.timeout} seconds"
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': '',
                'error_message': f"Execution error: {str(e)}"
            }
