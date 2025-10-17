#!/usr/bin/env python3
"""
Generate bug report from test results
"""
import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

def load_test_results():
    """Load all test results"""
    results = {}
    
    # Load functional test results
    result_files = [
        'reports/functional_results.json',
        'reports/device_results.json',
        'reports/smoke_results.json',
        'reports/regression_results.json',
        'reports/desktop_results.json',
        'reports/mobile_results.json',
        'reports/tablet_results.json'
    ]
    
    for file_path in result_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    results[file_path] = data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading {file_path}: {e}")
    
    return results

def extract_failed_tests(results):
    """Extract failed test cases from results"""
    failed_tests = []
    
    for file_path, data in results.items():
        if 'tests' in data:
            for test in data['tests']:
                if test.get('outcome') == 'failed':
                    failed_tests.append({
                        'Test File': file_path,
                        'Test Name': test.get('nodeid', 'Unknown'),
                        'Error Message': test.get('call', {}).get('longrepr', 'No error message'),
                        'Duration': test.get('call', {}).get('duration', 0),
                        'Status': 'FAILED',
                        'Priority': determine_priority(test.get('call', {}).get('longrepr', '')),
                        'Category': categorize_bug(test.get('nodeid', '')),
                        'Severity': determine_severity(test.get('call', {}).get('longrepr', '')),
                        'Reproduction Steps': generate_reproduction_steps(test.get('nodeid', '')),
                        'Expected Result': generate_expected_result(test.get('nodeid', '')),
                        'Actual Result': test.get('call', {}).get('longrepr', 'Test failed'),
                        'Environment': 'Test Environment',
                        'Browser': extract_browser_from_test(test.get('nodeid', '')),
                        'Device': extract_device_from_test(test.get('nodeid', '')),
                        'Screenshot': f"screenshots/{test.get('nodeid', '').replace('::', '_').replace('/', '_')}_failed.png"
                    })
    
    return failed_tests

def determine_priority(error_message):
    """Determine bug priority based on error message"""
    error_lower = error_message.lower()
    
    if any(keyword in error_lower for keyword in ['critical', 'blocking', 'cannot', 'unable to']):
        return 'High'
    elif any(keyword in error_lower for keyword in ['validation', 'required', 'missing']):
        return 'Medium'
    else:
        return 'Low'

def categorize_bug(test_name):
    """Categorize bug based on test name"""
    test_lower = test_name.lower()
    
    if 'signup' in test_lower:
        return 'Signup Functionality'
    elif 'validation' in test_lower:
        return 'Input Validation'
    elif 'device' in test_lower or 'mobile' in test_lower or 'tablet' in test_lower:
        return 'Device Compatibility'
    elif 'load' in test_lower or 'performance' in test_lower:
        return 'Performance'
    else:
        return 'General'

def determine_severity(error_message):
    """Determine bug severity"""
    error_lower = error_message.lower()
    
    if any(keyword in error_lower for keyword in ['exception', 'error', 'timeout', 'crash']):
        return 'Critical'
    elif any(keyword in error_lower for keyword in ['failed', 'not working', 'broken']):
        return 'High'
    elif any(keyword in error_lower for keyword in ['warning', 'issue', 'problem']):
        return 'Medium'
    else:
        return 'Low'

def generate_reproduction_steps(test_name):
    """Generate reproduction steps based on test name"""
    test_lower = test_name.lower()
    
    if 'signup' in test_lower:
        return """1. Navigate to SwiftAssess signup page
2. Fill in the signup form with test data
3. Click the signup button
4. Observe the behavior"""
    elif 'validation' in test_lower:
        return """1. Navigate to SwiftAssess signup page
2. Enter invalid data in the form fields
3. Attempt to submit the form
4. Check for validation error messages"""
    elif 'device' in test_lower:
        return """1. Open SwiftAssess signup page on the specified device
2. Test the signup functionality
3. Check for responsive design issues
4. Verify form usability"""
    else:
        return """1. Navigate to SwiftAssess signup page
2. Perform the test scenario
3. Observe the actual behavior
4. Compare with expected behavior"""

def generate_expected_result(test_name):
    """Generate expected result based on test name"""
    test_lower = test_name.lower()
    
    if 'signup' in test_lower and 'valid' in test_lower:
        return "User should be successfully signed up and redirected to dashboard"
    elif 'validation' in test_lower:
        return "Appropriate validation error messages should be displayed"
    elif 'device' in test_lower:
        return "Page should be fully functional and responsive on the device"
    else:
        return "Test should pass without errors"

def extract_browser_from_test(test_name):
    """Extract browser from test name"""
    test_lower = test_name.lower()
    
    if 'chrome' in test_lower:
        return 'Chrome'
    elif 'firefox' in test_lower:
        return 'Firefox'
    elif 'edge' in test_lower:
        return 'Edge'
    else:
        return 'Chrome'  # Default

def extract_device_from_test(test_name):
    """Extract device from test name"""
    test_lower = test_name.lower()
    
    if 'mobile' in test_lower:
        return 'Mobile'
    elif 'tablet' in test_lower:
        return 'Tablet'
    elif 'desktop' in test_lower:
        return 'Desktop'
    else:
        return 'Desktop'  # Default

def generate_bug_report():
    """Generate comprehensive bug report"""
    print("Generating bug report...")
    
    # Load test results
    results = load_test_results()
    
    # Extract failed tests
    failed_tests = extract_failed_tests(results)
    
    if not failed_tests:
        print("No failed tests found. Generating empty bug report.")
        # Create empty report
        empty_data = [{
            'Bug ID': 'N/A',
            'Test File': 'N/A',
            'Test Name': 'No failed tests',
            'Error Message': 'All tests passed',
            'Duration': 0,
            'Status': 'PASSED',
            'Priority': 'N/A',
            'Category': 'N/A',
            'Severity': 'N/A',
            'Reproduction Steps': 'N/A',
            'Expected Result': 'N/A',
            'Actual Result': 'N/A',
            'Environment': 'Test Environment',
            'Browser': 'N/A',
            'Device': 'N/A',
            'Screenshot': 'N/A'
        }]
        
        df = pd.DataFrame(empty_data)
    else:
        # Add bug IDs
        for i, bug in enumerate(failed_tests, 1):
            bug['Bug ID'] = f'BUG-{i:03d}'
        
        df = pd.DataFrame(failed_tests)
    
    # Generate Excel report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f'reports/bug_report_{timestamp}.xlsx'
    
    try:
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Main bug report
            df.to_excel(writer, sheet_name='Bug Report', index=False)
            
            # Summary by category
            if not df.empty and 'Category' in df.columns:
                category_summary = df.groupby('Category').agg({
                    'Bug ID': 'count',
                    'Priority': lambda x: (x == 'High').sum(),
                    'Severity': lambda x: (x == 'Critical').sum()
                }).rename(columns={
                    'Bug ID': 'Total Bugs',
                    'Priority': 'High Priority',
                    'Severity': 'Critical Severity'
                })
                category_summary.to_excel(writer, sheet_name='Summary by Category')
            
            # Summary by priority
            if not df.empty and 'Priority' in df.columns:
                priority_summary = df['Priority'].value_counts()
                priority_summary.to_excel(writer, sheet_name='Summary by Priority')
            
            # Summary by severity
            if not df.empty and 'Severity' in df.columns:
                severity_summary = df['Severity'].value_counts()
                severity_summary.to_excel(writer, sheet_name='Summary by Severity')
        
        print(f"Bug report generated successfully: {excel_file}")
        
        # Generate HTML bug report
        generate_html_bug_report(df, excel_file)
        
    except Exception as e:
        print(f"Error generating bug report: {e}")

def generate_html_bug_report(df, excel_file):
    """Generate HTML bug report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SwiftAssess Bug Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #dc3545; }}
            .metric-value {{ font-size: 2em; font-weight: bold; color: #dc3545; }}
            .metric-label {{ color: #6c757d; margin-top: 5px; }}
            .bug-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            .bug-table th, .bug-table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
            .bug-table th {{ background-color: #f8f9fa; font-weight: bold; }}
            .bug-table tr:nth-child(even) {{ background-color: #f8f9fa; }}
            .priority-high {{ color: #dc3545; font-weight: bold; }}
            .priority-medium {{ color: #ffc107; font-weight: bold; }}
            .priority-low {{ color: #28a745; font-weight: bold; }}
            .severity-critical {{ color: #dc3545; font-weight: bold; }}
            .severity-high {{ color: #fd7e14; font-weight: bold; }}
            .severity-medium {{ color: #ffc107; font-weight: bold; }}
            .severity-low {{ color: #28a745; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🐛 SwiftAssess Bug Report</h1>
                <p>Test Failure Analysis & Bug Tracking</p>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="summary">
                <div class="metric-card">
                    <div class="metric-value">{len(df)}</div>
                    <div class="metric-label">Total Bugs</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(df[df['Priority'] == 'High']) if not df.empty else 0}</div>
                    <div class="metric-label">High Priority</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(df[df['Severity'] == 'Critical']) if not df.empty else 0}</div>
                    <div class="metric-label">Critical Severity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(df[df['Category'] == 'Signup Functionality']) if not df.empty else 0}</div>
                    <div class="metric-label">Signup Issues</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Bug Details</h2>
                <table class="bug-table">
                    <thead>
                        <tr>
                            <th>Bug ID</th>
                            <th>Test Name</th>
                            <th>Category</th>
                            <th>Priority</th>
                            <th>Severity</th>
                            <th>Browser</th>
                            <th>Device</th>
                            <th>Error Message</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    if not df.empty:
        for _, row in df.iterrows():
            priority_class = f"priority-{row['Priority'].lower()}" if 'Priority' in row else ""
            severity_class = f"severity-{row['Severity'].lower()}" if 'Severity' in row else ""
            
            html_content += f"""
                        <tr>
                            <td>{row.get('Bug ID', 'N/A')}</td>
                            <td>{row.get('Test Name', 'N/A')}</td>
                            <td>{row.get('Category', 'N/A')}</td>
                            <td><span class="{priority_class}">{row.get('Priority', 'N/A')}</span></td>
                            <td><span class="{severity_class}">{row.get('Severity', 'N/A')}</span></td>
                            <td>{row.get('Browser', 'N/A')}</td>
                            <td>{row.get('Device', 'N/A')}</td>
                            <td>{str(row.get('Error Message', 'N/A'))[:100]}...</td>
                        </tr>
            """
    else:
        html_content += """
                        <tr>
                            <td colspan="8" style="text-align: center; color: #28a745; font-weight: bold;">
                                🎉 No bugs found! All tests passed successfully.
                            </td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>📊 Analysis & Recommendations</h2>
                <ul>
                    <li>Review high priority bugs first</li>
                    <li>Focus on critical severity issues</li>
                    <li>Check device compatibility issues</li>
                    <li>Verify browser-specific problems</li>
                    <li>Test signup functionality thoroughly</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>SwiftAssess QA Automation - Bug Report</p>
                <p>Excel Report: <a href="{excel_file}">Download Excel Report</a></p>
            </div>
        </div>
    </body>
    </html>
    """.format(excel_file=excel_file)
    
    # Save HTML report
    html_file = f'reports/bug_report_{timestamp}.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML bug report generated: {html_file}")

if __name__ == "__main__":
    generate_bug_report()
