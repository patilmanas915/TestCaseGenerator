import csv
import json
import os
from datetime import datetime
from config import Config
from gemini_client import GeminiClient
import logging

# Using pandas-free implementation for Render compatibility
PANDAS_AVAILABLE = False

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
        all_test_cases = []
        for i, feature in enumerate(features):
            try:
                if progress_callback:
                    progress_callback(f"Generating test cases for feature {i+1}/{len(features)}: {feature.get('name', 'Unknown')}")
                
                test_cases = self.gemini_client.generate_test_cases(feature)
                
                if test_cases and 'test_cases' in test_cases:
                    for test_case in test_cases['test_cases']:
                        test_case['feature_name'] = feature.get('name', 'Unknown')
                        test_case['feature_id'] = feature.get('id', f'feature_{i+1}')
                        all_test_cases.append(test_case)
                        
            except Exception as e:
                logger.error(f"Error generating test cases for feature {feature.get('name', 'Unknown')}: {e}")
                continue
        
        self.all_test_cases = all_test_cases
        logger.info(f"Generated {len(all_test_cases)} total test cases")
        
        if progress_callback:
            progress_callback(f"Generated {len(all_test_cases)} test cases successfully!")
        
        return True, f"Successfully generated {len(all_test_cases)} test cases"
    
    def get_statistics(self):
        """Get statistics about generated test cases"""
        if not self.all_test_cases:
            return {}
        
        stats = {
            'total_test_cases': len(self.all_test_cases),
            'positive_test_cases': 0,
            'negative_test_cases': 0,
            'boundary_test_cases': 0,
            'edge_test_cases': 0,
            'features_covered': len(set([tc.get('feature_name', '') for tc in self.all_test_cases]))
        }
        
        for test_case in self.all_test_cases:
            test_type = test_case.get('type', '').lower()
            if 'positive' in test_type:
                stats['positive_test_cases'] += 1
            elif 'negative' in test_type:
                stats['negative_test_cases'] += 1
            elif 'boundary' in test_type:
                stats['boundary_test_cases'] += 1
            elif 'edge' in test_type:
                stats['edge_test_cases'] += 1
        
        return stats
    
    def export_to_csv(self, download_folder):
        """Export test cases to CSV using native Python (pandas fallback)"""
        if not self.all_test_cases:
            return None, "No test cases to export"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_testcases_{timestamp}.csv"
        filepath = os.path.join(download_folder, filename)
        
        try:
            if PANDAS_AVAILABLE:
                # Use pandas if available
                df = pd.DataFrame(self.all_test_cases)
                df.to_csv(filepath, index=False)
            else:
                # Use native Python CSV
                self._export_csv_native(filepath)
            
            return filename, "Test cases exported successfully"
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            return None, f"Error exporting CSV: {str(e)}"
    
    def _export_csv_native(self, filepath):
        """Export CSV using native Python"""
        if not self.all_test_cases:
            return
        
        # Get all unique field names
        fieldnames = set()
        for test_case in self.all_test_cases:
            fieldnames.update(test_case.keys())
        
        fieldnames = sorted(list(fieldnames))
        
        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.all_test_cases)
    
    def export_to_excel(self, download_folder):
        """Export test cases to Excel"""
        if not self.all_test_cases:
            return None, "No test cases to export"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_testcases_{timestamp}.xlsx"
        filepath = os.path.join(download_folder, filename)
        
        try:
            if PANDAS_AVAILABLE:
                # Use pandas for Excel export
                df = pd.DataFrame(self.all_test_cases)
                with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Test Cases', index=False)
                    
                    # Add statistics sheet
                    stats = self.get_statistics()
                    stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            else:
                # Use openpyxl directly
                from openpyxl import Workbook
                wb = Workbook()
                ws = wb.active
                ws.title = "Test Cases"
                
                # Get headers
                if self.all_test_cases:
                    headers = sorted(self.all_test_cases[0].keys())
                    ws.append(headers)
                    
                    # Add data
                    for test_case in self.all_test_cases:
                        row = [test_case.get(header, '') for header in headers]
                        ws.append(row)
                
                # Add statistics sheet
                stats_ws = wb.create_sheet("Statistics")
                stats = self.get_statistics()
                stats_ws.append(["Metric", "Value"])
                for metric, value in stats.items():
                    stats_ws.append([metric, value])
                
                wb.save(filepath)
            
            return filename, "Test cases exported to Excel successfully"
        except Exception as e:
            logger.error(f"Error exporting Excel: {e}")
            return None, f"Error exporting Excel: {str(e)}"
