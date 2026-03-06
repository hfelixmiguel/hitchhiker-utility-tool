"""
Flask web application for Intergalactic Hitchhiker's Guide Utility.

Provides a modern, fluid UI for calculating fuel costs and generating travel advice.
Compatible with Vercel Python runtime.
"""

import json
import logging
from flask import Flask, jsonify, request, render_template_string

# Import from main module
from main import FuelCostCalculator, TravelAdviceGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple in-memory rate limiting (for demonstration)
request_counts = {}

def check_rate_limit(key, limit=10, window=60):
    """Simple rate limiting check"""
    import time
    now = time.time()
    if key not in request_counts:
        request_counts[key] = []
    # Clean old requests
    request_counts[key] = [t for t in request_counts[key] if now - t < window]
    if len(request_counts[key]) >= limit:
        return False
    request_counts[key].append(now)
    return True

# Apply rate limits to API endpoints
@app.route('/api/calculate', methods=['POST'])
def calculate_fuel_cost():
    """Calculate fuel cost for a journey.
    
    Returns:
        JSON response with calculation results or error message
    """
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
def get_history():
    """Get calculation history."""
    return jsonify({"success": True, "data": []}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Intergalactic Hitchhiker's Guide Utility"
    }), 200


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template_string(INDEX_TEMPLATE)


# Modern UI Template with enhanced features
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intergalactic Hitchhiker's Guide</title>
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --background: #0f0f20;
            --card-bg: #1a1a2e;
            --text-primary: #ffffff;
            --text-secondary: #a0a0c0;
            --success: #10b981;
            --error: #ef4444;
            --warning: #f59e0b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 1rem;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            font-size: 2rem;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
        }

        .card-title {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--primary);
        }

        .form-group {
            margin-bottom: 1rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        input[type="number"] {
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input[type="number"]:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
        }

        input[type="number"].input-error {
            border-color: var(--error);
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.3);
        }

        .error-hint {
            color: var(--error);
            font-size: 0.8rem;
            margin-top: 0.25rem;
            display: none;
        }

        .error-hint.visible {
            display: block;
        }

        button {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 0.875rem 1.5rem;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }

        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .result-card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            display: none;
        }

        .result-card.visible {
            display: block;
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .result-item:last-child {
            border-bottom: none;
        }

        .result-label {
            color: var(--text-secondary);
        }

        .result-value {
            font-weight: bold;
            color: var(--primary);
        }

        .advice-list {
            list-style: none;
            margin-top: 1rem;
        }

        .advice-item {
            background: rgba(99, 102, 241, 0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 3px solid var(--primary);
            animation: fadeIn 0.3s ease-in-out;
        }

        .loading {
            text-align: center;
            color: var(--text-secondary);
            display: none;
            padding: 1rem;
        }

        .loading.visible {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .spinner {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        .error-message {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--error);
            padding: 1rem;
            border-radius: 8px;
            color: var(--error);
            display: none;
            margin-top: 1rem;
        }

        .error-message.visible {
            display: block;
            animation: fadeIn 0.3s ease-in-out;
        }

        .history-section {
            margin-top: 1.5rem;
        }

        .history-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            display: flex;
            justify-content: space-between;
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        @media (min-width: 600px) {
            body { padding: 2rem; }
            h1 { font-size: 2.5rem; }
            .card { padding: 2rem; }
            .card-title { font-size: 1.5rem; }
            button { width: auto; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Intergalactic Hitchhiker's Guide</h1>
            <p class="subtitle">Your trusted companion for cosmic travel planning</p>
        </header>

        <div class="card">
            <h2 class="card-title">⛽ Fuel Cost Calculator</h2>
            
            <div class="form-group">
                <label for="distance">Distance (light-years)</label>
                <input type="number" id="distance" placeholder="Enter distance..." step="0.1" min="0">
                <div id="distance-error" class="error-hint">Please enter a valid positive number</div>
            </div>

            <div class="form-group">
                <label for="efficiency">Fuel Efficiency</label>
                <input type="number" id="efficiency" value="1.0" step="0.1" min="0.1">
                <div id="efficiency-error" class="error-hint">Efficiency must be greater than 0</div>
            </div>

            <div class="form-group">
                <label for="tax-rate">Tax Rate (%)</label>
                <input type="number" id="tax-rate" value="10" step="0.1" min="0" max="100">
                <div id="tax-error" class="error-hint">Tax rate must be between 0 and 100</div>
            </div>

            <button id="calc-btn" onclick="calculateFuelCost()">Calculate Cost</button>
        </div>

        <div class="card">
            <h2 class="card-title">💫 Travel Advice Generator</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Get random wisdom for your intergalactic journey.</p>
            <button id="advice-btn" onclick="getTravelAdvice()">Generate Advice</button>
        </div>

        <div id="loading" class="loading">
            <div class="spinner"></div>
            <span>Calculating...</span>
        </div>

        <div id="error-message" class="error-message"></div>

        <div id="result-card" class="result-card">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">Calculation Results</h3>
            <div id="results"></div>
        </div>

        <div id="advice-result" class="result-card">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">Travel Wisdom</h3>
            <ul id="advice-list" class="advice-list"></ul>
        </div>

        <div class="history-section" id="history-section" style="display: none;">
            <div class="card">
                <h3 class="card-title">📜 Recent Calculations</h3>
                <div id="history-list"></div>
            </div>
        </div>

        <footer class="footer">
            <p>© 2026 Intergalactic Hitchhiker's Guide Utility</p>
        </footer>
    </div>

    <script>
        let calculationHistory = JSON.parse(localStorage.getItem('fuelHistory') || '[]');
        updateHistoryDisplay();

        function validateInputs() {
            let isValid = true;
            const distance = document.getElementById('distance');
            const efficiency = document.getElementById('efficiency');
            const taxRate = document.getElementById('tax-rate');
            
            ['distance', 'efficiency', 'tax'].forEach(id => {
                document.getElementById(id + '-error')?.classList.remove('visible');
            });
            [distance, efficiency, taxRate].forEach(el => el.classList.remove('input-error'));
            
            if (distance.value === '' || parseFloat(distance.value) < 0) {
                distance.classList.add('input-error');
                document.getElementById('distance-error').classList.add('visible');
                isValid = false;
            }
            
            if (!efficiency.value || parseFloat(efficiency.value) <= 0) {
                efficiency.classList.add('input-error');
                document.getElementById('efficiency-error').classList.add('visible');
                isValid = false;
            }
            
            const tax = parseFloat(taxRate.value);
            if (tax < 0 || tax > 100) {
                taxRate.classList.add('input-error');
                document.getElementById('tax-error').classList.add('visible');
                isValid = false;
            }
            
            return isValid;
        }

        function setLoading(loading) {
            const loadingEl = document.getElementById('loading');
            const calcBtn = document.getElementById('calc-btn');
            const adviceBtn = document.getElementById('advice-btn');
            
            if (loading) {
                loadingEl.classList.add('visible');
                calcBtn.disabled = true;
                adviceBtn.disabled = true;
            } else {
                loadingEl.classList.remove('visible');
                calcBtn.disabled = false;
                adviceBtn.disabled = false;
            }
        }

        function showError(message) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = message;
            errorDiv.classList.add('visible');
            setTimeout(() => errorDiv.classList.remove('visible'), 5000);
        }

        function hideError() {
            document.getElementById('error-message').classList.remove('visible');
        }

        async function calculateFuelCost() {
            hideError();
            if (!validateInputs()) return;

            const distance = parseFloat(document.getElementById('distance').value);
            const efficiency = parseFloat(document.getElementById('efficiency').value);
            const taxRate = parseFloat(document.getElementById('tax-rate').value) / 100;

            setLoading(true);
            
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({distance, efficiency, tax_rate: taxRate})
                });

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || 'Calculation failed');
                }
                
                const data = await response.json();
                displayResults(data.data);
                addToHistory(data.data);
            } catch (error) {
                showError(error.message);
            } finally {
                setLoading(false);
            }
        }

        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <div class="result-item">
                    <span class="result-label">Distance:</span>
                    <span class="result-value">${result.distance_ly} light-years</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Base Cost:</span>
                    <span class="result-value">${result.base_cost} Galactic Credits</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Tax Amount:</span>
                    <span class="result-value">${result.tax_amount} Galactic Credits</span>
                </div>
                <div class="result-item" style="font-size: 1.2rem;"> 
                    <span class="result-label"><strong>Total Cost:</strong></span>
                    <span class="result-value" style="color: #10b981;"><strong>${result.total_cost} ${result.currency}</strong></span>
                </div>
            `;
            document.getElementById('result-card').classList.add('visible');
        }

        function addToHistory(result) {
            const entry = {
                distance: result.distance_ly,
                total: result.total_cost,
                currency: result.currency,
                timestamp: new Date().toLocaleTimeString()
            };
            calculationHistory.unshift(entry);
            if (calculationHistory.length > 5) calculationHistory.pop();
            localStorage.setItem('fuelHistory', JSON.stringify(calculationHistory));
            updateHistoryDisplay();
        }

        function updateHistoryDisplay() {
            const section = document.getElementById('history-section');
            const list = document.getElementById('history-list');
            
            if (calculationHistory.length === 0) {
                section.style.display = 'none';
                return;
            }
            
            section.style.display = 'block';
            list.innerHTML = calculationHistory.map(h => `
                <div class="history-item">
                    <span>${h.distance} ly → ${h.total} ${h.currency}</span>
                    <span style="color: var(--text-secondary);">${h.timestamp}</span>
                </div>
            `).join('');
        }

        async function getTravelAdvice() {
            hideError();
            setLoading(true);
            
            try {
                const response = await fetch('/api/advice?count=3');
                
                if (!response.ok) throw new Error('Failed to generate advice');
                
                const data = await response.json();
                displayAdvice(data.data.advices);
            } catch (error) {
                showError(error.message);
            } finally {
                setLoading(false);
            }
        }

        function displayAdvice(advices) {
            const listEl = document.getElementById('advice-list');
            listEl.innerHTML = advices.map((advice, i) => `
                <li class="advice-item" style="animation-delay: ${i * 0.1}s">${advice}</li>
            `).join('');
            document.getElementById('advice-result').classList.add('visible');
        }
    </script>
</body>
</html>'''


# Vercel handler function
def handler(event, context):
    """Vercel Python handler function"""
    return app(event, context)


if __name__ == '__main__':
    logger.info("Starting Flask web server...")
    app.run(host='0.0.0.0', port=5000, debug=True)