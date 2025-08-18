import pandas as pd
import os
from datetime import datetime
from config import Config
from gemini_client import GeminiClient
import json
import logging

logger = logging.getLogger(__name__)

class TestCaseGenerator:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.all_test_cases = []
        
    def process_frd_document(self, frd_content, progress_callback=None):
        """Process FRD document and generate test cases"""
        
        logger.info("Extracting features from FRD document...")
        if progress_callback:
            progress_callback("Extracting features from FRD document...")
            
        features_data = self.gemini_client.extract_features_from_frd(frd_content)
        
        if not features_data or 'features' not in features_data:
            logger.error("Failed to extract features from FRD")
            return False, "Failed to extract features from FRD document"
            
        features = features_data['features']
        logger.info(f"Found {len(features)} features")
        
        if progress_callback:
            progress_callback(f"Found {len(features)} features. Generating test cases...")
        
        # Generate test cases for each feature
        for idx, feature in enumerate(features, 1):
            logger.info(f"Generating test cases for Feature {idx}/{len(features)}: {feature.get('feature_name')}")
            
            if progress_callback:
                progress_callback(f"Generating test cases for feature {idx}/{len(features)}: {feature.get('feature_name')}")
            
            test_cases_data = self.gemini_client.generate_test_cases_for_feature(feature)
            
            if test_cases_data and 'test_cases' in test_cases_data:
                self.all_test_cases.extend(test_cases_data['test_cases'])
                logger.info(f"Generated {len(test_cases_data['test_cases'])} test cases")
            else:
                logger.warning(f"Failed to generate test cases for {feature.get('feature_name')}")
            
            # Add delay to respect API rate limits
            self.gemini_client.rate_limit_delay()
        
        return True, f"Successfully generated {len(self.all_test_cases)} test cases"
    
    def save_to_csv(self, filename=None):
        """Save all generated test cases to Excel file in few-shot format with proper formatting"""
        
        if not self.all_test_cases:
            logger.error("No test cases to save")
            return None, "No test cases to save"
        
        # Prepare data for Excel
        csv_data = []
        
        for idx, test_case in enumerate(self.all_test_cases, 1):
            # Use the formatted test steps from few-shot prompting
            test_steps_formatted = test_case.get('test_steps_formatted', '')
            
            # If not available, convert test steps list to numbered string
            if not test_steps_formatted and test_case.get('test_steps'):
                test_steps_formatted = '\n'.join([
                    f"{i+1}. {step}" 
                    for i, step in enumerate(test_case.get('test_steps', []))
                ])
            
            # Clean and format text fields to avoid Excel formatting issues
            def clean_text(text):
                if not text:
                    return ""
                # Remove extra whitespace and ensure proper line breaks
                cleaned = str(text).strip()
                # Replace multiple spaces with single space
                cleaned = ' '.join(cleaned.split())
                return cleaned
            
            csv_row = {
                'Test_Case_ID': test_case.get('test_case_id', f'TC{idx:03d}'),
                'Test_Case_Name': clean_text(test_case.get('test_case_name', '')),
                'Feature_ID': clean_text(test_case.get('feature_id', '')),
                'Feature_Name': clean_text(test_case.get('feature_name', '')),
                'Module': clean_text(test_case.get('module', '')),
                'Test_Type': clean_text(test_case.get('test_type', '')),
                'Priority': clean_text(test_case.get('priority', '')),
                'Category': clean_text(test_case.get('category', '')),
                'Gap_Coverage': clean_text(test_case.get('gap_coverage', '')),
                'Preconditions': clean_text(test_case.get('preconditions', '')),
                'Test_Steps_Few_Shot_Format': test_steps_formatted,
                'Test_Data': clean_text(test_case.get('test_data', '')),
                'Expected_Result': clean_text(test_case.get('expected_result', '')),
                'FRD_Reference': clean_text(test_case.get('frd_reference', '')),
                'Generated_On': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            csv_data.append(csv_row)
        
        # Create DataFrame
        df = pd.DataFrame(csv_data)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'generated_testcases_{timestamp}.xlsx'
        else:
            # Ensure .xlsx extension
            if not filename.endswith('.xlsx'):
                filename = filename.replace('.csv', '.xlsx')
        
        # Ensure download directory exists
        os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
        
        # Save to Excel with proper formatting
        output_path = os.path.join(Config.DOWNLOAD_FOLDER, filename)
        
        try:
            # Save to Excel with auto-adjusted column widths
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Test_Cases', index=False)
                
                # Get the workbook and worksheet
                worksheet = writer.sheets['Test_Cases']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        if cell.value:
                            cell_length = len(str(cell.value))
                            if cell_length > max_length:
                                max_length = cell_length
                    
                    # Set column width (with some padding)
                    adjusted_width = min(max_length + 2, 50)  # Max width of 50
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # Set specific column widths for better readability
                worksheet.column_dimensions['K'].width = 80  # Test Steps column
                worksheet.column_dimensions['M'].width = 40  # Expected Result column
                worksheet.column_dimensions['N'].width = 50  # FRD Reference column
                worksheet.column_dimensions['I'].width = 45  # Gap Coverage column
                
                # Add header formatting
                from openpyxl.styles import Font, PatternFill, Alignment
                
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                
                # Set text wrapping for test steps column
                for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=11, max_col=11):
                    for cell in row:
                        cell.alignment = Alignment(wrap_text=True, vertical="top")
        
        except ImportError:
            logger.error("openpyxl not available, cannot create Excel file")
            return None, "Excel library not available"
        except Exception as e:
            logger.error(f"Could not create Excel file: {e}")
            return None, f"Could not create Excel file: {e}"
        
        logger.info(f"Successfully saved {len(csv_data)} test cases to {output_path}")
        return output_path, f"Successfully saved {len(csv_data)} test cases in Excel format"
    
    def get_summary_stats(self):
        """Generate summary statistics of generated test cases"""
        
        if not self.all_test_cases:
            return {}
        
        df = pd.DataFrame(self.all_test_cases)
        
        stats = {
            'total_test_cases': len(self.all_test_cases),
            'test_types': {},
            'priorities': {},
            'features': {},
            'modules': {}
        }
        
        if 'test_type' in df.columns:
            stats['test_types'] = df['test_type'].value_counts().to_dict()
        
        if 'priority' in df.columns:
            stats['priorities'] = df['priority'].value_counts().to_dict()
        
        if 'feature_name' in df.columns:
            stats['features'] = df['feature_name'].value_counts().to_dict()
            
        if 'module' in df.columns:
            stats['modules'] = df['module'].value_counts().to_dict()
        
        return stats
