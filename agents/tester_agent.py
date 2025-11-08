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

        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.5)
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

    # New: Adversarial and high-coverage generation
    def generate_adversarial_cases(self, problem_statement: str, target_cases: int = 12) -> str:
        """Generate adversarial, boundary, and tricky cases strictly following the input format.

        The model must output a single input blob beginning with T, followed by exactly T test cases.
        """
        adv_system = """You are an expert in adversarial test generation for competitive programming.

Generate a HIGH-COVERAGE set of test cases that strictly matches the input format described in the problem statement.

Rules:
- Output ONLY valid input, no explanations or markdown
- First line MUST be T (the number of test cases)
- Provide exactly T cases with NO blank lines between them unless the format requires
- Include boundary and tricky patterns: minimums, maximums, all-equal, alternating, sorted, reverse-sorted, random, degenerate edge cases, and stress-shaped small maxima
- Keep sizes SMALL but diverse so a brute-force solution can run locally
- Exactly match whitespace specified by the format; avoid trailing spaces
"""

        adv_user = f"""Generate approximately {target_cases} adversarial test cases for this problem.

Problem statement:
{problem_statement}

IMPORTANT:
- Output ONLY the raw test input, nothing else
- Begin with T on the first line where T equals the number of test cases you provide
- Do not include any markdown fences
"""

        messages = [
            {"role": "system", "content": adv_system},
            {"role": "user", "content": adv_user}
        ]

        response = self.model.invoke(messages)
        content = response.content.strip()

        # Remove accidental markdown blocks
        if content.startswith("```"):
            lines = content.split("\n")
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        return content

    def generate_combined_test_cases(self, problem_statement: str) -> str:
        """Generate a combined suite: small + adversarial, with a single T header.

        Strategy:
        - Generate the regular small cases using the default prompt
        - Generate adversarial cases using a stricter prompt
        - Combine by summing T headers and concatenating bodies
        - No blank lines added
        """
        small = self.generate_test_cases(problem_statement)
        adv = self.generate_adversarial_cases(problem_statement)

        def split_block(block: str):
            lines = [ln.rstrip() for ln in block.splitlines() if ln is not None]
            lines = [ln for ln in lines if ln != ""]  # be safe about stray blanks
            if not lines:
                return 0, []
            try:
                t = int(lines[0].strip())
                body = lines[1:]
                return t, body
            except Exception:
                # If we can't parse T, treat whole block as one case blob
                return 1, lines

        t_small, body_small = split_block(small)
        t_adv, body_adv = split_block(adv)

        total_t = t_small + t_adv
        combined_lines = [str(total_t)] + body_small + body_adv
        combined = "\n".join(combined_lines).strip() + "\n"
        return combined
