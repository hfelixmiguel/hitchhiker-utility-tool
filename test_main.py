"""Unit tests for the Intergalactic Hitchhiker's Guide Utility."""

import pytest
from main import FuelCostCalculator, TravelAdviceGenerator


class TestFuelCostCalculator:
    """Test cases for FuelCostCalculator class."""

    def test_initialization_with_valid_rate(self):
        """Test calculator initializes with valid base rate."""
        calc = FuelCostCalculator(base_rate=1.5)
        assert calc.base_rate == 1.5

    def test_initialization_with_zero_rate(self):
        """Test calculator initializes with zero base rate."""
        calc = FuelCostCalculator(base_rate=0)
        assert calc.base_rate == 0

    def test_initialization_with_negative_rate_raises_error(self):
        """Test that negative base rate raises ValueError."""
        with pytest.raises(ValueError):
            FuelCostCalculator(base_rate=-1.0)

    def test_calculate_cost_basic(self):
        """Test basic cost calculation without tax or efficiency changes."""
        calc = FuelCostCalculator(base_rate=2.0)
        total_cost, breakdown = calc.calculate_cost(distance_ly=5.0)
        
        assert total_cost == 11.0
        assert breakdown["distance_ly"] == 5.0
        assert breakdown["base_cost"] == 10.0
        assert breakdown["tax_amount"] == 1.0  # Default 10% tax
        assert breakdown["total_cost"] == 11.0

    def test_calculate_cost_with_efficiency(self):
        """Test cost calculation with fuel efficiency modifier."""
        calc = FuelCostCalculator(base_rate=2.0)
        total_cost, breakdown = calc.calculate_cost(
            distance_ly=5.0, 
            fuel_efficiency=0.8  # Less efficient = more expensive
        )
        
        assert breakdown["base_cost"] == 12.5  # 5 * 2 / 0.8

    def test_calculate_cost_with_custom_tax(self):
        """Test cost calculation with custom tax rate."""
        calc = FuelCostCalculator(base_rate=2.0)
        total_cost, breakdown = calc.calculate_cost(
            distance_ly=10.0, 
            tax_rate=0.2  # 20% tax
        )
        
        assert breakdown["tax_amount"] == 4.0  # 20 * 0.2

    def test_calculate_cost_zero_distance(self):
        """Test cost calculation with zero distance."""
        calc = FuelCostCalculator(base_rate=1.5)
        total_cost, breakdown = calc.calculate_cost(distance_ly=0)
        
        assert total_cost == 0
        assert breakdown["total_cost"] == 0

    def test_calculate_cost_negative_distance_raises_error(self):
        """Test that negative distance raises ValueError."""
        calc = FuelCostCalculator(base_rate=1.5)
        with pytest.raises(ValueError):
            calc.calculate_cost(distance_ly=-5.0)

    def test_calculate_cost_zero_efficiency_raises_error(self):
        """Test that zero efficiency raises ValueError."""
        calc = FuelCostCalculator(base_rate=1.5)
        with pytest.raises(ValueError):
            calc.calculate_cost(distance_ly=5.0, fuel_efficiency=0)

    def test_calculate_cost_negative_efficiency_raises_error(self):
        """Test that negative efficiency raises ValueError."""
        calc = FuelCostCalculator(base_rate=1.5)
        with pytest.raises(ValueError):
            calc.calculate_cost(distance_ly=5.0, fuel_efficiency=-0.5)

    def test_breakdown_contains_currency(self):
        """Test that breakdown includes currency information."""
        calc = FuelCostCalculator(base_rate=1.5)
        _, breakdown = calc.calculate_cost(distance_ly=5.0)
        
        assert breakdown["currency"] == "Galactic Credits"


class TestTravelAdviceGenerator:
    """Test cases for TravelAdviceGenerator class."""

    def test_initialization(self):
        """Test generator initializes with advice templates."""
        gen = TravelAdviceGenerator()
        assert len(gen.advice_templates) > 0

    def test_get_advice_returns_string(self):
        """Test that get_advice returns a string."""
        gen = TravelAdviceGenerator()
        advice = gen.get_advice()
        
        assert isinstance(advice, str)
        assert len(advice) > 0

    def test_get_advice_returns_valid_template(self):
        """Test that returned advice is from templates."""
        gen = TravelAdviceGenerator()
        advice = gen.get_advice()
        
        assert advice in gen.advice_templates

    def test_get_multiple_advices_count(self):
        """Test getting multiple advices returns correct count."""
        gen = TravelAdviceGenerator()
        advices = gen.get_multiple_advices(count=3)
        
        assert len(advices) == 3

    def test_get_multiple_advices_unique(self):
        """Test that multiple advices are unique."""
        gen = TravelAdviceGenerator()
        advices = gen.get_multiple_advices(count=5)
        
        assert len(set(advices)) == 5

    def test_get_multiple_advices_zero_count_raises_error(self):
        """Test that zero count raises ValueError."""
        gen = TravelAdviceGenerator()
        with pytest.raises(ValueError):
            gen.get_multiple_advices(count=0)

    def test_get_multiple_advices_negative_count_raises_error(self):
        """Test that negative count raises ValueError."""
        gen = TravelAdviceGenerator()
        with pytest.raises(ValueError):
            gen.get_multiple_advices(count=-1)


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])