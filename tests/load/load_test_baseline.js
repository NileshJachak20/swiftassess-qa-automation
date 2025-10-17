/**
 * K6 Load Test - Baseline Test (10 concurrent users)
 * SwiftAssess Signup Page Load Testing
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 10 }, // Ramp up to 10 users over 1 minute
    { duration: '5m', target: 10 }, // Stay at 10 users for 5 minutes
    { duration: '1m', target: 0 },   // Ramp down to 0 users over 1 minute
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
    http_req_failed: ['rate<0.01'],    // Error rate should be less than 1%
    errors: ['rate<0.01'],
  },
};

// Test data
const testUsers = [
  {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    password: 'SecurePass123!',
    confirmPassword: 'SecurePass123!',
  },
  {
    firstName: 'Jane',
    lastName: 'Smith',
    email: 'jane.smith@example.com',
    password: 'TestPass456@',
    confirmPassword: 'TestPass456@',
  },
  {
    firstName: 'Bob',
    lastName: 'Johnson',
    email: 'bob.johnson@example.com',
    password: 'MyPassword789#',
    confirmPassword: 'MyPassword789#',
  },
  {
    firstName: 'Alice',
    lastName: 'Brown',
    email: 'alice.brown@example.com',
    password: 'StrongPass123$',
    confirmPassword: 'StrongPass123$',
  },
  {
    firstName: 'Charlie',
    lastName: 'Wilson',
    email: 'charlie.wilson@example.com',
    password: 'SecureKey456%',
    confirmPassword: 'SecureKey456%',
  }
];

// Base URL
const BASE_URL = 'https://app-stg.swiftassess.com';

export default function () {
  // Select random user data
  const user = testUsers[Math.floor(Math.random() * testUsers.length)];
  
  // Add unique timestamp to email to avoid duplicates
  const timestamp = Date.now();
  const uniqueEmail = user.email.replace('@', `+${timestamp}@`);
  
  // Test 1: Load signup page
  console.log(`[VU ${__VU}] Loading signup page...`);
  const signupPageResponse = http.get(`${BASE_URL}/Signup`);
  
  const signupPageCheck = check(signupPageResponse, {
    'signup page loads successfully': (r) => r.status === 200,
    'signup page contains form': (r) => r.body.includes('firstName') || r.body.includes('signup'),
    'signup page response time < 2s': (r) => r.timings.duration < 2000,
  });
  
  errorRate.add(!signupPageCheck);
  responseTime.add(signupPageResponse.timings.duration);
  
  if (!signupPageCheck) {
    console.error(`[VU ${__VU}] Failed to load signup page: ${signupPageResponse.status}`);
    return;
  }
  
  sleep(1); // Wait between requests
  
  // Test 2: Submit signup form
  console.log(`[VU ${__VU}] Submitting signup form for ${uniqueEmail}...`);
  
  const signupData = {
    firstName: user.firstName,
    lastName: user.lastName,
    email: uniqueEmail,
    password: user.password,
    confirmPassword: user.confirmPassword,
    terms: 'on',
    privacy: 'on'
  };
  
  const signupResponse = http.post(`${BASE_URL}/Signup`, signupData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    },
  });
  
  const signupCheck = check(signupResponse, {
    'signup form submission successful': (r) => r.status === 200 || r.status === 302,
    'signup response time < 3s': (r) => r.timings.duration < 3000,
    'no server errors': (r) => r.status < 500,
  });
  
  errorRate.add(!signupCheck);
  responseTime.add(signupResponse.timings.duration);
  
  if (!signupCheck) {
    console.error(`[VU ${__VU}] Signup form submission failed: ${signupResponse.status}`);
    console.error(`Response body: ${signupResponse.body}`);
  } else {
    console.log(`[VU ${__VU}] Signup form submitted successfully`);
  }
  
  sleep(2); // Wait between iterations
  
  // Test 3: Verify signup success (optional)
  if (signupResponse.status === 302 || signupResponse.status === 200) {
    console.log(`[VU ${__VU}] Verifying signup success...`);
    
    // Check if redirected to success page or dashboard
    const successResponse = http.get(`${BASE_URL}/dashboard`);
    
    const successCheck = check(successResponse, {
      'success page loads': (r) => r.status === 200,
      'success page response time < 2s': (r) => r.timings.duration < 2000,
    });
    
    errorRate.add(!successCheck);
    responseTime.add(successResponse.timings.duration);
  }
  
  sleep(1); // Final wait
}

export function handleSummary(data) {
  return {
    'reports/baseline_test_results.json': JSON.stringify(data, null, 2),
    'reports/baseline_test_summary.html': generateHTMLReport(data, 'Baseline Test Results'),
  };
}

function generateHTMLReport(data, title) {
  const summary = data.metrics;
  const totalRequests = summary.http_reqs.values.count;
  const failedRequests = summary.http_req_failed.values.count;
  const avgResponseTime = summary.http_req_duration.values.avg;
  const p95ResponseTime = summary.http_req_duration.values.p95;
  const p99ResponseTime = summary.http_req_duration.values.p99;
  const errorRate = (failedRequests / totalRequests * 100).toFixed(2);
  
  return `
    <!DOCTYPE html>
    <html>
    <head>
        <title>${title}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
            .metric { margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-radius: 3px; }
            .good { color: green; }
            .warning { color: orange; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>${title}</h1>
            <p>Generated on: ${new Date().toLocaleString()}</p>
        </div>
        
        <div class="metrics">
            <h2>Test Summary</h2>
            <div class="metric">
                <strong>Total Requests:</strong> ${totalRequests}
            </div>
            <div class="metric">
                <strong>Failed Requests:</strong> ${failedRequests}
            </div>
            <div class="metric">
                <strong>Error Rate:</strong> <span class="${errorRate > 5 ? 'error' : errorRate > 1 ? 'warning' : 'good'}">${errorRate}%</span>
            </div>
            <div class="metric">
                <strong>Average Response Time:</strong> ${avgResponseTime.toFixed(2)}ms
            </div>
            <div class="metric">
                <strong>95th Percentile Response Time:</strong> ${p95ResponseTime.toFixed(2)}ms
            </div>
            <div class="metric">
                <strong>99th Percentile Response Time:</strong> ${p99ResponseTime.toFixed(2)}ms
            </div>
        </div>
        
        <div class="analysis">
            <h2>Analysis</h2>
            <p><strong>Test Type:</strong> Baseline Load Test</p>
            <p><strong>Concurrent Users:</strong> 10</p>
            <p><strong>Duration:</strong> 7 minutes (1m ramp up, 5m steady, 1m ramp down)</p>
            <p><strong>Target:</strong> Assess system behavior under normal load</p>
        </div>
    </body>
    </html>
  `;
}
