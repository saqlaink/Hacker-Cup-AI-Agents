from langchain_google_genai import ChatGoogleGenerativeAI


class TesterAgent:
    """Agent responsible for generating small test cases from problem statement."""

    def __init__(self, model_name: str):
        # Parse model name (format: "google:model-name")
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name

        # Remove 'models/' prefix if present - LangChain adds it automatically
        if model.startswith("models/"):
            model = model.replace("models/", "")

        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.7)
        self.system_prompt = """You are a test case generation expert for programming problems.

Your task is to generate SMALL, simple test cases that adhere to the input format specified in the problem statement.

Guidelines:
- Generate 3-5 small test cases
- Follow the exact input format specified
- Use small values (arrays of size 2-5, numbers < 100, etc.)
- Cover edge cases (empty, single element, boundary values)
- Output ONLY the test input, nothing else - NO markdown, NO code blocks, NO explanations
- DO NOT add blank lines between test cases unless the problem format requires it
- DO NOT wrap output in ``` markers or any other formatting
- Each line should contain exactly what the problem specifies (no extra whitespace)

CRITICAL RULES:
1. The FIRST line must be T (the number of test cases)
2. After T, immediately provide the test cases WITHOUT blank lines in between
3. Format each test case exactly as shown in the problem's input format
4. NO blank lines unless explicitly required by the problem format
5. Output ONLY the raw test input data, nothing else!


Example for a problem with format "T / N / A1 A2 ... AN":
3
5
2 4 5 1 4
3
13 10 11
4
1 3 3 7

CRITICAL: Output ONLY the raw test input data above, nothing else!
"""

    def generate_test_cases(self, problem_statement: str) -> str:
        """Generate test cases for the given problem statement."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Generate small test cases for this problem:\n\n{problem_statement}"}
        ]

        response = self.model.invoke(messages)
        content = response.content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first and last lines if they are markdown markers
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        return content
