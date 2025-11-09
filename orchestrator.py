import os
import yaml
import json
import time
from typing import Dict, Optional, Tuple, List
from agents import TesterAgent, BruteAgent, OptimalAgent, DebuggerAgent, ValidatorAgent, ComplexityAgent, WebSearchAgent
from utils import CodeExecutor, OutputComparator, ProgressIndicator
from dotenv import load_dotenv


class ProblemSolverOrchestrator:
    """Main orchestrator for the multi-agent problem solving system."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize orchestrator with configuration."""
        # Load environment variables from .env if present
        load_dotenv()
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Set up API key
        api_keys = self.config.get('api_keys', {})

        # Google API key for Gemini: resolve from env or expand placeholders like ${GOOGLE_API_KEY}
        raw_google_key = api_keys.get('google')
        google_key = None
        if isinstance(raw_google_key, str):
            try:
                # Expand env var placeholders
                expanded = os.path.expandvars(raw_google_key).strip()
                if expanded and expanded != raw_google_key:
                    google_key = expanded
            except Exception:
                pass
        # Fallback to direct env var if not expanded
        if not google_key:
            google_key = os.getenv('GOOGLE_API_KEY')
        # Set into environment for downstream libraries
        if google_key:
            os.environ['GOOGLE_API_KEY'] = google_key

        # Initialize agents
        self.tester_agent = TesterAgent(self.config['models']['tester_agent'])
        self.brute_agent = BruteAgent(self.config['models']['brute_agent'])
        self.optimal_agent = OptimalAgent(self.config['models']['optimal_agent'])
        self.debugger_agent = DebuggerAgent(self.config['models'].get('debugger_agent', 
                                                                       self.config['models']['optimal_agent']))
        self.validator_agent = ValidatorAgent(self.config['models'].get('validator_agent',
                                                                        self.config['models']['optimal_agent']))
        self.complexity_agent = ComplexityAgent(self.config['models'].get('complexity_agent',
                                                                          self.config['models']['optimal_agent']))
        self.web_search_agent = WebSearchAgent()

        # Initialize utilities
        timeout = self.config['execution']['timeout_seconds']
        self.executor = CodeExecutor(timeout=timeout)
        self.comparator = OutputComparator()

        # Set up workspace
        self.workspace = self.config['output']['workspace_dir']
        os.makedirs(self.workspace, exist_ok=True)

        # File paths
        self.files = {
            'test_inputs': os.path.join(self.workspace, self.config['files']['test_inputs']),
            'brute_solution': os.path.join(self.workspace, self.config['files']['brute_solution']),
            'brute_outputs': os.path.join(self.workspace, self.config['files']['brute_outputs']),
            'optimal_solution': os.path.join(self.workspace, self.config['files']['optimal_solution']),
            'optimal_outputs': os.path.join(self.workspace, self.config['files']['optimal_outputs'])
        }

        self.max_attempts = self.config['execution']['max_optimal_attempts']

    def solve(self, problem_statement: str) -> Tuple[bool, Optional[str], Dict]:
        """
        Solve the given problem using multi-agent approach.

        Args:
            problem_statement: The problem description

        Returns:
            Tuple of (success, optimal_code, metadata)
        """
        metadata = {
            'attempts': 0,
            'test_cases_generated': False,
            'brute_force_generated': False,
            'brute_force_executed': False,
            'optimal_solution_found': False,
            'errors': [],
            'optimal_attempts': [],  # Store all attempts with details
            'custom_test_used': False,
            'web_search_performed': False,
            'web_hints': None
        }

        # Check for custom test input
        custom_test_path = self.config.get('execution', {}).get('custom_test_input')
        
        if custom_test_path and os.path.exists(custom_test_path):
            # Use custom test input
            print("=" * 80)
            print("STEP 1: Using custom test input...")
            print("=" * 80)
            
            try:
                # Read custom test input
                with open(custom_test_path, 'r', encoding='utf-8') as f:
                    test_cases = f.read()
                
                # Write to workspace
                with open(self.files['test_inputs'], 'w', encoding='utf-8') as f:
                    f.write(test_cases)
                
                # Parse T for logging
                try:
                    first_line = test_cases.splitlines()[0].strip()
                    t_count = int(first_line)
                    print(f"✓ Loaded {t_count} custom test cases from: {custom_test_path}")
                except Exception:
                    print(f"✓ Loaded custom test cases from: {custom_test_path}")
                
                metadata['test_cases_generated'] = True
                metadata['custom_test_used'] = True
                print(f"✓ Test cases copied to: {self.files['test_inputs']}\n")
            except Exception as e:
                error = f"Failed to load custom test input: {str(e)}"
                metadata['errors'].append(error)
                print(f"✗ {error}\n")
                return False, None, metadata
        else:
            # Auto-generate test cases with TesterAgent
            print("=" * 80)
            print("STEP 1: Generating test cases...")
            print("=" * 80)

            try:
                with ProgressIndicator("Generating small + adversarial test cases with TesterAgent"):
                    # Prefer combined generation if available
                    if hasattr(self.tester_agent, 'generate_combined_test_cases'):
                        test_cases = self.tester_agent.generate_combined_test_cases(problem_statement)
                    else:
                        test_cases = self.tester_agent.generate_test_cases(problem_statement)

                # Write to input file
                with open(self.files['test_inputs'], 'w') as f:
                    f.write(test_cases)

                # Attempt to parse T for logging
                try:
                    first_line = test_cases.splitlines()[0].strip()
                    t_count = int(first_line)
                    print(f"✓ Generated {t_count} test cases (small + adversarial)")
                except Exception:
                    print("✓ Generated test cases (could not parse T header)")

                metadata['test_cases_generated'] = True
                print(f"✓ Test cases saved to: {self.files['test_inputs']}\n")
            except Exception as e:
                error = f"Failed to generate test cases: {str(e)}"
                metadata['errors'].append(error)
                print(f"✗ {error}\n")
                return False, None, metadata

        # Step 1.5: Web search is deferred until after two failed optimal attempts
        web_hints = None
        enable_web_search = self.config.get('execution', {}).get('enable_web_search', True)
        web_search_after_attempts = 2  # Deferred trigger threshold

        print("=" * 80)
        print("STEP 2: Generating brute force solution...")
        print("=" * 80)

        try:
            with ProgressIndicator("Generating brute force solution with BruteAgent"):
                brute_code = self.brute_agent.generate_solution(problem_statement)
            with open(self.files['brute_solution'], 'w') as f:
                f.write(brute_code)
            metadata['brute_force_generated'] = True
            print(f"✓ Brute force solution saved to: {self.files['brute_solution']}\n")
        except Exception as e:
            error = f"Failed to generate brute force solution: {str(e)}"
            metadata['errors'].append(error)
            print(f"✗ {error}\n")
            return False, None, metadata

        print("=" * 80)
        print("STEP 3: Executing brute force solution...")
        print("=" * 80)

        success, error = self.executor.execute(
            self.files['brute_solution'],
            self.files['test_inputs'],
            self.files['brute_outputs']
        )

        if not success:
            error_msg = f"Brute force execution failed: {error}"
            metadata['errors'].append(error_msg)
            print(f"✗ {error_msg}\n")
            return False, None, metadata

        metadata['brute_force_executed'] = True
        print(f"✓ Brute force outputs saved to: {self.files['brute_outputs']}\n")

        print("=" * 80)
        print("STEP 4: Generating and testing optimal solution...")
        print("=" * 80)

        feedback = None
        optimal_code = None

        for attempt in range(1, self.max_attempts + 1):
            metadata['attempts'] = attempt
            print(f"\n--- Attempt {attempt}/{self.max_attempts} ---")

            attempt_data = {
                'attempt_number': attempt,
                'timestamp': time.time(),
                'code': None,
                'verdict': None,
                'error_message': None,
                'execution_success': False,
                'output_match': False,
                'output_diff': None
            }

            try:
                with ProgressIndicator(f"Generating optimal solution (attempt {attempt}/{self.max_attempts})"):
                    # Include web hints if they were fetched after earlier failed attempts
                    if web_hints:
                        enhanced_problem = f"{problem_statement}\n\n{web_hints}"
                        optimal_code = self.optimal_agent.generate_solution(
                            enhanced_problem,
                            feedback=feedback,
                            attempt=attempt
                        )
                    else:
                        # Normal generation with feedback
                        optimal_code = self.optimal_agent.generate_solution(
                            problem_statement,
                            feedback=feedback,
                            attempt=attempt
                        )

                attempt_data['code'] = optimal_code

                # Save this attempt separately
                attempt_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}.py')
                with open(attempt_file, 'w') as f:
                    f.write(optimal_code)

                # Also update the main optimal solution file
                with open(self.files['optimal_solution'], 'w') as f:
                    f.write(optimal_code)

                print(f"✓ Generated optimal solution")

            except Exception as e:
                error = f"Failed to generate optimal solution: {str(e)}"
                attempt_data['verdict'] = 'Generation Failed'
                attempt_data['error_message'] = str(e)
                metadata['errors'].append(error)
                metadata['optimal_attempts'].append(attempt_data)
                print(f"✗ {error}")
                continue

            # ==================== PRE-EXECUTION VALIDATION ====================
            print("\n--- Pre-Execution Validation ---")
            
            # 1. Quick syntactic check
            with ProgressIndicator("Running quick code checks"):
                quick_check_result = self.validator_agent.quick_check(optimal_code)
            
            if not quick_check_result['passed']:
                print(f"⚠️ Quick check warnings:")
                for issue in quick_check_result.get('issues', []):
                    print(f"  - {issue}")
            else:
                print(f"✓ Quick checks passed")
            
            # 2. Quick complexity estimate
            with ProgressIndicator("Estimating complexity"):
                complexity_est = self.complexity_agent.quick_complexity_estimate(optimal_code)
            
            print(f"✓ Estimated time: {complexity_est['time_complexity']}")
            print(f"✓ Estimated space: {complexity_est['space_complexity']}")
            
            if complexity_est['max_loop_depth'] >= 3:
                print(f"⚠️ Warning: High loop nesting depth ({complexity_est['max_loop_depth']})")
            
            # 3. Deep complexity analysis
            with ProgressIndicator("Analyzing complexity against constraints"):
                complexity_analysis = self.complexity_agent.analyze_complexity(optimal_code, problem_statement)
            
            print(f"✓ Time complexity: {complexity_analysis['time_complexity']}")
            print(f"✓ Space complexity: {complexity_analysis['space_complexity']}")
            
            if not complexity_analysis['will_pass_time']:
                print(f"⚠️ WARNING: Solution may TLE (Time Limit Exceeded)")
                for opt in complexity_analysis.get('optimizations', []):
                    print(f"  Suggestion: {opt}")
            
            if not complexity_analysis['will_pass_space']:
                print(f"⚠️ WARNING: Solution may MLE (Memory Limit Exceeded)")
            
            # 4. Deep logical validation
            with ProgressIndicator("Validating logic and edge cases"):
                validation_result = self.validator_agent.validate_logic(optimal_code, problem_statement)
            
            if not validation_result['passed']:
                print(f"⚠️ Logic validation found issues (confidence: {validation_result.get('confidence', 0):.1%}):")
                for issue in validation_result.get('issues', []):
                    print(f"  - {issue}")
                for suggestion in validation_result.get('suggestions', []):
                    print(f"  → {suggestion}")
            else:
                print(f"✓ Logic validation passed (confidence: {validation_result.get('confidence', 0):.1%})")
            
            # Store validation metadata
            attempt_data['validation'] = {
                'quick_check': quick_check_result,
                'complexity_estimate': complexity_est,
                'complexity_analysis': complexity_analysis,
                'logic_validation': validation_result
            }
            
            # Provide combined feedback if critical issues found
            critical_issues = []
            if not quick_check_result['passed'] and quick_check_result.get('severity') == 'critical':
                critical_issues.extend(quick_check_result.get('issues', []))
            if not complexity_analysis['will_pass']:
                critical_issues.append(f"Complexity issue: {complexity_analysis['time_complexity']}")
            if not validation_result['passed'] and validation_result.get('confidence', 0) > 0.7:
                critical_issues.extend(validation_result.get('issues', []))
            
            if critical_issues and attempt < self.max_attempts:
                print(f"\n⚠️ Critical issues detected. Consider fixing before execution.")
                validation_feedback = "Pre-execution validation found critical issues:\n\n"
                for issue in critical_issues:
                    validation_feedback += f"- {issue}\n"
                
                if complexity_analysis.get('optimizations'):
                    validation_feedback += "\nOptimization suggestions:\n"
                    for opt in complexity_analysis.get('optimizations', []):
                        validation_feedback += f"- {opt}\n"
                
                if validation_result.get('suggestions'):
                    validation_feedback += "\nLogic improvements:\n"
                    for sugg in validation_result.get('suggestions', []):
                        validation_feedback += f"- {sugg}\n"
                
                # Let user decide whether to proceed or regenerate
                # For now, proceed with execution but pass feedback for next iteration
                feedback = validation_feedback + "\n\n" + (feedback or "")
            
            print("=" * 60)
            # ==================== END VALIDATION ====================

            # Execute optimal solution
            attempt_output_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}_output.txt')
            success, error = self.executor.execute(
                self.files['optimal_solution'],
                self.files['test_inputs'],
                attempt_output_file
            )

            # Also update main output file
            if success:
                with open(self.files['optimal_outputs'], 'w') as f_out:
                    with open(attempt_output_file, 'r') as f_in:
                        f_out.write(f_in.read())

            if not success:
                print(f"✗ Execution failed: {error}")
                attempt_data['verdict'] = 'Runtime Error'
                attempt_data['error_message'] = error
                attempt_data['execution_success'] = False
                metadata['optimal_attempts'].append(attempt_data)
                feedback = f"Your solution failed to execute:\n{error}\n\nPlease fix the errors."
                metadata['errors'].append(f"Attempt {attempt}: Execution failed - {error}")
                # Trigger web search after N failed attempts (once)
                if enable_web_search and not metadata.get('web_search_performed') and attempt >= web_search_after_attempts:
                    print("\n" + "=" * 80)
                    print("WEB SEARCH: Fetching algorithm hints after repeated failures...")
                    print("=" * 80)
                    try:
                        with ProgressIndicator("Searching for algorithm hints with WebSearchAgent"):
                            search_results = self.web_search_agent.search_algorithm_hints(problem_statement)
                            if search_results:
                                web_hints = self.web_search_agent.extract_hints(search_results)
                                metadata['web_search_performed'] = True
                                metadata['web_hints'] = web_hints
                                print(f"✓ Found {len(search_results)} relevant resources")
                                print(f"✓ Algorithm hints will be provided to subsequent attempts\n")
                            else:
                                print("✓ No relevant algorithm hints found (will proceed normally)\n")
                    except Exception as e:
                        print(f"⚠ Web search failed: {str(e)} (continuing without hints)\n")
                continue

            attempt_data['execution_success'] = True
            print(f"✓ Execution successful")

            # Compare outputs
            if self.comparator.compare(self.files['brute_outputs'], attempt_output_file):
                print(f"✓ Outputs match! Solution found in {attempt} attempt(s)")
                attempt_data['verdict'] = 'Accepted'
                attempt_data['output_match'] = True
                metadata['optimal_attempts'].append(attempt_data)
                metadata['optimal_solution_found'] = True
                print("\n" + "=" * 80)
                print("SUCCESS: Optimal solution found!")
                print("=" * 80)

                # Generate results JSON for viewer
                self._generate_results_json(problem_statement, metadata)

                return True, optimal_code, metadata
            else:
                diff = self.comparator.get_diff_summary(
                    self.files['brute_outputs'],
                    attempt_output_file
                )
                print(f"✗ Outputs don't match")
                print(f"Difference: {diff[:200]}...")
                
                # Use debugger agent to add instrumentation and analyze
                print(f"\n🔍 Running debug analysis...")
                
                try:
                    # Read test input and expected output
                    with open(self.files['test_inputs'], 'r') as f:
                        test_input = f.read()
                    with open(self.files['brute_outputs'], 'r') as f:
                        expected_output = f.read()
                    with open(attempt_output_file, 'r') as f:
                        actual_output = f.read()
                    
                    # Add debug instrumentation
                    with ProgressIndicator("Adding debug instrumentation"):
                        debug_code = self.debugger_agent.add_debug_instrumentation(
                            optimal_code,
                            test_input,
                            expected_output,
                            actual_output,
                            diff
                        )
                    print("✓ Debug instrumentation added")
                    
                    # Save and execute debug version
                    debug_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}_debug.py')
                    debug_output_file = os.path.join(self.workspace, f'optimal_attempt_{attempt}_debug_output.txt')
                    
                    with open(debug_file, 'w') as f:
                        f.write(debug_code)
                    print(f"✓ Saved instrumented code to: {os.path.basename(debug_file)}")
                    
                    # Execute with debug output
                    with ProgressIndicator("Executing instrumented code"):
                        debug_result = self.executor.execute_with_debug(
                            debug_file,
                            self.files['test_inputs'],
                            debug_output_file
                        )
                    
                    if debug_result['success'] and debug_result['stderr']:
                        print(f"✓ Execution successful")
                        print(f"✓ Debug output captured ({len(debug_result['stderr'])} chars)")
                        
                        # Analyze debug output
                        with ProgressIndicator("Analyzing debug trace"):
                            analysis = self.debugger_agent.analyze_debug_output(
                                debug_result['stderr'],
                                expected_output,
                                actual_output
                            )
                        
                        print(f"\n💡 Debug Analysis:")
                        print(f"   {analysis}\n")
                        
                        # Enhanced feedback with debug analysis
                        feedback = f"""Your solution produced incorrect output.

DIFF:
{diff}

DEBUG ANALYSIS:
{analysis}

DEBUG OUTPUT (first 500 chars):
{debug_result['stderr'][:500]}

Please fix the logic based on this analysis."""
                    else:
                        print(f"⚠️  Debug execution failed or no debug output captured")
                        feedback = f"Your solution produced incorrect output:\n{diff}\n\nPlease fix the logic."
                        
                except Exception as e:
                    print(f"✗ Debug analysis failed: {str(e)}")
                    feedback = f"Your solution produced incorrect output:\n{diff}\n\nPlease fix the logic."
                
                attempt_data['verdict'] = 'Wrong Answer'
                attempt_data['output_match'] = False
                attempt_data['output_diff'] = diff
                metadata['optimal_attempts'].append(attempt_data)
                metadata['errors'].append(f"Attempt {attempt}: Output mismatch")

                # Trigger web search after N failed attempts (once)
                if enable_web_search and not metadata.get('web_search_performed') and attempt >= web_search_after_attempts:
                    print("\n" + "=" * 80)
                    print("WEB SEARCH: Fetching algorithm hints after repeated failures...")
                    print("=" * 80)
                    try:
                        with ProgressIndicator("Searching for algorithm hints with WebSearchAgent"):
                            search_results = self.web_search_agent.search_algorithm_hints(problem_statement)
                            if search_results:
                                web_hints = self.web_search_agent.extract_hints(search_results)
                                metadata['web_search_performed'] = True
                                metadata['web_hints'] = web_hints
                                print(f"✓ Found {len(search_results)} relevant resources")
                                print(f"✓ Algorithm hints will be provided to subsequent attempts\n")
                            else:
                                print("✓ No relevant algorithm hints found (will proceed normally)\n")
                    except Exception as e:
                        print(f"⚠ Web search failed: {str(e)} (continuing without hints)\n")

        print("\n" + "=" * 80)
        print(f"FAILED: Could not find correct solution in {self.max_attempts} attempts")
        print("=" * 80)

        # Generate results JSON even on failure
        self._generate_results_json(problem_statement, metadata)

        return False, optimal_code, metadata

    def _generate_results_json(self, problem_statement: str, metadata: Dict):
        """Generate results.json for the web viewer."""
        # Read all necessary files
        test_input = ""
        brute_code = ""
        brute_output = ""

        try:
            with open(self.files['test_inputs'], 'r') as f:
                test_input = f.read()
        except:
            pass

        try:
            with open(self.files['brute_solution'], 'r') as f:
                brute_code = f.read()
        except:
            pass

        try:
            with open(self.files['brute_outputs'], 'r') as f:
                brute_output = f.read()
        except:
            pass

        results = {
            'problem_statement': problem_statement,
            'test_input': test_input,
            'test_output': brute_output,
            'brute_force_code': brute_code,
            'optimal_attempts': metadata['optimal_attempts'],
            'success': metadata['optimal_solution_found'],
            'total_attempts': metadata['attempts'],
            'has_validation_data': any('validation' in attempt for attempt in metadata['optimal_attempts'])
        }

        results_file = os.path.join(self.workspace, 'results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✓ Results saved to: {results_file}")
        print("\n" + "=" * 80)
        print("📊 VIEW RESULTS IN WEB BROWSER")
        print("=" * 80)
        print("\nTo view the beautiful HTML report, run:")
        print("\n  python -m http.server 8000")
        print("\nThen open: http://localhost:8000/viewer.html")
        print("\n(HTTP server needed to avoid CORS restrictions)")
        print("=" * 80)
