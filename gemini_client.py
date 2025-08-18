import google.generativeai as genai
from config import Config
import json
import time
import logging
import csv
import os

# Try to import pandas, fallback to native Python if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
            
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Load few-shot examples and key-value pairs
        self.few_shot_examples = self.load_few_shot_examples()
        self.key_value_pairs = self.load_key_value_pairs()
    
    def load_few_shot_examples(self):
        """Load few-shot examples from CSV"""
        try:
            csv_path = 'Few_Shot_Prompting_Rib.csv'
            if os.path.exists(csv_path):
                if PANDAS_AVAILABLE:
                    df = pd.read_csv(csv_path)
                    return df.to_dict('records')
                else:
                    # Use native Python CSV reader
                    with open(csv_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        return list(reader)
            else:
                logger.warning("Few_Shot_Prompting_Rib.csv not found, using default examples")
                return []
        except Exception as e:
            logger.error(f"Error loading few-shot examples: {e}")
            return []
    
    def load_key_value_pairs(self):
        """Load key-value pairs from CSV"""
        try:
            csv_path = 'Key_Value_Pair_.csv'
            if os.path.exists(csv_path):
                if PANDAS_AVAILABLE:
                    df = pd.read_csv(csv_path)
                    return df.to_dict('records')
                else:
                    # Use native Python CSV reader
                    with open(csv_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        return list(reader)
            else:
                logger.warning("Key_Value_Pair_.csv not found")
                return []
        except Exception as e:
            logger.error(f"Error loading key-value pairs: {e}")
            return []
        
    def extract_features_from_frd(self, frd_content):
        """Extract features from FRD document and return as JSON using few-shot prompting"""
        
        # Build few-shot examples
        few_shot_context = ""
        if self.few_shot_examples:
            few_shot_context = "\n\nFew-shot Examples:\n"
            for i, example in enumerate(self.few_shot_examples[:3], 1):  # Use first 3 examples
                few_shot_context += f"\nExample {i}:\nInput: {example.get('Input', '')}\nOutput: {example.get('Output', '')}\n"
        
        prompt = f"""
        You are an expert test case generator. Analyze the following Functional Requirements Document (FRD) and extract all features/functionalities in the exact format shown in the examples.
        
        {few_shot_context}
        
        Based on the above examples, analyze the FRD content and extract features in JSON format:
        
        {{
            "features": [
                {{
                    "feature_id": "F001",
                    "feature_name": "Feature Name",
                    "description": "Detailed description from FRD",
                    "requirements": ["requirement 1", "requirement 2"],
                    "acceptance_criteria": ["criteria 1", "criteria 2"],
                    "priority": "High/Medium/Low",
                    "module": "Module name",
                    "frd_line": "Original FRD line that describes this feature"
                }}
            ]
        }}
        
        FRD Content:
        {frd_content[:50000]}  # Limit content to avoid token limits
        
        Important: 
        1. Return only valid JSON format
        2. Extract all distinct features mentioned in the document
        3. Follow the pattern from the few-shot examples
        4. Include the original FRD line for each feature
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean response text and parse JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
                
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Response text: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return None
    
    def generate_test_cases_for_feature(self, feature_data):
        """Generate test cases for a specific feature using few-shot prompting and key-value pairs"""
        
        # Build few-shot examples context
        few_shot_context = ""
        if self.few_shot_examples:
            few_shot_context = "\n\nFew-shot Examples for Test Case Generation:\n"
            for i, example in enumerate(self.few_shot_examples[:5], 1):  # Use first 5 examples
                few_shot_context += f"\nExample {i}:\nFRD Input: {example.get('Input', '')}\nExpected Test Case Output: {example.get('Output', '')}\n"
        
        # Build key-value pairs context
        key_value_context = ""
        if self.key_value_pairs:
            key_value_context = "\n\nKey-Value Pairs for Reference:\n"
            for kv in self.key_value_pairs[:10]:  # Use first 10 key-value pairs
                key_value_context += f"\nFeature: {kv.get('Feature Name', '')}"
                key_value_context += f"\nScenario: {kv.get('Scenario_Name', '')}"
                key_value_context += f"\nDescription: {kv.get('Scenario_Description', '')}"
                key_value_context += f"\nSteps: {kv.get('Testing_Steps', '')}\n"
        
        prompt = f"""
        You are an expert test case generator. Based on the feature information provided and the few-shot examples, generate comprehensive test cases in the EXACT format shown in the examples.
        
        {few_shot_context}
        
        {key_value_context}
        
        Feature Information to Generate Test Cases For:
        - Feature ID: {feature_data.get('feature_id')}
        - Feature Name: {feature_data.get('feature_name')}
        - Description: {feature_data.get('description')}
        - FRD Line: {feature_data.get('frd_line', '')}
        - Requirements: {feature_data.get('requirements')}
        - Acceptance Criteria: {feature_data.get('acceptance_criteria')}
        - Module: {feature_data.get('module')}
        
        Generate comprehensive test cases covering ALL of the following categories:
        
        1. POSITIVE TEST CASES:
        - Happy path scenarios
        - Valid input scenarios
        - Expected functionality validation
        
        2. NEGATIVE TEST CASES:
        - Invalid input scenarios
        - Error condition handling
        - Boundary violations
        
        3. EDGE CASES:
        - Boundary value testing
        - Extreme scenarios
        - Unusual input combinations
        
        4. ADVANCED COVERAGE (Include these critical gaps):
        - Conflict resolution scenarios and detailed messaging validation
        - Error recovery and retry mechanisms after failures
        - Fallback behavior when primary options fail
        - Multi-object creation scenarios (multiple curves = multiple objects)
        - Backward compatibility with existing features
        - Integration testing with other features
        - Performance under extreme conditions
        - Data validation and format checking
        - User workflow interruption and resumption
        - System state consistency after operations
        
        5. SPECIFIC GAP COVERAGE:
        - Conflict Solver Detailed Messaging: Validate 3-line format (creation conflict, switch to partial, list options to remove)
        - Editing after Conflict: Test user can remove options and retry Complete Result after failure
        - Fallback Rule Testing: Validate "To Closest → By Delta" fallback sequence
        - Multi-curve Validation: Test that 4 curves = 4 objects, or 1 sketch = 1 object
        - Backward Compatibility: Ensure old features remain unaffected by new changes
        
        Use this exact format for each test case:
        "The following test scenario for the [Feature Name] feature is derived from the corresponding line in the FRD document:
        
        1. [Step 1]
        2. [Step 2]
        3. [Step 3]
        ...
        
        Exp: [Expected Result]"
        
        Return response in JSON format:
        {{
            "test_cases": [
                {{
                    "test_case_id": "TC001",
                    "test_case_name": "Test case name",
                    "feature_id": "{feature_data.get('feature_id')}",
                    "feature_name": "{feature_data.get('feature_name')}",
                    "module": "{feature_data.get('module')}",
                    "test_type": "Positive/Negative/Boundary/Edge/Conflict/Fallback/Integration/Compatibility",
                    "priority": "High/Medium/Low",
                    "preconditions": "Prerequisites for test execution",
                    "test_steps_formatted": "The following test scenario for the [Feature] feature is derived from the corresponding line in the FRD document:\n\n1. Step 1\n2. Step 2\n...\n\nExp: Expected result",
                    "test_data": "Required test data",
                    "expected_result": "Expected outcome",
                    "category": "Functional/Non-functional/Integration/Compatibility/Performance",
                    "frd_reference": "{feature_data.get('frd_line', '')}",
                    "gap_coverage": "Specific gap or advanced scenario this test covers"
                }}
            ]
        }}
        
        Generate 15-25 comprehensive test cases covering ALL categories above, ensuring complete coverage of gaps and edge cases.
        IMPORTANT: Follow the exact format from the few-shot examples in the test_steps_formatted field.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
                
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for feature {feature_data.get('feature_name')}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error generating test cases for feature {feature_data.get('feature_name')}: {str(e)}")
            return None
    
    def rate_limit_delay(self):
        """Add delay to respect API rate limits"""
        time.sleep(1)
