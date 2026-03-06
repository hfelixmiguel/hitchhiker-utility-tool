"""
Flask web application for Intergalactic Hitchhiker's Guide Utility.

Provides a modern, fluid UI for calculating fuel costs and generating travel advice.
Compatible with Vercel Python runtime.
Includes API key authentication and rate limiting.
"""

import json
import logging
import os
from functools import wraps
from flask import Flask, jsonify, request, render_template_string

# Import from main module
from main import FuelCostCalculator, TravelAdviceGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create Flask app - must be named 'app' for Vercel
app = Flask(__name__)

# Configuration
API_KEY = os.environ.get('API_KEY', 'hitchhiker-default-key-2026')

# Simple in-memory rate limiting
request_counts = {}

def check_rate_limit(key, limit=10, window=60):
    """Simple rate limiting check"""
    import time
    now = time.time()
    if key not in request_counts:
        request_counts[key] = []
    request_counts[key] = [t for t in request_counts[key] if now - t < window]
    if len(request_counts[key]) >= limit:
        return False
    request_counts[key].append(now)
    return True

def require_api_key(f):
    """Decorator to require API key for endpoint access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            logger.warning("Missing API key in request")
            return jsonify({
                "error": "API key required",
                "message": "Please provide API key in X-API-Key header"
            }), 401
        
        if api_key != API_KEY:
            logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
            return jsonify({
                "error": "Invalid API key",
                "message": "The provided API key is not valid"
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/calculate', methods=['POST'])
@require_api_key
def calculate_fuel_cost():
    """Calculate fuel cost for a journey."""
    if not check_rate_limit('calculate', limit=10, window=60):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        distance_ly = float(data.get('distance', 0))
        fuel_efficiency = float(data.get('efficiency', 1.0))
        tax_rate = float(data.get('tax_rate', 0.1))
        
        calculator = FuelCostCalculator(base_rate=1.5)
        total_cost, breakdown = calculator.calculate_cost(
            distance_ly=distance_ly,
            fuel_efficiency=fuel_efficiency,
            tax_rate=tax_rate
        )
        
        return jsonify({
            "success": True,
            "data": breakdown
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/advice', methods=['GET'])
@require_api_key
def get_advice():
    """Generate random travel advice."""
    if not check_rate_limit('advice', limit=20, window=60):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    
    try:
        count = request.args.get('count', 3, type=int)
        generator = TravelAdviceGenerator()
        advices = generator.get_multiple_advices(count=count)
        
        return jsonify({
            "success": True,
            "data": {"advices": advices}
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating advice: {e}")
        return jsonify({"error": "Failed to generate advice"}), 500


@app.route('/api/history', methods=['GET'])
@require_api_key
def get_history():
    """Get calculation history."""
    return jsonify({"success": True, "data": []}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint (public, no auth required)."""
    return jsonify({
        "status": "healthy",
        "service": "Intergalactic Hitchhiker's Guide Utility",
        "version": "1.0.0",
        "auth_enabled": True
    }), 200


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template_string(INDEX_TEMPLATE)


# Modern UI Template (shortened for brevity)
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intergalactic Hitchhiker's Guide</title>
    <style>
        :root { --primary: #6366f1; --secondary: #8b5cf6; --background: #0f0f20; --card-bg: #1a1a2e; --text-primary: #ffffff; --text-secondary: #a0a0c0; --success: #10b981; --error: #ef4444; --warning: #f59e0b; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--background); color: var(--text-primary); min-height: 100vh; padding: 1rem; }
        .container { max-width: 800px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 2rem; }
        h1 { font-size: 2rem; background: linear-gradient(90deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card { background: var(--card-bg); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; }
        .card-title { font-size: 1.25rem; margin-bottom: 1rem; color: var(--primary); }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.9rem; }
        input[type="number"], input[type="password"] { width: 100%; padding: 12px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 8px; color: var(--text-primary); font-size: 1rem; }
        button { background: linear-gradient(90deg, var(--primary), var(--secondary)); color: white; border: none; padding: 0.875rem 1.5rem; border-radius: 8px; font-size: 1rem; cursor: pointer; width: 100%; }
        .api-key-notice { background: rgba(245, 158, 11, 0.15); border: 1px solid var(--warning); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.85rem; color: var(--warning); }
        .result-card { background: var(--card-bg); border-radius: 16px; padding: 1.5rem; margin-top: 1.5rem; display: none; }
        .result-card.visible { display: block; animation: fadeIn 0.5s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .result-item { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .result-label { color: var(--text-secondary); }
        .result-value { font-weight: bold; color: var(--primary); }
        .advice-list { list-style: none; margin-top: 1rem; }
        .advice-item { background: rgba(99, 102, 241, 0.2); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid var(--primary); }
        .footer { text-align: center; margin-top: 2rem; color: var(--text-secondary); font-size: 0.85rem; }
        @media (min-width: 600px) { body { padding: 2rem; } h1 { font-size: 2.5rem; } .card { padding: 2rem; } button { width: auto; } }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>🚀 Intergalactic Hitchhiker's Guide</h1><p class="subtitle">Your trusted companion for cosmic travel planning</p></header>
        <div class="api-key-notice">🔐 API Authentication Enabled - Enter your API key below</div>
        <div class="card"><h2 class="card-title">🔑 API Configuration</h2><div class="form-group"><label for="api-key">API Key</label><input type="password" id="api-key" placeholder="Enter your API key..."></div></div>
        <div class="card"><h2 class="card-title">⛽ Fuel Cost Calculator</h2><div class="form-group"><label for="distance">Distance (light-years)</label><input type="number" id="distance" placeholder="Enter distance..." step="0.1" min="0"></div><div class="form-group"><label for="efficiency">Fuel Efficiency</label><input type="number" id="efficiency" value="1.0" step="0.1" min="0.1"></div><div class="form-group"><label for="tax-rate">Tax Rate (%)</label><input type="number" id="tax-rate" value="10" step="0.1" min="0" max="100"></div><button onclick="calculateFuelCost()">Calculate Cost</button></div>
        <div class="card"><h2 class="card-title">💫 Travel Advice Generator</h2><p style="color: var(--text-secondary);">Get random wisdom for your journey.</p><button onclick="getTravelAdvice()">Generate Advice</button></div>
        <div id="result-card" class="result-card"><h3>Calculation Results</h3><div id="results"></div></div>
        <div id="advice-result" class="result-card"><h3>Travel Wisdom</h3><ul id="advice-list" class="advice-list"></ul></div>
        <footer class="footer"><p>© 2026 Intergalactic Hitchhiker's Guide Utility</p></footer>
    </div>
    <script>
        let savedApiKey = localStorage.getItem('hitchhiker_api_key') || '';
        if (savedApiKey) document.getElementById('api-key').value = savedApiKey;
        function getApiKey() { const k = document.getElementById('api-key').value.trim(); if (k) localStorage.setItem('hitchhiker_api_key', k); return k; }
        async function calculateFuelCost() {
            const apiKey = getApiKey();
            if (!apiKey) return alert('Please enter API key');
            const distance = parseFloat(document.getElementById('distance').value);
            const efficiency = parseFloat(document.getElementById('efficiency').value);
            const taxRate = parseFloat(document.getElementById('tax-rate').value) / 100;
            try {
                const res = await fetch('/api/calculate', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey }, body: JSON.stringify({ distance, efficiency, tax_rate: taxRate }) });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('results').innerHTML = '<div class="result-item"><span class="result-label">Distance:</span><span class="result-value">' + data.data.distance_ly + ' light-years</span></div><div class="result-item"><span class="result-label">Total Cost:</span><span class="result-value" style="color:#10b981">' + data.data.total_cost + ' Galactic Credits</span></div>';
                    document.getElementById('result-card').classList.add('visible');
                }
            } catch (e) { alert('Error: ' + e.message); }
        }
        async function getTravelAdvice() {
            const apiKey = getApiKey();
            if (!apiKey) return alert('Please enter API key');
            try {
                const res = await fetch('/api/advice?count=3', { headers: { 'X-API-Key': apiKey } });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('advice-list').innerHTML = data.data.advices.map(a => '<li class="advice-item">' + a + '</li>').join('');
                    document.getElementById('advice-result').classList.add('visible');
                }
            } catch (e) { alert('Error: ' + e.message); }
        }
    </script>
</body>
</html>'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)