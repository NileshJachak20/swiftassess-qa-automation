#!/usr/bin/env python3
"""
Generate combined test report from all test results
"""
import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

def load_json_results(file_path):
    """Load JSON test results from file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        return None

def generate_combined_report():
    """Generate combined test report"""
    print("Generating combined test report...")
    
    # Load all test results
    results = {
        'functional': load_json_results('reports/functional_results.json'),
        'device': load_json_results('reports/device_results.json'),
        'smoke': load_json_results('reports/smoke_results.json'),
        'regression': load_json_results('reports/regression_results.json'),
        'desktop': load_json_results('reports/desktop_results.json'),
        'mobile': load_json_results('reports/mobile_results.json'),
        'tablet': load_json_results('reports/tablet_results.json'),
    }
    
    # Load load test results
    load_results = {}
    for test_type in ['baseline', 'stress', 'spike']:
        file_path = f'reports/{test_type}_test_results.json'
        if os.path.exists(file_path):
            load_results[test_type] = load_json_results(file_path)
    
    # Generate HTML report
    html_content = generate_html_report(results, load_results)
    
    # Save HTML report
    with open('reports/combined_test_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate Excel report
    generate_excel_report(results, load_results)
    
    print("Combined test report generated successfully!")

def generate_html_report(results, load_results):
    """Generate HTML report content"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate summary statistics
    total_tests = 0
    total_passed = 0
    total_failed = 0
    
    for test_type, result in results.items():
        if result and 'summary' in result:
            summary = result['summary']
            total_tests += summary.get('total', 0)
            total_passed += summary.get('passed', 0)
            total_failed += summary.get('failed', 0)
    
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SwiftAssess Combined Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }}
            .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
            .metric-label {{ color: #6c757d; margin-top: 5px; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #343a40; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
            .test-results {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .test-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #dee2e6; }}
            .test-card h3 {{ margin-top: 0; color: #495057; }}
            .status-passed {{ color: #28a745; font-weight: bold; }}
            .status-failed {{ color: #dc3545; font-weight: bold; }}
            .status-warning {{ color: #ffc107; font-weight: bold; }}
            .load-test {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 10px 0; }}
            .load-metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }}
            .load-metric {{ text-align: center; padding: 10px; background: white; border-radius: 4px; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 SwiftAssess QA Test Report</h1>
                <p>Comprehensive Test Results & Analysis</p>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="summary">
                <div class="metric-card">
                    <div class="metric-value">{total_tests}</div>
                    <div class="metric-label">Total Tests</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_passed}</div>
                    <div class="metric-label">Passed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_failed}</div>
                    <div class="metric-label">Failed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{pass_rate:.1f}%</div>
                    <div class="metric-label">Pass Rate</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Functional Test Results</h2>
                <div class="test-results">
    """
    
    # Add functional test results
    for test_type, result in results.items():
        if result and 'summary' in result:
            summary = result['summary']
            status = 'passed' if summary.get('failed', 0) == 0 else 'failed'
            status_class = f'status-{status}'
            
            html += f"""
                    <div class="test-card">
                        <h3>{test_type.title()} Tests</h3>
                        <p><span class="{status_class}">{summary.get('passed', 0)} passed</span> / {summary.get('total', 0)} total</p>
                        <p>Duration: {summary.get('duration', 'N/A')}</p>
                        <p>Status: <span class="{status_class}">{status.upper()}</span></p>
                    </div>
            """
    
    html += """
                </div>
            </div>
            
            <div class="section">
                <h2>⚡ Load Test Results</h2>
    """
    
    # Add load test results
    for test_type, result in load_results.items():
        if result and 'metrics' in result:
            metrics = result['metrics']
            http_reqs = metrics.get('http_reqs', {}).get('values', {})
            http_failed = metrics.get('http_req_failed', {}).get('values', {})
            duration = metrics.get('http_req_duration', {}).get('values', {})
            
            total_requests = http_reqs.get('count', 0)
            failed_requests = http_failed.get('count', 0)
            avg_duration = duration.get('avg', 0)
            p95_duration = duration.get('p95', 0)
            
            error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
            
            html += f"""
                <div class="load-test">
                    <h3>{test_type.title()} Load Test</h3>
                    <div class="load-metrics">
                        <div class="load-metric">
                            <strong>{total_requests}</strong><br>
                            <small>Total Requests</small>
                        </div>
                        <div class="load-metric">
                            <strong>{failed_requests}</strong><br>
                            <small>Failed Requests</small>
                        </div>
                        <div class="load-metric">
                            <strong>{error_rate:.1f}%</strong><br>
                            <small>Error Rate</small>
                        </div>
                        <div class="load-metric">
                            <strong>{avg_duration:.0f}ms</strong><br>
                            <small>Avg Response Time</small>
                        </div>
                        <div class="load-metric">
                            <strong>{p95_duration:.0f}ms</strong><br>
                            <small>95th Percentile</small>
                        </div>
                    </div>
                </div>
            """
    
    html += """
            </div>
            
            <div class="section">
                <h2>📈 Performance Analysis</h2>
                <div class="test-results">
                    <div class="test-card">
                        <h3>Response Time Analysis</h3>
                        <p>Average response times across all test scenarios</p>
                        <p>Target: &lt; 2 seconds for 95th percentile</p>
                    </div>
                    <div class="test-card">
                        <h3>Error Rate Analysis</h3>
                        <p>Error rates under different load conditions</p>
                        <p>Target: &lt; 1% error rate under normal load</p>
                    </div>
                    <div class="test-card">
                        <h3>Throughput Analysis</h3>
                        <p>Requests per second under various loads</p>
                        <p>Target: &gt; 100 RPS under normal conditions</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔧 Recommendations</h2>
                <ul>
                    <li>Monitor server resources during peak load</li>
                    <li>Implement caching strategies for static content</li>
                    <li>Consider load balancing for high traffic scenarios</li>
                    <li>Optimize database queries for better performance</li>
                    <li>Implement auto-scaling for traffic spikes</li>
                    <li>Add monitoring and alerting for performance metrics</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>SwiftAssess QA Automation & Load Testing</p>
                <p>Generated by automated testing pipeline</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def generate_excel_report(results, load_results):
    """Generate Excel report"""
    try:
        # Create Excel writer
        with pd.ExcelWriter('reports/combined_test_report.xlsx', engine='openpyxl') as writer:
            
            # Summary sheet
            summary_data = []
            for test_type, result in results.items():
                if result and 'summary' in result:
                    summary = result['summary']
                    summary_data.append({
                        'Test Type': test_type.title(),
                        'Total Tests': summary.get('total', 0),
                        'Passed': summary.get('passed', 0),
                        'Failed': summary.get('failed', 0),
                        'Pass Rate (%)': round((summary.get('passed', 0) / summary.get('total', 1) * 100), 2),
                        'Duration (s)': summary.get('duration', 0)
                    })
            
            if summary_data:
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Load test results sheet
            load_data = []
            for test_type, result in load_results.items():
                if result and 'metrics' in result:
                    metrics = result['metrics']
                    http_reqs = metrics.get('http_reqs', {}).get('values', {})
                    http_failed = metrics.get('http_req_failed', {}).get('values', {})
                    duration = metrics.get('http_req_duration', {}).get('values', {})
                    
                    load_data.append({
                        'Test Type': test_type.title(),
                        'Total Requests': http_reqs.get('count', 0),
                        'Failed Requests': http_failed.get('count', 0),
                        'Error Rate (%)': round((http_failed.get('count', 0) / http_reqs.get('count', 1) * 100), 2),
                        'Avg Response Time (ms)': round(duration.get('avg', 0), 2),
                        '95th Percentile (ms)': round(duration.get('p95', 0), 2),
                        '99th Percentile (ms)': round(duration.get('p99', 0), 2)
                    })
            
            if load_data:
                df_load = pd.DataFrame(load_data)
                df_load.to_excel(writer, sheet_name='Load Test Results', index=False)
        
        print("Excel report generated successfully!")
        
    except Exception as e:
        print(f"Error generating Excel report: {e}")

if __name__ == "__main__":
    generate_combined_report()
