# Intergalactic Hitchhiker's Guide Utility

![CI/CD](https://github.com/hfelixmiguel/hitchhiker-utility-tool/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/github/license/hfelixmiguel/hitchhiker-utility-tool.svg)

A Python utility for calculating galactic fuel costs and providing travel advice for intergalactic journeys.

## Features

- **Fuel Cost Calculator**: Calculate fuel costs for space travel with customizable parameters
- **Travel Advice Generator**: Get random travel wisdom in the spirit of the Guide
- **Modern Web UI**: Interactive web interface with real-time calculations
- **CLI Interface**: Use as a Python module in your own projects

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

### Python Module

```python
from main import FuelCostCalculator, TravelAdviceGenerator

# Calculate fuel costs
calculator = FuelCostCalculator(base_rate=1.5)
total_cost, breakdown = calculator.calculate_cost(
    distance_ly=10.0,
    fuel_efficiency=1.0,
    tax_rate=0.1
)

# Get travel advice
generator = TravelAdviceGenerator()
advice = generator.get_advice()
```

## Testing

```bash
pytest test_main.py -v
```

## Development

### Codespace

Click the "Code" button on GitHub and select "Create codespace" for a ready-to-use development environment.

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_main.py -v

# Start web server
python app.py
```

## License

MIT License
