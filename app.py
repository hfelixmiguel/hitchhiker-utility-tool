"""
Flask web application for Intergalactic Hitchhiker's Guide Utility.

Provides a modern, fluid UI for calculating fuel costs and generating travel advice.
"""

import logging
from flask import Flask, jsonify, request, render_template_string

# Import from main module
from main import FuelCostCalculator, TravelAdviceGenerator, ConfigurationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template_string(INDEX_TEMPLATE)


@app.route('/api/calculate', methods=['POST'])
def calculate_fuel_cost():
    """Calculate fuel cost for a journey.
    
    Returns:
        JSON response with calculation results or error message
    """
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
        
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/advice', methods=['GET'])
def get_advice():
    """Generate random travel advice."""
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


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Intergalactic Hitchhiker's Guide Utility"
    }), 200


# Modern UI Template with embedded HTML/CSS/JS
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
            padding: 2rem;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
        }

        .card-title {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: var(--primary);
        }

        .form-group {
            margin-bottom: 1.5rem;
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
            border: 1px solid var(--primary);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input[type="number"]:focus {
            outline: none;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.5);
        }

        button {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        .result-card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 2rem;
            margin-top: 2rem;
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
        }

        .loading {
            text-align: center;
            color: var(--text-secondary);
            display: none;
        }

        .error-message {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid var(--error);
            padding: 1rem;
            border-radius: 8px;
            color: var(--error);
            display: none;
        }

        .footer {
            text-align: center;
            margin-top: 3rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
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
            </div>

            <div class="form-group">
                <label for="efficiency">Fuel Efficiency</label>
                <input type="number" id="efficiency" value="1.0" step="0.1" min="0.1">
            </div>

            <div class="form-group">
                <label for="tax-rate">Tax Rate (%)</label>
                <input type="number" id="tax-rate" value="10" step="0.1" min="0" max="100">
            </div>

            <button onclick="calculateFuelCost()">Calculate Cost</button>
        </div>

        <div class="card">
            <h2 class="card-title">💫 Travel Advice Generator</h2>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">Get random wisdom for your intergalactic journey.</p>
            <button onclick="getTravelAdvice()">Generate Advice</button>
        </div>

        <div id="result-card" class="result-card">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">Calculation Results</h3>
            <div id="results"></div>
        </div>

        <div id="advice-result" class="result-card">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">Travel Wisdom</h3>
            <ul id="advice-list" class="advice-list"></ul>
        </div>

        <div id="loading" class="loading">Calculating...</div>
        <div id="error-message" class="error-message"></div>

        <footer class="footer">
            <p>© 2026 Intergalactic Hitchhiker's Guide Utility</p>
        </footer>
    </div>

    <script>
        async function calculateFuelCost() {
            const distance = parseFloat(document.getElementById('distance').value) || 0;
            const efficiency = parseFloat(document.getElementById('efficiency').value) || 1.0;
            const taxRate = parseFloat(document.getElementById('tax-rate').value) / 100 || 0.1;

            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({distance, efficiency, tax_rate: taxRate})
                });

                if (!response.ok) throw new Error('Calculation failed');
                
                const data = await response.json();
                displayResults(data.data);
            } catch (error) {
                showError(error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
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

        async function getTravelAdvice() {
            const adviceResult = document.getElementById('advice-result');
            
            try {
                const response = await fetch('/api/advice?count=3');
                
                if (!response.ok) throw new Error('Failed to generate advice');
                
                const data = await response.json();
                displayAdvice(data.data.advices);
            } catch (error) {
                showError(error.message);
            }
        }

        function displayAdvice(advices) {
            const listEl = document.getElementById('advice-list');
            listEl.innerHTML = advices.map(advice => 
                `<li class="advice-item">${advice}</li>`
            ).join('');
            adviceResult.classList.add('visible');
        }

        function showError(message) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    </script>
</body>
</html>'''


if __name__ == '__main__':
    logger.info("Starting Flask web server...")
    app.run(host='0.0.0.0', port=5000, debug=True)